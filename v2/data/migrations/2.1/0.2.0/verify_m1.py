#!/usr/bin/env python3
"""Read-only, versioned W6 -> 2.1 provenance slice and paired regression."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import psycopg
import rdflib
from psycopg import sql
from psycopg.rows import dict_row
from pyshacl import validate
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.compare import to_canonical_graph
from rdflib.namespace import DCTERMS, XSD

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools/v2_data"))
from compare_sql_sparql import normalize_rows  # noqa: E402

CMPE = Namespace("https://w3id.org/cm-pharme/2.1/")
INST = "https://w3id.org/cm-pharme/2.1/instance/"
PROV = Namespace("http://www.w3.org/ns/prov#")
SOURCE_SQL = """
SELECT d.public_id AS dataset_public, d.doi,
       dr.public_id AS release_public, sr.row_number, sr.source_hash,
       tr.public_id AS run_public
FROM cmpe.source_record sr
JOIN cmpe.dataset_release dr ON dr.dataset_release_id=sr.dataset_release_id
JOIN cmpe.dataset d ON d.dataset_id=dr.dataset_id
LEFT JOIN cmpe.transformation_run tr ON tr.transformation_run_id=sr.transformation_run_id
WHERE d.doi IS NOT NULL
ORDER BY d.public_id, dr.public_id, sr.row_number, sr.source_hash, tr.public_id
"""
PAIR_SPARQL = """
PREFIX cmpe: <https://w3id.org/cm-pharme/2.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?doi ?release_public ?row_number ?source_hash ?run_public WHERE {
  ?d a cmpe:Dataset ; dct:identifier ?doi ; cmpe:hasDatasetRelease ?release .
  ?release a cmpe:DatasetRelease ; dct:identifier ?release_public ;
           cmpe:containsSourceRecord ?sr .
  ?sr a cmpe:SourceRecord ; rdf:value ?row_number ; prov:value ?source_hash .
  OPTIONAL { ?sr prov:wasGeneratedBy ?run . ?run dct:identifier ?run_public . }
} ORDER BY ?doi ?release_public ?row_number ?source_hash ?run_public
"""
COLUMNS = ["doi", "release_public", "row_number", "source_hash", "run_public"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode()


def node(kind: str, key: str) -> URIRef:
    return URIRef(INST + kind + "/" + quote(key, safe=""))


def source_key(row: dict) -> str:
    return json.dumps([row["release_public"], row["row_number"], row["source_hash"]], ensure_ascii=False, separators=(",", ":"))


def canonical(g: Graph) -> bytes:
    lines = sorted(f"{s.n3()} {p.n3()} {o.n3()} .\n" for s, p, o in to_canonical_graph(g))
    return "".join(lines).encode()


def pin_inputs(config: dict):
    for name, expected in config["sha256"].items():
        actual = sha((ROOT / name).read_bytes())
        if actual != expected:
            raise SystemExit(f"Pinned input changed: {name}: {actual} != {expected}")


def check_dispositions():
    prior = list(csv.DictReader((ROOT / "v2/data/migrations/2.1/0.1.0/w6-mapping-crosswalk.csv").open()))
    rows = list(csv.DictReader((HERE / "mapping-dispositions.csv").open()))
    if len(rows) != len(prior) or {r["mapping_id"] for r in rows} != {r["mapping_id"] for r in prior}:
        raise SystemExit("The 36-row disposition register differs from the pinned W6 crosswalk")
    selected = {"M001", "M002", "M003", "M004"}
    for row in rows:
        expected = "EXECUTED_BOUNDED_21" if row["mapping_id"] in selected else (
            "ZERO_CHANGE_NO_TABLE" if row["mapping_id"] in {"M035", "M036"} else
            "QUALITY_REVIEW_NO_21_EXPORT" if row["mapping_id"] == "M023" else
            "UNIMPLEMENTED_21_KEEP_20")
        if row["disposition"] != expected or not row["reason"].strip():
            raise SystemExit(f"Invalid disposition for {row['mapping_id']}")
    return {r["disposition"]: sum(x["disposition"] == r["disposition"] for x in rows)
            for r in rows}


def database_snapshot(url: str) -> dict:
    with psycopg.connect(url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='cmpe' ORDER BY tablename")
            names = [r["tablename"] for r in cur.fetchall()]
            table_data = {}
            counts = {}
            for name in names:
                cur.execute(sql.SQL("SELECT to_jsonb(t)::text AS doc FROM {} AS t").format(sql.Identifier("cmpe", name)))
                values = sorted(r["doc"] for r in cur.fetchall())
                table_data[name] = sha(compact(values))
                counts[name] = len(values)
            cur.execute("""SELECT table_name,column_name,data_type,is_nullable,column_default
                           FROM information_schema.columns WHERE table_schema='cmpe'
                           ORDER BY table_name,ordinal_position""")
            columns = [dict(r) for r in cur.fetchall()]
            cur.execute("""SELECT c.conrelid::regclass::text AS relation,c.conname,
                                  pg_get_constraintdef(c.oid) AS definition
                           FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace
                           WHERE n.nspname='cmpe' ORDER BY 1,2""")
            constraints = [dict(r) for r in cur.fetchall()]
            cur.execute("SELECT version() AS pg_version, postgis_full_version() AS postgis_version")
            version = dict(cur.fetchone())
    return {"data_sha256": sha(compact(table_data)), "table_sha256": table_data,
            "row_counts": counts, "schema_sha256": sha(compact([columns, constraints])), "versions": version}


def sql_rows(url: str) -> list[dict]:
    with psycopg.connect(url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            cur.execute(SOURCE_SQL)
            return [dict(r) for r in cur.fetchall()]


def build_graph(rows: list[dict]) -> Graph:
    g = Graph()
    for prefix, ns in [("cmpe", CMPE), ("prov", PROV), ("dct", DCTERMS)]:
        g.bind(prefix, ns)
    for r in rows:
        d = node("dataset", r["dataset_public"])
        release = node("dataset-release", r["release_public"])
        record = node("source-record", source_key(r))
        g.add((d, RDF.type, CMPE.Dataset))
        g.add((d, DCTERMS.identifier, Literal(r["doi"])))
        g.add((d, CMPE.hasDatasetRelease, release))
        g.add((release, RDF.type, CMPE.DatasetRelease))
        g.add((release, DCTERMS.identifier, Literal(r["release_public"])))
        g.add((release, CMPE.containsSourceRecord, record))
        g.add((record, RDF.type, CMPE.SourceRecord))
        g.add((record, DCTERMS.identifier, Literal(source_key(r))))
        g.add((record, RDF.value, Literal(r["row_number"], datatype=XSD.integer)))
        g.add((record, PROV.value, Literal(r["source_hash"])))
        if r["run_public"]:
            run = node("provenance-activity", r["run_public"])
            g.add((run, RDF.type, CMPE.ProvenanceActivity))
            g.add((run, DCTERMS.identifier, Literal(r["run_public"])))
            g.add((record, PROV.wasGeneratedBy, run))
    return g


def run_legacy(url: str, folder: Path) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    kg, manifest, eq = folder / "legacy.ttl", folder / "legacy-manifest.json", folder / "legacy-pairs.json"
    for command in [
        ["tools/v2_data/export_kg.py", "--database-url", url, "--output", str(kg), "--manifest", str(manifest)],
        ["tools/v2_data/compare_sql_sparql.py", "--database-url", url, "--kg", str(kg), "--report", str(eq)],
    ]:
        subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT, check=True, capture_output=True, text=True)
    result = json.loads(eq.read_text())
    assert result["passed"] and result["benchmarks_passed"] == result["benchmarks_total"] == 4
    return {"kg_sha256": json.loads(manifest.read_text())["canonical_ntriples_sha256"],
            "query_sha256": sha(compact(result["results"])), "pairs_passed": 4,
            "kg_triples": json.loads(manifest.read_text())["triple_count"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--database-url", default=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cmpe"))
    ap.add_argument("--output-dir", default="build/v2-21-rdb-m1")
    a = ap.parse_args()
    out = ROOT / a.output_dir
    out.mkdir(parents=True, exist_ok=True)
    config = json.loads((HERE / "scope.json").read_text())
    pin_inputs(config)
    dispositions = check_dispositions()

    before = database_snapshot(a.database_url)
    legacy_before = run_legacy(a.database_url, out / "before")
    rows = sql_rows(a.database_url)
    if not rows:
        raise SystemExit("Fixture contains no source-record witness")
    g = build_graph(rows)
    candidate = Graph().parse(ROOT / config["candidate_ontology"], format="turtle")
    for cls in [CMPE.Dataset, CMPE.DatasetRelease, CMPE.SourceRecord, CMPE.ProvenanceActivity,
                CMPE.hasDatasetRelease, CMPE.containsSourceRecord]:
        if not list(candidate.triples((cls, None, None))):
            raise SystemExit(f"Candidate term missing: {cls}")
    shapes = Graph().parse(ROOT / config["candidate_shapes"], format="turtle")
    conforms, _, report = validate(g, shacl_graph=shapes, ont_graph=candidate,
                                   inference="rdfs", advanced=True, meta_shacl=True)
    if not conforms:
        raise SystemExit(f"Bounded 2.1 graph fails candidate SHACL: {report}")
    nt = canonical(g)
    (out / "provenance-21.nt").write_bytes(nt)
    g.serialize(out / "provenance-21.ttl", format="turtle")
    reparsed = Graph().parse(out / "provenance-21.nt", format="nt")
    if canonical(reparsed) != nt:
        raise SystemExit("RDF serialization round trip differs")
    qres = reparsed.query(PAIR_SPARQL)
    sparql_rows = [{str(var): row[i] for i, var in enumerate(qres.vars)} for row in qres]
    normalized_sql = normalize_rows(rows, COLUMNS)
    normalized_rdf = normalize_rows(sparql_rows, COLUMNS)
    if normalized_sql != normalized_rdf:
        raise SystemExit("Q21-01 normalized SQL/SPARQL tuples differ")
    keys = {(r["release_public"], int(r["row_number"]), r["source_hash"]): source_key(r) for r in rows}
    if len(keys) != len(rows):
        raise SystemExit("Composite source identity collision in copied fixture")
    for r in rows:
        n = node("source-record", source_key(r))
        if json.loads(str(reparsed.value(n, DCTERMS.identifier))) != [r["release_public"], r["row_number"], r["source_hash"]]:
            raise SystemExit("RDF round trip lost a source identity")
    legacy_after = run_legacy(a.database_url, out / "after")
    after = database_snapshot(a.database_url)
    if before != after or legacy_before != legacy_after:
        raise SystemExit("W6 database or 2.0 KG changed during 2.1 read-only projection")
    report = {"schema_version": 1, "passed": True, "scope": "M001-M004 only",
              "source_commit": config["w6_commit"], "model_commit": config["model_commit"],
              "selected_mapping_ids": ["M001", "M002", "M003", "M004"],
              "dispositions": dispositions, "database_before": before, "database_after_sha256": before["data_sha256"],
              "schema_after_sha256": before["schema_sha256"], "legacy_before": legacy_before,
              "legacy_after": legacy_after, "q21_01": {"rows": len(normalized_sql),
              "sql_normalized_sha256": sha(compact(normalized_sql)),
              "sparql_normalized_sha256": sha(compact(normalized_rdf)), "passed": True},
              "rdf_roundtrip": True, "shacl_conforms": bool(conforms),
              "graph_triples": len(g), "graph_sha256": sha(nt),
              "software": {"python": platform.python_version(), "psycopg": psycopg.__version__,
                           "rdflib": rdflib.__version__},
              "rollback": "No DDL or DML was applied; remove the separate 2.1 export files to roll back. All W6 tables, ontology_iri defaults and the 2.0 exporter remain byte-identical.",
              "boundary": "Synthetic copied W6 fixture only; no full-source download, role/quality promotion, complete 36-row export or GA acceptance."}
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({k: report[k] for k in ["passed", "scope", "q21_01", "graph_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
