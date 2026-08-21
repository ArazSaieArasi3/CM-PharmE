#!/usr/bin/env python3
"""Evaluate bounded semantic consistency across CM-PharmE ontology, RDB and RDF/KG.

This evaluator is deliberately scoped to the registered mappings, the W6 reference
realization and the frozen SQL↔SPARQL benchmark set. It does not claim universal
round-trip equivalence between relational and RDF representations.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from collections import Counter
from pathlib import Path
from urllib.parse import quote

import psycopg
from psycopg.rows import dict_row
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.namespace import DCTERMS

CMPE_NS = "https://w3id.org/cm-pharme/2.0/"
INST = "https://w3id.org/cm-pharme/2.0/instance/"
CMPE = Namespace(CMPE_NS)
PROV = Namespace("http://www.w3.org/ns/prov#")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--database-url", default=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cmpe"))
    p.add_argument("--kg", default="build/w7-e10/cm-pharme-v2-fixture-kg.ttl")
    p.add_argument("--mapping", default="v2/data/mappings/ontology-rdb-mapping.csv")
    p.add_argument("--ontology-dir", default="v2/ontology/source/modules")
    p.add_argument("--sql-sparql-report", default="build/w7-e10/sql-sparql-equivalence.json")
    p.add_argument("--output", default="build/w7-e10/e10-semantic-consistency.json")
    p.add_argument("--summary", default="build/w7-e10/e10-semantic-consistency.md")
    return p.parse_args()


def ontology_graph(path: str) -> Graph:
    g = Graph()
    for p in sorted(Path(path).glob("*.ttl")):
        g.parse(p, format="turtle")
    return g


def iri(kind: str, public_id: str) -> URIRef:
    return URIRef(INST + kind + "/" + quote(str(public_id), safe=""))


def count_type(g: Graph, cls: URIRef) -> int:
    return len(set(g.subjects(RDF.type, cls)))


def count_typed_relation(g: Graph, cls: URIRef, prop: URIRef) -> int:
    nodes = set(g.subjects(RDF.type, cls))
    return sum(1 for s in nodes for _ in g.objects(s, prop))


def table_count(cur, table: str, where: str = "") -> int:
    sql = f"SELECT count(*) AS n FROM cmpe.{table}"
    if where:
        sql += " WHERE " + where
    cur.execute(sql)
    return int(cur.fetchone()["n"])


def main():
    a = parse_args()
    ont = ontology_graph(a.ontology_dir)
    kg = Graph().parse(a.kg, format="turtle")
    mapping_rows = list(csv.DictReader(Path(a.mapping).open(encoding="utf-8")))
    eq = json.loads(Path(a.sql_sparql_report).read_text(encoding="utf-8"))

    known_terms = (
        set(ont.subjects(RDF.type, OWL.Class))
        | set(ont.subjects(RDF.type, OWL.ObjectProperty))
        | set(ont.subjects(RDF.type, OWL.DatatypeProperty))
        | set(ont.subjects(RDF.type, RDFS.Datatype))
    )

    mapping_unknown_iris = sorted({r["ontology_iri"] for r in mapping_rows if r["ontology_iri"] and URIRef(r["ontology_iri"]) not in known_terms})
    mapping_status_counts = dict(sorted(Counter(r["mapping_status"] for r in mapping_rows).items()))
    exception_rows = [
        {
            "mapping_id": r["mapping_id"],
            "ontology_iri": r["ontology_iri"],
            "mapping_status": r["mapping_status"],
            "representation_note": r["representation_note"],
        }
        for r in mapping_rows if r["mapping_status"] != "direct"
    ]
    undocumented_exceptions = [r["mapping_id"] for r in mapping_rows if r["mapping_status"] != "direct" and not r["representation_note"].strip()]

    class_parity = []
    relation_parity = []
    roundtrip = []
    projection_rows = []
    missing_tables = []

    class_specs = [
        ("dataset", CMPE.Dataset, "dataset", "public_id"),
        ("dataset_release", CMPE.DatasetRelease, "dataset-release", "public_id"),
        ("source_record", CMPE.SourceRecord, "source-record", "source_hash"),
        ("transformation_run", CMPE.ProvenanceActivity, "provenance-activity", "public_id"),
        ("facility", CMPE.Facility, "facility", "public_id"),
        ("pharmaceutical_substance", CMPE.PharmaceuticalSubstance, "substance", "public_id"),
        ("medicinal_product", CMPE.MedicinalProduct, "product", "public_id"),
        ("product_presentation", CMPE.MedicinalProductPresentation, "presentation", "public_id"),
        ("identifier_scheme", CMPE.IdentifierScheme, "identifier-scheme", "public_id"),
        ("identifier_assignment", CMPE.IdentifierAssignment, "identifier-assignment", "public_id"),
        ("assertion", CMPE.Assertion, "assertion", "public_id"),
        ("evidence_support", CMPE.EvidenceSupport, "evidence-support", "public_id"),
        ("entity_match_assertion", CMPE.EntityMatchAssertion, "entity-match", "public_id"),
    ]

    with psycopg.connect(a.database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            mapped_tables = sorted({r["rdb_table"] for r in mapping_rows if r["rdb_table"]})
            for table in mapped_tables:
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='cmpe' AND table_name=%s) AS ok", (table,))
                if not bool(cur.fetchone()["ok"]):
                    missing_tables.append(table)

            for table, cls, kind, identity_col in class_specs:
                rdb_n = table_count(cur, table)
                kg_n = count_type(kg, cls)
                class_parity.append({"table": table, "class": str(cls), "rdb_count": rdb_n, "kg_count": kg_n, "passed": rdb_n == kg_n})
                cur.execute(f"SELECT {identity_col} AS identity FROM cmpe.{table} ORDER BY {identity_col}")
                for row in cur.fetchall():
                    node = iri(kind, row["identity"])
                    ok = (node, RDF.type, cls) in kg
                    roundtrip.append({"table": table, "identity": str(row["identity"]), "node": str(node), "passed": ok})

            geo_rdb = table_count(cur, "geography")
            geo_kg = count_type(kg, CMPE.AdministrativeRegion) + count_type(kg, CMPE.Country) + count_type(kg, CMPE.GeographicFeature)
            class_parity.append({"table": "geography", "class": "GeographicFeature|AdministrativeRegion|Country", "rdb_count": geo_rdb, "kg_count": geo_kg, "passed": geo_rdb == geo_kg})
            cur.execute("SELECT public_id, geography_type FROM cmpe.geography ORDER BY public_id")
            for row in cur.fetchall():
                cls = CMPE.AdministrativeRegion if row["geography_type"] == "administrative_region" else (CMPE.Country if row["geography_type"] == "country" else CMPE.GeographicFeature)
                node = iri("geography", row["public_id"])
                roundtrip.append({"table": "geography", "identity": row["public_id"], "node": str(node), "passed": (node, RDF.type, cls) in kg})

            relation_specs = [
                ("presentationOf", "SELECT count(*) AS n FROM cmpe.product_presentation", len(list(kg.triples((None, CMPE.presentationOf, None))))),
                ("hasActiveSubstance", "SELECT count(*) AS n FROM cmpe.medicinal_product WHERE primary_substance_id IS NOT NULL", len(list(kg.triples((None, CMPE.hasActiveSubstance, None))))),
                ("facilityLocatedIn", "SELECT count(*) AS n FROM cmpe.facility WHERE geography_id IS NOT NULL", len(list(kg.triples((None, CMPE.locatedIn, None))))),
                ("identifierScheme", "SELECT count(*) AS n FROM cmpe.identifier_assignment", len(list(kg.triples((None, CMPE.identifierScheme, None))))),
                ("identifierEntity", "SELECT count(*) AS n FROM cmpe.identifier_assignment", len(list(kg.triples((None, CMPE.identifierEntity, None))))),
                ("identifierLexicalValue", "SELECT count(*) AS n FROM cmpe.identifier_assignment", len(list(kg.triples((None, CMPE.identifierLexicalValue, None))))),
                ("evidenceRecord", "SELECT count(*) AS n FROM cmpe.evidence_support", len(list(kg.triples((None, CMPE.evidenceRecord, None))))),
                ("evidenceAssertion", "SELECT count(*) AS n FROM cmpe.evidence_support", len(list(kg.triples((None, CMPE.evidenceAssertion, None))))),
                ("entityMatchConfidence", "SELECT count(*) AS n FROM cmpe.entity_match_assertion", len(list(kg.triples((None, CMPE.hasMatchConfidence, None))))),
            ]
            for name, sql, kg_n in relation_specs:
                cur.execute(sql)
                rdb_n = int(cur.fetchone()["n"])
                relation_parity.append({"relation": name, "rdb_count": rdb_n, "kg_count": kg_n, "passed": rdb_n == kg_n})

            sr_with_run = table_count(cur, "source_record", "transformation_run_id IS NOT NULL")
            kg_sr_with_run = count_typed_relation(kg, CMPE.SourceRecord, PROV.wasGeneratedBy)
            relation_parity.append({"relation": "SourceRecord-prov:wasGeneratedBy", "rdb_count": sr_with_run, "kg_count": kg_sr_with_run, "passed": sr_with_run == kg_sr_with_run})

            cur.execute("SELECT public_id, patient_count, package_count, cost_bgn, cost_eur FROM cmpe.observation_result ORDER BY public_id")
            metric_specs = [("patients", "patient_count"), ("packages", "package_count"), ("cost-bgn", "cost_bgn"), ("cost-eur", "cost_eur")]
            expected_projection_total = 0
            observed_projection_total = 0
            for row in cur.fetchall():
                expected_nodes = []
                observed_nodes = []
                for suffix, field in metric_specs:
                    if row[field] is None:
                        continue
                    expected_projection_total += 1
                    node = iri("observation-result", str(row["public_id"]) + ":" + suffix)
                    expected_nodes.append(str(node))
                    ok = (node, RDF.type, CMPE.ReimbursementUtilisationObservationResult) in kg and any(True for _ in kg.objects(node, CMPE.measureNumericValue))
                    if ok:
                        observed_projection_total += 1
                        observed_nodes.append(str(node))
                projection_rows.append({
                    "rdb_observation_public_id": row["public_id"],
                    "expected_rdf_nodes": len(expected_nodes),
                    "observed_valid_rdf_nodes": len(observed_nodes),
                    "passed": len(expected_nodes) == len(observed_nodes),
                })

            rdb_observation_rows = table_count(cur, "observation_result")
            kg_observation_nodes = count_type(kg, CMPE.ReimbursementUtilisationObservationResult)

    class_failures = [x for x in class_parity if not x["passed"]]
    relation_failures = [x for x in relation_parity if not x["passed"]]
    roundtrip_failures = [x for x in roundtrip if not x["passed"]]
    projection_failures = [x for x in projection_rows if not x["passed"]]
    eq_pass = bool(eq.get("passed")) and eq.get("benchmarks_passed") == eq.get("benchmarks_total")

    mandatory_pass = not any([
        mapping_unknown_iris,
        missing_tables,
        undocumented_exceptions,
        class_failures,
        relation_failures,
        roundtrip_failures,
        projection_failures,
        not eq_pass,
        expected_projection_total != kg_observation_nodes,
    ])

    family_status = "PASS_WITH_WARNING" if mandatory_pass and exception_rows else ("PASS" if mandatory_pass else "FAIL")
    report = {
        "schema_version": 1,
        "mandatory_gate": "PASS" if mandatory_pass else "FAIL",
        "family_status": family_status,
        "scope": "Registered ontology↔RDB mappings, W6 reference realization, generated fixture KG and frozen SQL↔SPARQL benchmarks only.",
        "mapping_registry": {
            "rows": len(mapping_rows),
            "unknown_ontology_iris": mapping_unknown_iris,
            "missing_rdb_tables": missing_tables,
            "status_counts": mapping_status_counts,
            "documented_non_direct_exceptions": exception_rows,
            "undocumented_exceptions": undocumented_exceptions,
        },
        "class_cardinality_checks": class_parity,
        "class_cardinality_passed": sum(1 for x in class_parity if x["passed"]),
        "class_cardinality_total": len(class_parity),
        "relation_cardinality_checks": relation_parity,
        "relation_cardinality_passed": sum(1 for x in relation_parity if x["passed"]),
        "relation_cardinality_total": len(relation_parity),
        "roundtrip_identity_checks": {
            "passed": sum(1 for x in roundtrip if x["passed"]),
            "total": len(roundtrip),
            "failures": roundtrip_failures,
        },
        "one_to_many_projection": {
            "rdb_observation_rows": rdb_observation_rows,
            "expected_metric_nodes": expected_projection_total,
            "observed_metric_nodes": kg_observation_nodes,
            "row_checks_passed": sum(1 for x in projection_rows if x["passed"]),
            "row_checks_total": len(projection_rows),
            "failures": projection_failures,
            "interpretation": "A single relational reimbursement aggregate may project to multiple RDF ObservationResult nodes, one per non-null metric; equality of raw row counts is therefore not expected.",
        },
        "sql_sparql": {
            "passed": eq_pass,
            "benchmarks_passed": eq.get("benchmarks_passed"),
            "benchmarks_total": eq.get("benchmarks_total"),
            "boundary": eq.get("interpretation_boundary"),
        },
        "semantic_loss_exception_count": len(exception_rows),
        "warnings": [
            "Non-direct mappings are retained as explicit bounded/polymorphic/projection/deferred exceptions rather than reported as lossless direct equivalence."
        ] if exception_rows else [],
        "interpretation_boundary": "PASS establishes consistency for the audited registered mappings, reference fixture realization and frozen query benchmarks. It does not establish universal bidirectional or lossless equivalence for every ontology term, database field, RDF graph or query.",
    }

    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# W7-E10 Ontology↔RDB↔KG Semantic Consistency",
        "",
        f"- Mandatory gate: **{report['mandatory_gate']}**",
        f"- Family status: **{family_status}**",
        f"- Mapping registry: **{len(mapping_rows)} rows**; unknown ontology IRIs: **{len(mapping_unknown_iris)}**; missing mapped tables: **{len(missing_tables)}**",
        f"- Class/cardinality checks: **{report['class_cardinality_passed']}/{report['class_cardinality_total']}**",
        f"- Relation/cardinality checks: **{report['relation_cardinality_passed']}/{report['relation_cardinality_total']}**",
        f"- Deterministic identity round-trip checks: **{report['roundtrip_identity_checks']['passed']}/{report['roundtrip_identity_checks']['total']}**",
        f"- Relational observation aggregates: **{rdb_observation_rows}**",
        f"- Expected/observed RDF metric ObservationResults: **{expected_projection_total}/{kg_observation_nodes}**",
        f"- One-to-many row projection checks: **{report['one_to_many_projection']['row_checks_passed']}/{report['one_to_many_projection']['row_checks_total']}**",
        f"- SQL↔SPARQL frozen benchmarks: **{eq.get('benchmarks_passed')}/{eq.get('benchmarks_total')}**",
        f"- Explicit non-direct/semantic-loss mapping exceptions: **{len(exception_rows)}**",
        "",
        "## Boundary",
        report["interpretation_boundary"],
    ]
    Path(a.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    if not mandatory_pass:
        raise SystemExit("W7-E10 mandatory semantic-consistency gate failed; see report for preserved findings.")


if __name__ == "__main__":
    main()
