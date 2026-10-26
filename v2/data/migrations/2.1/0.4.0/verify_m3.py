#!/usr/bin/env python3
"""Bounded FR-02 PostgreSQL/RDF projection with documentary and fixture scopes."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from pyshacl import validate
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.namespace import DCTERMS, XSD
from owlready2 import World, sync_reasoner, VERSION as OWLREADY_VERSION
from owlready2.entity import OwlReadyInconsistentOntologyError

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))
from verify_source import verify as verify_source  # noqa: E402

spec = importlib.util.spec_from_file_location("m3_m1", HERE.parent / "0.2.0/verify_m1.py")
m1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m1)
C = Namespace("https://w3id.org/cm-pharme/2.1/")
PROV = Namespace("http://www.w3.org/ns/prov#")
M3 = Namespace("urn:cmpe:rdb-m3:")
SOURCE = json.loads((HERE / "source-witness.json").read_text())
ORACLES = json.loads((HERE / "fixed-oracles.json").read_text())
EXPECTED = ORACLES["expected"]
DOC_ORG = SOURCE["manufacturer"]["public_id"]
DOC_PRODUCT = SOURCE["product"]["public_id"]
FOR_ORG = SOURCE["manufactured_for"]["public_id"]
NAME_ORG = "m3-fixture-org:name-only"
SYN_ORG = "m3-fixture-org:a"
SYN_PRODUCTS = ["m3-fixture-product:a", "m3-fixture-product:b"]

COLUMNS = ["responsibility_id", "organization_id", "product_id", "claim_kind", "valid_from", "valid_to",
           "release_id", "row_number", "source_hash", "run_id", "assertion_id", "evidence_id"]
SQL = """
SELECT r.public_id AS responsibility_id, o.public_id AS organization_id,
       p.public_id AS product_id, r.claim_kind, r.valid_from, r.valid_to,
       dr.public_id AS release_id, sr.row_number, sr.source_hash,
       tr.public_id AS run_id, a.public_id AS assertion_id, es.public_id AS evidence_id,
       sr.raw_key
