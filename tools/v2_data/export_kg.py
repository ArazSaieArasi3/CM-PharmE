#!/usr/bin/env python3
"""Export the W6 reference database to a deterministic RDF ABox/KG."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote

import psycopg
from psycopg.rows import dict_row
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from rdflib.compare import to_canonical_graph
from rdflib.namespace import DCTERMS, XSD

CMPE = Namespace("https://w3id.org/cm-pharme/2.0/")
INST = "https://w3id.org/cm-pharme/2.0/instance/"
PROV = Namespace("http://www.w3.org/ns/prov#")


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--database-url", default=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cmpe"))
    p.add_argument("--output", default="build/w6/cm-pharme-v2-fixture-kg.ttl")
    p.add_argument("--manifest", default="build/w6/kg-manifest.json")
    return p.parse_args()


def iri(kind: str, public_id: str) -> URIRef:
    return URIRef(INST + kind + "/" + quote(public_id, safe=""))


def canonical_bytes(g: Graph) -> bytes:
    cg = to_canonical_graph(g)
    lines = sorted(f"{s.n3()} {p.n3()} {o.n3()} .\n" for s, p, o in cg)
    return "".join(lines).encode("utf-8")


def add_label(g: Graph, node: URIRef, label: str | None):
    if label:
        g.add((node, RDFS.label, Literal(label, lang="en")))


def main():
    a = args()
    g = Graph()
    g.bind("cmpe", CMPE)
    g.bind("prov", PROV)
    g.bind("dct", DCTERMS)

    with psycopg.connect(a.database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM cmpe.dataset ORDER BY public_id")
            for r in cur.fetchall():
                n = iri("dataset", r["public_id"])
                g.add((n, RDF.type, CMPE.Dataset))
                add_label(g, n, r["title"])
                if r["doi"]:
                    g.add((n, DCTERMS.identifier, Literal(r["doi"])))

            cur.execute("""SELECT dr.*, d.public_id AS dataset_public FROM cmpe.dataset_release dr
                           JOIN cmpe.dataset d ON d.dataset_id=dr.dataset_id ORDER BY dr.public_id""")
            for r in cur.fetchall():
                d = iri("dataset", r["dataset_public"])
                n = iri("dataset-release", r["public_id"])
                g.add((n, RDF.type, CMPE.DatasetRelease))
                g.add((d, CMPE.hasDatasetRelease, n))
                if r["source_filename"]:
                    g.add((n, DCTERMS.identifier, Literal(r["source_filename"])))

            cur.execute("SELECT * FROM cmpe.transformation_run ORDER BY public_id")
            for r in cur.fetchall():
                n = iri("provenance-activity", r["public_id"])
                g.add((n, RDF.type, CMPE.ProvenanceActivity))
                add_label(g, n, f"{r['adapter_name']} {r['adapter_version']}")

            cur.execute("""SELECT sr.*, dr.public_id AS release_public, tr.public_id AS run_public
                           FROM cmpe.source_record sr
                           JOIN cmpe.dataset_release dr ON dr.dataset_release_id=sr.dataset_release_id
                           LEFT JOIN cmpe.transformation_run tr ON tr.transformation_run_id=sr.transformation_run_id
                           ORDER BY sr.source_record_id""")
            source_nodes = {}
            for r in cur.fetchall():
                n = iri("source-record", r["source_hash"])
                source_nodes[r["source_record_id"]] = n
                release = iri("dataset-release", r["release_public"])
                g.add((n, RDF.type, CMPE.SourceRecord))
                g.add((release, CMPE.containsSourceRecord, n))
                g.add((n, DCTERMS.identifier, Literal(r["source_hash"])))
                if r["run_public"]:
                    g.add((n, PROV.wasGeneratedBy, iri("provenance-activity", r["run_public"])))

            cur.execute("SELECT * FROM cmpe.geography ORDER BY public_id")
            geo_nodes = {}
            for r in cur.fetchall():
                n = iri("geography", r["public_id"])
                geo_nodes[r["geography_id"]] = n
                cls = CMPE.AdministrativeRegion if r["geography_type"] == "administrative_region" else (CMPE.Country if r["geography_type"] == "country" else CMPE.GeographicFeature)
                g.add((n, RDF.type, cls))
                add_label(g, n, r["canonical_name"])
                if r["geonames_id"] is not None:
                    g.add((n, DCTERMS.identifier, Literal(f"GeoNames:{r['geonames_id']}")))

            cur.execute("SELECT * FROM cmpe.facility ORDER BY public_id")
            facility_nodes = {}
            for r in cur.fetchall():
                n = iri("facility", r["public_id"])
                facility_nodes[r["facility_id"]] = n
                g.add((n, RDF.type, CMPE.Facility))
                add_label(g, n, r["preferred_name"])
                if r["geography_id"]:
                    g.add((n, CMPE.locatedIn, geo_nodes[r["geography_id"]]))

            cur.execute("SELECT * FROM cmpe.pharmaceutical_substance ORDER BY public_id")
            substance_nodes = {}
            for r in cur.fetchall():
                n = iri("substance", r["public_id"])
                substance_nodes[r["substance_id"]] = n
                g.add((n, RDF.type, CMPE.PharmaceuticalSubstance))
                add_label(g, n, r["preferred_name"])

            cur.execute("SELECT * FROM cmpe.medicinal_product ORDER BY public_id")
            product_nodes = {}
            for r in cur.fetchall():
                n = iri("product", r["public_id"])
                product_nodes[r["medicinal_product_id"]] = n
                g.add((n, RDF.type, CMPE.MedicinalProduct))
                add_label(g, n, r["preferred_name"])
                if r["primary_substance_id"]:
                    g.add((n, CMPE.hasActiveSubstance, substance_nodes[r["primary_substance_id"]]))

            cur.execute("SELECT * FROM cmpe.product_presentation ORDER BY public_id")
            presentation_nodes = {}
            for r in cur.fetchall():
                n = iri("presentation", r["public_id"])
                presentation_nodes[r["product_presentation_id"]] = n
                g.add((n, RDF.type, CMPE.MedicinalProductPresentation))
                g.add((n, CMPE.presentationOf, product_nodes[r["medicinal_product_id"]]))
                add_label(g, n, r["public_id"])

            cur.execute("SELECT * FROM cmpe.identifier_scheme ORDER BY public_id")
            scheme_nodes = {}
            for r in cur.fetchall():
                n = iri("identifier-scheme", r["public_id"])
                scheme_nodes[r["identifier_scheme_id"]] = n
                g.add((n, RDF.type, CMPE.IdentifierScheme))
                add_label(g, n, r["scheme_name"])

            cur.execute("SELECT * FROM cmpe.identifier_assignment ORDER BY public_id")
            for r in cur.fetchall():
                n = iri("identifier-assignment", r["public_id"])
                g.add((n, RDF.type, CMPE.IdentifierAssignment))
                g.add((n, CMPE.identifierScheme, scheme_nodes[r["identifier_scheme_id"]]))
                g.add((n, CMPE.identifierLexicalValue, Literal(r["lexical_value"], datatype=XSD.string)))
                entity_type = r["entity_type"]
                entity_public = r["entity_public_id"]
                target = iri({"product_presentation":"presentation","facility":"facility","medicinal_product":"product","substance":"substance","geography":"geography","organization":"organization"}[entity_type], entity_public)
                g.add((n, CMPE.identifierEntity, target))
                if r["source_record_id"]:
                    g.add((n, PROV.wasDerivedFrom, source_nodes[r["source_record_id"]]))

            cur.execute("""SELECT o.*, pp.public_id AS presentation_public, sr.source_hash,
                                  tr.public_id AS run_public
                           FROM cmpe.observation_result o
                           LEFT JOIN cmpe.product_presentation pp ON pp.product_presentation_id=o.product_presentation_id
                           JOIN cmpe.source_record sr ON sr.source_record_id=o.source_record_id
                           LEFT JOIN cmpe.transformation_run tr ON tr.transformation_run_id=sr.transformation_run_id
                           ORDER BY o.public_id""")
            observation_base_nodes = {}
            metrics = [
                ("patients", "patient count", "patient_count"),
                ("packages", "package count", "package_count"),
                ("cost-bgn", "BGN", "cost_bgn"),
                ("cost-eur", "EUR", "cost_eur"),
            ]
            for r in cur.fetchall():
                base = r["public_id"]
                observation_base_nodes[r["assertion_id"]] = []
                for suffix, unit, field in metrics:
                    if r[field] is None:
                        continue
                    n = iri("observation-result", base + ":" + suffix)
                    observation_base_nodes[r["assertion_id"]].append(n)
                    g.add((n, RDF.type, CMPE.ReimbursementUtilisationObservationResult))
                    if r["presentation_public"]:
                        g.add((n, CMPE.observationResultAbout, iri("presentation", r["presentation_public"])))
                    g.add((n, CMPE.measureNumericValue, Literal(r[field], datatype=XSD.decimal)))
                    g.add((n, CMPE.measureUnitLabel, Literal(unit)))
                    g.add((n, CMPE.validFrom, Literal(str(r["reporting_period"]) + "T00:00:00+00:00", datatype=XSD.dateTime)))
                    if r["geography_id"]:
                        g.add((n, DCTERMS.spatial, geo_nodes[r["geography_id"]]))
                    if r["facility_id"]:
                        g.add((n, DCTERMS.relation, facility_nodes[r["facility_id"]]))
                    g.add((n, PROV.wasDerivedFrom, source_nodes[r["source_record_id"]]))
                    if r["run_public"]:
                        g.add((n, PROV.wasGeneratedBy, iri("provenance-activity", r["run_public"])))

            cur.execute("SELECT * FROM cmpe.assertion ORDER BY public_id")
            assertion_nodes = {}
            for r in cur.fetchall():
                n = iri("assertion", r["public_id"])
                assertion_nodes[r["assertion_id"]] = n
                g.add((n, RDF.type, CMPE.Assertion))
                for obs in observation_base_nodes.get(r["assertion_id"], []):
                    g.add((n, RDFS.seeAlso, obs))

            cur.execute("SELECT * FROM cmpe.evidence_support ORDER BY public_id")
            for r in cur.fetchall():
                n = iri("evidence-support", r["public_id"])
                g.add((n, RDF.type, CMPE.EvidenceSupport))
                g.add((n, CMPE.evidenceRecord, source_nodes[r["source_record_id"]]))
                g.add((n, CMPE.evidenceAssertion, assertion_nodes[r["assertion_id"]]))

            cur.execute("SELECT * FROM cmpe.entity_match_assertion ORDER BY public_id")
            for r in cur.fetchall():
                n = iri("entity-match", r["public_id"])
                q = iri("match-confidence", r["public_id"])
                g.add((n, RDF.type, CMPE.EntityMatchAssertion))
                g.add((n, CMPE.matchSubject, source_nodes[r["source_record_a_id"]]))
                g.add((n, CMPE.matchObject, source_nodes[r["source_record_b_id"]]))
                g.add((n, CMPE.hasMatchConfidence, q))
                g.add((q, RDF.type, CMPE.MatchConfidence))
                g.add((q, RDF.value, Literal(r["confidence"], datatype=XSD.decimal)))
                g.add((n, RDFS.seeAlso, iri("presentation", r["matched_public_id"])))

    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(out, format="turtle")
    canonical = canonical_bytes(g)
    nt = out.with_suffix(".nt")
    nt.write_bytes(canonical)
    manifest = {
        "schema_version": 1,
        "graph_kind": "W6 schema-faithful fixture ABox",
        "triple_count": len(g),
        "canonical_ntriples_sha256": hashlib.sha256(canonical).hexdigest(),
        "ontology_namespace": str(CMPE),
        "instance_namespace": INST,
        "full_external_dataset_ingestion": False,
        "held_out_used": False,
    }
    Path(a.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
