#!/usr/bin/env python3
"""Compare paired SQL and SPARQL benchmark answers over W6 fixture data."""
from __future__ import annotations

import argparse
import json
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from rdflib import Graph


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--database-url", default=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cmpe"))
    p.add_argument("--kg", default="build/w6/cm-pharme-v2-fixture-kg.ttl")
    p.add_argument("--benchmarks", default="v2/data/queries/sql-sparql-benchmarks.json")
    p.add_argument("--report", default="build/w6/sql-sparql-equivalence.json")
    return p.parse_args()


def canon(v):
    if v is None:
        return None
    if hasattr(v, "toPython"):
        v = v.toPython()
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, Decimal, float)):
        try:
            d = Decimal(str(v))
            if d == d.to_integral():
                return str(d.quantize(Decimal(1)))
            return format(d.normalize(), "f")
        except InvalidOperation:
            pass
    return str(v)


def normalize_rows(rows, columns):
    return sorted(tuple(canon(r.get(c)) for c in columns) for r in rows)


def main():
    a = args()
    registry = json.loads(Path(a.benchmarks).read_text(encoding="utf-8"))
    kg = Graph().parse(a.kg, format="turtle")
    results = []
    with psycopg.connect(a.database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            for b in registry["benchmarks"]:
                columns = b["columns"]
                cur.execute(b["sql"])
                sql_rows = [dict(r) for r in cur.fetchall()]
                sparql_rows = []
                qres = kg.query(b["sparql"])
                for row in qres:
                    sparql_rows.append({str(var): row[i] for i, var in enumerate(qres.vars)})
                sql_norm = normalize_rows(sql_rows, columns)
                sp_norm = normalize_rows(sparql_rows, columns)
                passed = sql_norm == sp_norm
                results.append({
                    "id": b["id"],
                    "purpose": b["purpose"],
                    "passed": passed,
                    "sql_rows": len(sql_norm),
                    "sparql_rows": len(sp_norm),
                    "sql_normalized": sql_norm,
                    "sparql_normalized": sp_norm,
                })
                if not passed:
                    raise SystemExit(f"SQL/SPARQL mismatch for {b['id']}: SQL={sql_norm!r} SPARQL={sp_norm!r}")

    report = {
        "schema_version": 1,
        "passed": all(r["passed"] for r in results),
        "benchmarks_passed": sum(1 for r in results if r["passed"]),
        "benchmarks_total": len(results),
        "results": results,
        "interpretation_boundary": "Equivalence is established only for the registered W6 fixture benchmark queries, not for all possible SQL/SPARQL queries."
    }
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