FROM cmpe.manufacturing_responsibility_21 r
JOIN cmpe.organization o USING (organization_id)
JOIN cmpe.medicinal_product p USING (medicinal_product_id)
JOIN cmpe.source_record sr ON sr.source_record_id=r.source_record_id
JOIN cmpe.dataset_release dr USING (dataset_release_id)
JOIN cmpe.transformation_run tr USING (transformation_run_id)
JOIN cmpe.assertion a ON a.assertion_id=r.assertion_id
JOIN cmpe.evidence_support es ON es.evidence_support_id=r.evidence_support_id
ORDER BY r.public_id
"""
SPARQL = """
PREFIX c: <https://w3id.org/cm-pharme/2.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?responsibility_id ?organization_id ?product_id ?claim_kind ?valid_from ?valid_to
       ?release_id ?row_number ?source_hash ?run_id ?assertion_id ?evidence_id WHERE {
  ?r a c:ManufacturingResponsibility ; dct:identifier ?responsibility_id ; dct:type ?claim_kind ;
     c:manufacturingResponsibilityHolder ?org ; c:manufacturingResponsibilityCounterpart ?product ;
     prov:wasDerivedFrom ?sr ; dct:relation ?evidence .
  ?org a c:Organization, c:ManufacturerRole ; dct:identifier ?organization_id .
  ?product a c:MedicinalProduct, c:ManufacturingResponsibilitySubjectRole ; dct:identifier ?product_id .
  ?release c:containsSourceRecord ?sr ; dct:identifier ?release_id .
  ?sr rdf:value ?row_number ; prov:value ?source_hash ; prov:wasGeneratedBy ?run .
  ?run dct:identifier ?run_id .
  ?evidence dct:identifier ?evidence_id ; dct:relation ?assertion .
  ?assertion dct:identifier ?assertion_id .
  OPTIONAL { ?r c:validFrom ?from . BIND(SUBSTR(STR(?from),1,10) AS ?valid_from) }
  OPTIONAL { ?r c:validTo ?to . BIND(SUBSTR(STR(?to),1,10) AS ?valid_to) }
} ORDER BY ?responsibility_id
"""


def source_records():
    return [
        {"source_kind": "documentary_attribution", "document_id": SOURCE["document_id"],
         "source_url": SOURCE["source_url"], "pdf_sha256": SOURCE["pdf_sha256"],
         "page": SOURCE["pdf_page_1_based"], "revision": SOURCE["revision"],
         "manufacturer_public_id": DOC_ORG, "product_public_id": DOC_PRODUCT,
         "excerpt_sha256": SOURCE["excerpt_sha256"]},
        {"source_kind": "synthetic_fixture", "fixture_only": True,
         "source_url": "urn:cmpe:rdb-m3:synthetic-fixture", "case": "role-contexts-only"},
    ]


def example_rows():
    raw = source_records()
    contexts = [
        ("m3-doc-responsibility:FDA-125514-S186", DOC_ORG, DOC_PRODUCT, 0, None, None),
        ("m3-fixture-responsibility:1", SYN_ORG, SYN_PRODUCTS[0], 1, "2026-01-01", "2026-03-31"),
        ("m3-fixture-responsibility:2", SYN_ORG, SYN_PRODUCTS[0], 1, "2026-04-01", None),
        ("m3-fixture-responsibility:3", SYN_ORG, SYN_PRODUCTS[1], 1, None, None),
    ]
    rows = []
    for i, (key, org, product, src, start, end) in enumerate(contexts, 1):
        rows.append({"responsibility_id": key, "organization_id": org, "product_id": product,
                     "claim_kind": raw[src]["source_kind"], "valid_from": start, "valid_to": end,
                     "release_id": "m3-release:" + (SOURCE["document_id"] if src == 0 else "synthetic"),
                     "row_number": 1, "source_hash": m1.sha(m1.compact(raw[src])),
                     "run_id": "m3-run:reviewed-extraction-0.4.0",
                     "assertion_id": f"m3-assertion:{i}", "evidence_id": f"m3-evidence:{i}",
                     "raw_key": raw[src]})
    return rows


def export(rows):
    g = Graph()
    for prefix, ns in [("c", C), ("prov", PROV), ("dct", DCTERMS)]:
        g.bind(prefix, ns)
    for row in rows:
        rel = m1.node("manufacturing-responsibility", row["responsibility_id"])
        org = m1.node("organization", row["organization_id"])
        product = m1.node("medicinal-product", row["product_id"])
        source = m1.node("source-record", m1.source_key({"release_public": row["release_id"],
                              "row_number": row["row_number"], "source_hash": row["source_hash"]}))
        release = m1.node("dataset-release", row["release_id"])
        run = m1.node("provenance-activity", row["run_id"])
        assertion = m1.node("assertion", row["assertion_id"])
        evidence = m1.node("evidence-support", row["evidence_id"])
        for node, kind, key in [(rel, C.ManufacturingResponsibility, row["responsibility_id"]),
                                (org, C.Organization, row["organization_id"]),
                                (product, C.MedicinalProduct, row["product_id"]),
                                (release, C.DatasetRelease, row["release_id"]),
                                (run, C.ProvenanceActivity, row["run_id"]),
                                (assertion, C.Assertion, row["assertion_id"])]:
            g.add((node, RDF.type, kind)); g.add((node, DCTERMS.identifier, Literal(key)))
        g.add((org, RDF.type, C.ManufacturerRole))
        g.add((product, RDF.type, C.ManufacturingResponsibilitySubjectRole))
        g.add((rel, C.manufacturingResponsibilityHolder, org))
        g.add((rel, C.manufacturingResponsibilityCounterpart, product))
        g.add((rel, DCTERMS.type, Literal(row["claim_kind"])))
        for field, prop in [("valid_from", C.validFrom), ("valid_to", C.validTo)]:
            if row[field] is not None:
                g.add((rel, prop, Literal(str(row[field]) + "T00:00:00Z", datatype=XSD.dateTime)))
        g.add((rel, PROV.wasDerivedFrom, source)); g.add((rel, DCTERMS.relation, evidence))
        g.add((source, RDF.type, C.SourceRecord))
        g.add((source, RDF.value, Literal(row["row_number"], datatype=XSD.integer)))
        g.add((source, PROV.value, Literal(row["source_hash"])))
        g.add((source, DCTERMS.source, URIRef(row["raw_key"]["source_url"])))
        g.add((source, DCTERMS.type, Literal(row["claim_kind"])))
        g.add((source, DCTERMS.description, Literal(json.dumps(row["raw_key"], sort_keys=True))))
        g.add((release, C.containsSourceRecord, source)); g.add((source, PROV.wasGeneratedBy, run))
        # M025's global EvidenceSupport role interpretation is deliberately not promoted.
        g.add((evidence, DCTERMS.identifier, Literal(row["evidence_id"])))
        g.add((evidence, PROV.wasDerivedFrom, source)); g.add((evidence, DCTERMS.relation, assertion))
        g.add((assertion, RDF.subject, org)); g.add((assertion, RDF.object, product))
        g.add((assertion, RDF.predicate, M3.documented_manufacturer))
    for key, label in [(FOR_ORG, SOURCE["manufactured_for"]["name"]), (NAME_ORG, "Manufacturer Limited")]:
        org = m1.node("organization", key)
        g.add((org, RDF.type, C.Organization)); g.add((org, DCTERMS.identifier, Literal(key)))
        g.add((org, RDFS.label, Literal(label)))
    return g


def shacl_checks(g, ontology, shapes):
    def check(data):
        ok, report, _ = validate(data, shacl_graph=shapes, ont_graph=ontology,
                                 inference="none", advanced=True, meta_shacl=True)
        return bool(ok), len(list(report.subjects(RDF.type, Namespace("http://www.w3.org/ns/shacl#").ValidationResult)))
    rel = m1.node("manufacturing-responsibility", "m3-doc-responsibility:FDA-125514-S186")
    org, product = m1.node("organization", DOC_ORG), m1.node("medicinal-product", DOC_PRODUCT)
    base = g - Graph()
    mutations = {
        "missing_holder": ([(rel, C.manufacturingResponsibilityHolder, org)], []),
        "missing_product": ([(rel, C.manufacturingResponsibilityCounterpart, product)], []),
        "two_holders": ([], [(rel, C.manufacturingResponsibilityHolder, m1.node("organization", SYN_ORG))]),
        "two_products": ([], [(rel, C.manufacturingResponsibilityCounterpart, m1.node("medicinal-product", SYN_PRODUCTS[0]))]),
        "wrong_product_kind": ([(product, RDF.type, C.ManufacturingResponsibilitySubjectRole),
                                (product, RDF.type, C.MedicinalProduct)], [(product, RDF.type, C.Facility)]),
        "missing_source": (list(g.triples((rel, PROV.wasDerivedFrom, None))), []),
        "missing_evidence": (list(g.triples((rel, DCTERMS.relation, None))), []),
    }
    results = {"positive": check(base)[0]}
    details = {}
    for name, (remove, add) in mutations.items():
        data = base - Graph()
        for triple in remove: data.remove(triple)
        for triple in add: data.add(triple)
        results[name], details[name] = check(data)
    for name, key in [("name_only", NAME_ORG), ("manufactured_for_only", FOR_ORG)]:
        data = Graph(); n = m1.node("organization", key)
        for triple in g.triples((n, None, None)): data.add(triple)
        results[name] = check(data)[0]
    bare = Graph(); bare.add((m1.node("organization", NAME_ORG), RDF.type, C.ManufacturerRole))
    results["bare_role"] = check(bare)[0]
    if results != EXPECTED["shacl"]:
        raise AssertionError(f"SHACL differed from frozen oracles: {results}")
    # Supplemental alignment mutation is separate from the frozen core denominator.
    mismatch = base - Graph()
    assertion = m1.node("assertion", "m3-assertion:1")
    mismatch.set((assertion, RDF.subject, m1.node("organization", FOR_ORG)))
    mismatch_ok, _ = check(mismatch)
    if mismatch_ok: raise AssertionError("Misaligned RDF assertion was admitted")
    return {"expected": EXPECTED["shacl"], "observed": results, "all_expected_met": True,
            "negative_violation_counts": details, "supplemental_misaligned_assertion_rejected": True,
            "inference": "none; admission completeness is separate from OWL open-world reasoning"}


def consistent(ontology, abox):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "m3.rdf"
        (ontology + abox).serialize(path, format="xml")
        world = World(); world.get_ontology(path.as_uri()).load()
        try:
            sync_reasoner(world, debug=0)
            return True
        except OwlReadyInconsistentOntologyError:
            return False
        finally:
            world.close()


def reasoner_checks(g, ontology):
    rel = m1.node("manufacturing-responsibility", "m3-doc-responsibility:FDA-125514-S186")
    org, product = m1.node("organization", DOC_ORG), m1.node("medicinal-product", DOC_PRODUCT)
    missing = g - Graph(); missing.remove((rel, C.manufacturingResponsibilityCounterpart, product))
    dual = g - Graph(); other = m1.node("organization", SYN_ORG)
    dual.add((rel, C.manufacturingResponsibilityHolder, other)); dual.add((org, OWL.differentFrom, other))
    collapsed = g - Graph(); collapsed.add((org, OWL.sameAs, product))
    result = {"positive": consistent(ontology, g), "missing_product_open_world": consistent(ontology, missing),
              "two_distinct_holders": consistent(ontology, dual),
              "organization_product_identity_collapse": consistent(ontology, collapsed)}
    for name, key in [("name_only_not_manufacturer_countermodel", NAME_ORG),
                      ("manufactured_for_not_manufacturer_countermodel", FOR_ORG)]:
        data = Graph(); n = m1.node("organization", key)
        for triple in g.triples((n, None, None)): data.add(triple)
        complement = URIRef("urn:cmpe:rdb-m3:NonManufacturerCountermodel")
        data.add((complement, RDF.type, OWL.Class)); data.add((complement, OWL.complementOf, C.ManufacturerRole))
        data.add((n, RDF.type, complement))
        result[name] = consistent(ontology, data)
    if result != EXPECTED["hermit"]:
        raise AssertionError(f"HermiT differed from frozen oracles: {result}")
    return {"expected": EXPECTED["hermit"], "observed": result, "all_expected_met": True}


def native_check(config):
    native = json.loads((ROOT / config["candidate_native"]).read_text())
    elements = {}
    def walk(x):
        if isinstance(x, dict):
            if x.get("id"): elements[x["id"]] = x
            for value in x.values(): walk(value)
        elif isinstance(x, list):
            for value in x: walk(value)
    walk(native)
    ids = ["Organization", "MedicinalProduct", "ManufacturerRole", "ManufacturingResponsibility",
           "ManufacturingResponsibilitySubjectRole", "rel-manufacturingResponsibilityHolder",
           "rel-manufacturingResponsibilityCounterpart"]
    assert all(key in elements for key in ids)
    ends = {}
    for name, kind in [("manufacturingResponsibilityHolder", "ManufacturerRole"),
                       ("manufacturingResponsibilityCounterpart", "ManufacturingResponsibilitySubjectRole")]:
        node = elements["end-" + name + "-target"]
        assert node["propertyType"] == kind and node["cardinality"] == "1"
        assert elements["rel-" + name]["stereotype"] == "mediation"
        ends[name] = {"target": kind, "cardinality": node["cardinality"], "stereotype": "mediation"}
    return {"anchors": ids, "ends": ends, "boundary": "Existing native anchors checked; no new native model or full anti-pattern conformance claim."}


def rdf_checks(rows, out, config):
    g = export(rows)
    ontology = Graph().parse(ROOT / config["candidate_ontology"])
    shapes = Graph().parse(ROOT / config["candidate_shapes"]) + Graph().parse(HERE / "admission.ttl")
    nt = m1.canonical(g); (out / "manufacturer-21.nt").write_bytes(nt)
    g.serialize(out / "manufacturer-21.ttl", format="turtle")
    reparsed = Graph().parse(out / "manufacturer-21.nt", format="nt")
    assert m1.canonical(reparsed) == nt
    query = reparsed.query(SPARQL)
    answers = [{str(v): r[i] for i, v in enumerate(query.vars)} for r in query]
    normalized = m1.normalize_rows(answers, COLUMNS)
    assert len(normalized) == EXPECTED["admitted_rows"]
    documentary = [r for r in answers if str(r["claim_kind"]) == "documentary_attribution"]
    assert len(documentary) == EXPECTED["documentary_rows"]
    assert str(documentary[0]["organization_id"]) == EXPECTED["source_positive_holder"]
    assert str(documentary[0]["product_id"]) == EXPECTED["source_positive_product"]
    assert documentary[0]["valid_from"] is None and documentary[0]["valid_to"] is None
    assert sum(str(r["claim_kind"]) == "synthetic_fixture" for r in answers) == EXPECTED["synthetic_rows"]
    for key in [FOR_ORG, NAME_ORG]:
        assert not [r for r in answers if str(r["organization_id"]) == key]
        assert (m1.node("organization", key), RDF.type, C.ManufacturerRole) not in g
    for row in rows:
        assert m1.sha(m1.compact(row["raw_key"])) == row["source_hash"]
    return {"rdf_roundtrip": True, "graph_sha256": m1.sha(nt), "graph_triples": len(g),
            "query_rows": normalized, "documentary_rows": len(documentary), "synthetic_rows": 3,
            "name_only_contexts": 0, "manufactured_for_contexts": 0,
            "source_record_hashes_preserved": True, "shacl": shacl_checks(g, ontology, shapes),
            "hermit": reasoner_checks(g, ontology), "native": native_check(config)}


def rejected(cur, query, params, expected):
    cur.execute("SAVEPOINT m3_negative")
    try:
        cur.execute(query, params)
    except psycopg.Error as error:
        cur.execute("ROLLBACK TO SAVEPOINT m3_negative"); cur.execute("RELEASE SAVEPOINT m3_negative")
        if error.sqlstate != expected:
            raise AssertionError(f"Expected SQLSTATE {expected}; got {error.sqlstate}") from error
        return error.sqlstate
    cur.execute("ROLLBACK TO SAVEPOINT m3_negative"); cur.execute("RELEASE SAVEPOINT m3_negative")
    raise AssertionError("Invalid M3 row was admitted")


def seed(url):
    rows = example_rows()
    with psycopg.connect(url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            # Negative explicit primary keys do not advance existing W6 sequences.
            for table, key in [("organization", "organization_id"), ("medicinal_product", "medicinal_product_id"),
                               ("dataset", "dataset_id"), ("dataset_release", "dataset_release_id"),
                               ("transformation_run", "transformation_run_id"), ("source_record", "source_record_id"),
                               ("assertion", "assertion_id"), ("evidence_support", "evidence_support_id")]:
                cur.execute(f"SELECT count(*) AS n FROM cmpe.{table} WHERE {key} BETWEEN -320100 AND -320001")
                if cur.fetchone()["n"]: raise AssertionError("Reserved M3 fixture IDs already used")
            cur.execute((HERE / "migration.sql").read_text())
            orgs = {DOC_ORG: -320001, FOR_ORG: -320002, NAME_ORG: -320003, SYN_ORG: -320004}
            for key, pk in orgs.items():
                label = (SOURCE["manufacturer"]["name"] if key == DOC_ORG else
                         SOURCE["manufactured_for"]["name"] if key == FOR_ORG else
                         "Manufacturer Limited" if key == NAME_ORG else "Synthetic Organization A")
                cur.execute("INSERT INTO cmpe.organization(organization_id,public_id,preferred_name) VALUES (%s,%s,%s)", (pk,key,label))
            products = {DOC_PRODUCT: -320001, SYN_PRODUCTS[0]: -320002, SYN_PRODUCTS[1]: -320003}
            for key, pk in products.items():
                cur.execute("INSERT INTO cmpe.medicinal_product(medicinal_product_id,public_id,preferred_name) VALUES (%s,%s,%s)",
                            (pk,key,SOURCE["product"]["name"] if key == DOC_PRODUCT else key))
            cur.execute("INSERT INTO cmpe.transformation_run(transformation_run_id,public_id,adapter_name,adapter_version,status) VALUES (-320001,%s,'reviewed-documentary-extraction','0.4.0','completed')", (rows[0]["run_id"],))
            for src in [0,1]:
                row = rows[0 if src == 0 else 1]; pk = -320001-src
                cur.execute("INSERT INTO cmpe.dataset(dataset_id,public_id,title,source_role) VALUES (%s,%s,%s,%s)",
                            (pk,f"m3-dataset:{src}","FDA reviewed attribution" if src == 0 else "M3 synthetic fixtures",'authoritative' if src == 0 else 'fixture'))
                cur.execute("INSERT INTO cmpe.dataset_release(dataset_release_id,dataset_id,public_id,release_label,source_filename) VALUES (%s,%s,%s,%s,%s)",
                            (pk,pk,row["release_id"],SOURCE["revision"] if src == 0 else "synthetic",SOURCE["document_id"] if src == 0 else "synthetic-record"))
                cur.execute("INSERT INTO cmpe.source_record(source_record_id,dataset_release_id,transformation_run_id,row_number,source_hash,raw_key) VALUES (%s,%s,-320001,1,%s,%s::jsonb)",
                            (pk,pk,row["source_hash"],json.dumps(row["raw_key"])))
            insert = """INSERT INTO cmpe.manufacturing_responsibility_21
                (public_id,organization_id,medicinal_product_id,source_record_id,assertion_id,evidence_support_id,claim_kind,valid_from,valid_to)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            params = []
            for i,row in enumerate(rows,1):
                pk = -320000-i; src = -320001 if i == 1 else -320002
                cur.execute("INSERT INTO cmpe.assertion(assertion_id,public_id,assertion_type,subject_public_id,predicate_key,object_public_id) VALUES (%s,%s,%s,%s,'documented_manufacturer',%s)",
                            (pk,row["assertion_id"],row["claim_kind"],row["organization_id"],row["product_id"]))
                cur.execute("INSERT INTO cmpe.evidence_support(evidence_support_id,public_id,source_record_id,assertion_id) VALUES (%s,%s,%s,%s)",
                            (pk,row["evidence_id"],src,pk))
                values = (row["responsibility_id"],orgs[row["organization_id"]],products[row["product_id"]],src,pk,pk,row["claim_kind"],row["valid_from"],row["valid_to"])
                cur.execute(insert,values); params.append(values)
            # Independent negative statement: commissioned-for does not admit a manufacturer.
            cur.execute("INSERT INTO cmpe.assertion(assertion_id,public_id,assertion_type,subject_public_id,predicate_key,object_public_id) VALUES (-320099,'m3-assertion:for','documentary_attribution',%s,'documented_manufactured_for',%s)", (FOR_ORG,DOC_PRODUCT))
            cur.execute("INSERT INTO cmpe.evidence_support(evidence_support_id,public_id,source_record_id,assertion_id) VALUES (-320099,'m3-evidence:for',-320001,-320099)")
            changes = {"missing_holder":{1:None},"missing_product":{2:None},
                       "wrong_holder_fk":{1:-999999999},"wrong_product_fk":{2:-999999999},
                       "missing_source":{3:None},"wrong_source_fk":{3:-999999999},
                       "duplicate_public_id":{0:params[0][0]},"reversed_interval":{7:"2026-04-01",8:"2026-03-31"},
                       "mismatched_evidence":{5:-320002},"duplicate_source_assertion":{},
                       "manufactured_for_as_manufacturer":{1:orgs[FOR_ORG],4:-320099,5:-320099}}
            results = {}
            for name, updates in changes.items():
                values = list(params[0]); values[0] = "m3-invalid:"+name
                # Most probes use a fresh assertion/evidence so uniqueness cannot mask their target.
                if name not in {"duplicate_public_id","duplicate_source_assertion"}:
                    values[4] = -320099; values[5] = -320099
                    # Only FK/NOT NULL/date errors should happen before the evidence guard.
                for i,value in updates.items(): values[i]=value
                results[name] = rejected(cur,insert,values,EXPECTED["sql_rejections"][name])
    return {"rows":len(rows),"sql_rejections":results,"explicit_negative_ids_preserve_sequences":True}


