#!/usr/bin/env python3
"""Validate W6 RDB/KG traceability, provenance and SHACL constraints."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from pyshacl import validate

CMPE_NS = "https://w3id.org/cm-pharme/2.0/"
CMPE = Namespace(CMPE_NS)
SH = Namespace("http://www.w3.org/ns/shacl#")


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--database-url", default=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cmpe"))
    p.add_argument("--kg", default="build/w6/cm-pharme-v2-fixture-kg.ttl")
    p.add_argument("--mapping", default="v2/data/mappings/ontology-rdb-mapping.csv")
    p.add_argument("--ontology-dir", default="v2/ontology/source/modules")
    p.add_argument("--shapes", default="v2/ontology/shapes/cm-pharme-v2.shacl.ttl")
    p.add_argument("--manifest", default="v2/data/sources/source-manifest.json")
    p.add_argument("--report", default="build/w6/validation-report.json")
    return p.parse_args()


def ontology_graph(path: str) -> Graph:
    g = Graph()
    for p in sorted(Path(path).glob("*.ttl")):
        g.parse(p, format="turtle")
    return g


def main():
    a = args()
    ont = ontology_graph(a.ontology_dir)
    kg = Graph().parse(a.kg, format="turtle")
    shapes = Graph().parse(a.shapes, format="turtle")
    manifest = json.loads(Path(a.manifest).read_text(encoding="utf-8"))

    known_terms = set(ont.subjects(RDF.type, OWL.Class)) | set(ont.subjects(RDF.type, OWL.ObjectProperty)) | set(ont.subjects(RDF.type, OWL.DatatypeProperty)) | set(ont.subjects(RDF.type, RDFS.Datatype))
    mapping_rows = list(csv.DictReader(open(a.mapping, encoding="utf-8")))
    missing_mapping_iris = []
    for row in mapping_rows:
        iri = row["ontology_iri"]
        if iri and URIRef(iri) not in known_terms:
            missing_mapping_iris.append(iri)
    if missing_mapping_iris:
        raise SystemExit("Mapping registry references unknown ontology IRIs: " + ", ".join(sorted(set(missing_mapping_iris))))

    unknown_cmpe_terms = set()
    for s, p, o in kg:
        if isinstance(p, URIRef) and str(p).startswith(CMPE_NS) and p not in known_terms:
            unknown_cmpe_terms.add(str(p))
        if p == RDF.type and isinstance(o, URIRef) and str(o).startswith(CMPE_NS) and o not in known_terms:
            unknown_cmpe_terms.add(str(o))
    if unknown_cmpe_terms:
        raise SystemExit("KG uses CMPE terms absent from W5 ontology: " + ", ".join(sorted(unknown_cmpe_terms)))

    conforms, report_graph, report_text = validate(
        kg, shacl_graph=shapes, ont_graph=ont, inference="rdfs", meta_shacl=True,
        advanced=True, allow_infos=True, allow_warnings=True, abort_on_first=False
    )
    if not conforms:
        raise SystemExit("Generated W6 KG fails SHACL:\n" + str(report_text))

    checks = {}
    with psycopg.connect(a.database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            queries = {
                "observations_have_source_assertion": "SELECT count(*)=0 AS ok FROM cmpe.observation_result WHERE source_record_id IS NULL OR assertion_id IS NULL",
                "assertions_have_evidence": "SELECT count(*)=0 AS ok FROM cmpe.assertion a LEFT JOIN cmpe.evidence_support e ON e.assertion_id=a.assertion_id WHERE e.evidence_support_id IS NULL",
                "source_records_have_release": "SELECT count(*)=0 AS ok FROM cmpe.source_record WHERE dataset_release_id IS NULL",
                "geography_aliases_resolve": "SELECT count(*)=0 AS ok FROM cmpe.geography_alias WHERE geography_id IS NULL OR confidence IS NULL",
                "presentation_product_split": "SELECT count(*)>0 AS ok FROM cmpe.product_presentation pp JOIN cmpe.medicinal_product mp ON mp.medicinal_product_id=pp.medicinal_product_id WHERE pp.public_id<>mp.public_id",
                "facility_geography_split": "SELECT count(*)>0 AS ok FROM cmpe.facility f JOIN cmpe.geography g ON g.geography_id=f.geography_id WHERE f.public_id<>g.public_id",
                "cross_source_matches_present": "SELECT count(*)>0 AS ok FROM cmpe.entity_match_assertion WHERE status='accepted' AND confidence=1.0",
                "no_self_match": "SELECT count(*)=0 AS ok FROM cmpe.entity_match_assertion WHERE source_record_a_id=source_record_b_id",
            }
            for name, sql in queries.items():
                cur.execute(sql)
                checks[name] = bool(cur.fetchone()["ok"])
            cur.execute("SELECT count(*) AS n FROM cmpe.observation_result")
            observation_count = int(cur.fetchone()["n"])
            cur.execute("SELECT count(*) AS n FROM cmpe.source_record")
            source_record_count = int(cur.fetchone()["n"])
            cur.execute("SELECT count(*) AS n FROM cmpe.product_presentation")
            presentation_count = int(cur.fetchone()["n"])
            cur.execute("SELECT count(*) AS n FROM cmpe.facility")
            facility_count = int(cur.fetchone()["n"])

    if not all(checks.values()):
        failed = [k for k, v in checks.items() if not v]
        raise SystemExit("W6 relational checks failed: " + ", ".join(failed))

    held_out_names = {"ClinicalTrials.gov/AACT", "openFDA Drug Shortages", "reserved national EML sample"}
    manifest_held = set(manifest.get("held_out", []))
    if not held_out_names.issubset(manifest_held):
        raise SystemExit("Held-out manifest is incomplete")
    source_ids = {s["id"] for s in manifest["sources"]}
    if any(x in source_ids for x in held_out_names):
        raise SystemExit("Held-out source appears in W6 source execution list")

    report = {
        "schema_version": 1,
        "passed": True,
        "mapping_rows": len(mapping_rows),
        "mapping_ontology_iris_resolve": True,
        "unknown_cmpe_terms_in_kg": 0,
        "shacl_conforms": bool(conforms),
        "shacl_report_triples": len(report_graph),
        "relational_checks": checks,
        "counts": {
            "observations": observation_count,
            "source_records": source_record_count,
            "presentations": presentation_count,
            "facilities": facility_count,
            "kg_triples": len(kg)
        },
        "held_out_integrity": True,
        "full_external_dataset_ingestion_claimed": False,
        "interpretation_boundary": "PASS establishes W6 representation mechanics on schema-faithful fixtures, not full-dataset empirical validity or held-out generalizability."
    }
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