def teardown(url):
    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE cmpe.manufacturing_responsibility_21")
            cur.execute("DROP FUNCTION cmpe.check_manufacturing_responsibility_21()")
            for table, key in [("evidence_support","evidence_support_id"),("assertion","assertion_id"),
                               ("source_record","source_record_id"),("dataset_release","dataset_release_id"),
                               ("dataset","dataset_id"),("medicinal_product","medicinal_product_id"),
                               ("organization","organization_id"),("transformation_run","transformation_run_id")]:
                cur.execute(f"DELETE FROM cmpe.{table} WHERE {key} BETWEEN -320100 AND -320001")


def sequences(url):
    with psycopg.connect(url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT sequencename,last_value FROM pg_sequences WHERE schemaname='cmpe' ORDER BY sequencename")
            return [dict(r) for r in cur.fetchall()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--database-url", default=os.getenv("DATABASE_URL","postgresql://postgres:postgres@localhost:5432/cmpe"))
    ap.add_argument("--output-dir",default="build/v2-21-rdb-m3")
    ap.add_argument("--offline",action="store_true",help="RDF/native/source/SHACL/HermiT only; never claim SQL execution")
    args=ap.parse_args(); out=ROOT/args.output_dir; out.mkdir(parents=True,exist_ok=True)
    config=json.loads((HERE/"scope.json").read_text()); m1.pin_inputs(config)
    report={"schema_version":1,"passed":False,"requirement":"FR-02","model_commit":config["model_commit"],
            "oracle_commit":"0508dc0cb5ce20856f3068abdbdb25c245dd0d13",
            "source":verify_source(),"database_executed":not args.offline,
            "software":{"python":platform.python_version(),"psycopg":psycopg.__version__,
                        "rdflib":__import__('rdflib').__version__,"pyshacl":__import__('pyshacl').__version__,
                        "owlready2":OWLREADY_VERSION},
            "boundary":"One reviewed FDA label attribution and three synthetic contexts. Source-qualified candidate mapping; legal responsibility, current manufacture, full P3 scientific/author acceptance and release readiness remain open."}
    if args.offline:
        report["rdf"]=rdf_checks(example_rows(),out,config)
        report["passed"]=True; report["scope"]="OFFLINE_RDF_ONLY_NO_POSTGRESQL_CLAIM"
    else:
        before=m1.database_snapshot(args.database_url); sequence_before=sequences(args.database_url)
        legacy_before=m1.run_legacy(args.database_url,out/"before")
        seeded=False
        try:
            report["sql"]=seed(args.database_url); seeded=True
            legacy_during=m1.run_legacy(args.database_url,out/"during")
            validation=out/"during/w6-validation.json"
            subprocess.run([sys.executable,str(ROOT/"tools/v2_data/validate_w6.py"),"--database-url",args.database_url,
                            "--kg",str(out/"during/legacy.ttl"),"--report",str(validation)],
                           cwd=ROOT,check=True,capture_output=True,text=True)
            w6=json.loads(validation.read_text()); assert w6["passed"] and w6["shacl_conforms"]
            with psycopg.connect(args.database_url,row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute(SQL); rows=[dict(r) for r in cur.fetchall()]
            report["rdf"]=rdf_checks(rows,out,config)
            sql_norm=m1.normalize_rows(rows,COLUMNS); rdf_norm=report["rdf"]["query_rows"]
            assert sql_norm==rdf_norm and len(sql_norm)==EXPECTED["admitted_rows"]
            report["q21_03"]={"rows":len(sql_norm),"passed":True,"sql_normalized_sha256":m1.sha(m1.compact(sql_norm)),
                               "sparql_normalized_sha256":m1.sha(m1.compact(rdf_norm))}
            report["legacy_during"]=legacy_during
            report["w6_during_validation"]={"passed":w6["passed"],"shacl_conforms":w6["shacl_conforms"]}
        finally:
            if seeded: teardown(args.database_url)
        after=m1.database_snapshot(args.database_url); sequence_after=sequences(args.database_url)
        legacy_after=m1.run_legacy(args.database_url,out/"after")
        assert before==after and sequence_before==sequence_after and legacy_before==legacy_after
        report.update({"passed":True,"scope":"COPIED_POSTGRESQL_POSTGIS_M3_ONLY", "database_before":before,
                       "database_after":after,"legacy_before":legacy_before,"legacy_after":legacy_after,
                       "sequences_unchanged":True,"rollback_restored":True})
    (out/"report.json").write_text(json.dumps(report,indent=2,sort_keys=True,default=str)+"\n")
    print(json.dumps({"passed":report["passed"],"scope":report["scope"],"q21_03":report.get("q21_03"),
                      "shacl":report["rdf"]["shacl"]["all_expected_met"],"hermit":report["rdf"]["hermit"]["all_expected_met"]},indent=2))


if __name__=="__main__": main()
