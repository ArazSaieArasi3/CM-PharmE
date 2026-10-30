#!/usr/bin/env python3
"""Copied-W6 FacilityOperation projection, witnesses, parity and rollback."""
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
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL
from rdflib.namespace import DCTERMS, XSD
from pyshacl import validate
from owlrl import DeductiveClosure, OWLRL_Semantics
from owlready2 import World, sync_reasoner
from owlready2.entity import OwlReadyInconsistentOntologyError

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
M1_PATH = HERE.parent / "0.2.0/verify_m1.py"
spec = importlib.util.spec_from_file_location("verify_m1", M1_PATH)
m1 = importlib.util.module_from_spec(spec)
sys.modules["verify_m1"] = m1
spec.loader.exec_module(m1)

C = Namespace("https://w3id.org/cm-pharme/2.1/")
PROV = Namespace("http://www.w3.org/ns/prov#")
FIX = "m2-fixture-"
SQL = """
SELECT fo.public_id AS operation_id, o.public_id AS organization_id,
       f.public_id AS facility_id, fo.valid_from, fo.valid_to,
       dr.public_id AS release_id, sr.row_number, sr.source_hash,
       tr.public_id AS run_id, a.public_id AS assertion_id, es.public_id AS evidence_id
FROM cmpe.facility_operation fo
JOIN cmpe.organization o ON o.organization_id=fo.organization_id
JOIN cmpe.facility f ON f.facility_id=fo.facility_id
LEFT JOIN cmpe.facility_operation_21_evidence x ON x.facility_operation_id=fo.facility_operation_id
LEFT JOIN cmpe.evidence_support es ON es.evidence_support_id=x.evidence_support_id
LEFT JOIN cmpe.assertion a ON a.assertion_id=es.assertion_id
LEFT JOIN cmpe.source_record sr ON sr.source_record_id=es.source_record_id
LEFT JOIN cmpe.dataset_release dr ON dr.dataset_release_id=sr.dataset_release_id
LEFT JOIN cmpe.transformation_run tr ON tr.transformation_run_id=sr.transformation_run_id
ORDER BY fo.public_id, es.public_id
"""
SPARQL = """
PREFIX c: <https://w3id.org/cm-pharme/2.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?operation_id ?organization_id ?facility_id ?valid_from ?valid_to
       ?release_id ?row_number ?source_hash ?run_id ?assertion_id ?evidence_id WHERE {
  ?op a c:FacilityOperation ; dct:identifier ?operation_id ;
      c:operationOrganization ?org ; c:operationFacility ?facility .
  ?org a c:OperatingOrganizationRole ; dct:identifier ?organization_id .
  ?facility a c:OperatedFacilityRole ; dct:identifier ?facility_id .
  OPTIONAL { ?op c:validFrom ?from . BIND(SUBSTR(STR(?from),1,10) AS ?valid_from) }
  OPTIONAL { ?op c:validTo ?to . BIND(SUBSTR(STR(?to),1,10) AS ?valid_to) }
  OPTIONAL {
    ?op prov:wasDerivedFrom ?sr ; dct:relation ?evidence .
    ?sr rdf:value ?row_number ; prov:value ?source_hash .
    ?release c:containsSourceRecord ?sr ; dct:identifier ?release_id .
    ?sr prov:wasGeneratedBy ?run . ?run dct:identifier ?run_id .
    ?evidence dct:identifier ?evidence_id ; dct:relation ?assertion .
    ?assertion dct:identifier ?assertion_id .
  }
} ORDER BY ?operation_id ?evidence_id
"""
COLUMNS = ["operation_id", "organization_id", "facility_id", "valid_from", "valid_to",
           "release_id", "row_number", "source_hash", "run_id", "assertion_id", "evidence_id"]


def cfg_check(config):
    m1.pin_inputs(config)
    for path in ["v2/data/migrations/2.1/0.2.0/verify_m1.py",
                 "v2/data/migrations/2.1/0.2.0/scope.json"]:
        if path not in config["sha256"]:
            raise SystemExit("M1 dependency missing from M2 pins")


def one(cur, query, params):
    cur.execute(query, params)
    return next(iter(cur.fetchone().values()))


def rejected(cur, name, query, params, sqlstate):
    cur.execute("SAVEPOINT m2_expected_failure")
    try:
        cur.execute(query, params)
    except psycopg.Error as exc:
        cur.execute("ROLLBACK TO SAVEPOINT m2_expected_failure")
        cur.execute("RELEASE SAVEPOINT m2_expected_failure")
        if exc.sqlstate != sqlstate:
            raise AssertionError(f"{name}: expected SQLSTATE {sqlstate}, got {exc.sqlstate}") from exc
        return {"name": name, "rejected": True, "sqlstate": exc.sqlstate}
    cur.execute("ROLLBACK TO SAVEPOINT m2_expected_failure")
    cur.execute("RELEASE SAVEPOINT m2_expected_failure")
    raise AssertionError(f"{name}: invalid fixture was accepted")


def seed(url):
    with psycopg.connect(url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE cmpe.facility_operation_21_evidence (
              facility_operation_id BIGINT NOT NULL REFERENCES cmpe.facility_operation(facility_operation_id),
              evidence_support_id BIGINT NOT NULL REFERENCES cmpe.evidence_support(evidence_support_id),
              PRIMARY KEY(facility_operation_id,evidence_support_id))""")
            cur.execute("SELECT geography_id FROM cmpe.geography ORDER BY geography_id LIMIT 1")
            geo = cur.fetchone()["geography_id"]
            orgs = {}
            for key, label in [("a", "Fixture Operator A"), ("b", "Fixture Operator B"),
                               ("unbacked", "Same Name Place")]:
                orgs[key] = one(cur, "INSERT INTO cmpe.organization(public_id,preferred_name) VALUES (%s,%s) RETURNING organization_id",
                                (FIX + "org-" + key, label))
            sites = {}
            for key, label in [("1", "Fixture Site One"), ("2", "Fixture Site Two"),
                               ("unbacked", "Same Name Place")]:
                sites[key] = one(cur, "INSERT INTO cmpe.facility(public_id,preferred_name,geography_id) VALUES (%s,%s,%s) RETURNING facility_id",
                                 (FIX + "site-" + key, label, geo))
            operations = {}
            for key, org, site, start, end in [
                ("a-1", "a", "1", "2026-01-01", "2026-03-31"),
                ("a-2", "a", "2", "2026-02-01", None),
                ("b-1-joint", "b", "1", "2026-02-01", "2026-03-31"),
                ("b-1-successor", "b", "1", "2026-04-01", None)]:
                operations[key] = one(cur, """INSERT INTO cmpe.facility_operation
                    (public_id,organization_id,facility_id,valid_from,valid_to)
                    VALUES (%s,%s,%s,%s,%s) RETURNING facility_operation_id""",
                    (FIX + "op-" + key, orgs[org], sites[site], start, end))

            dataset = one(cur, "INSERT INTO cmpe.dataset(public_id,title,source_role) VALUES (%s,%s,'fixture') RETURNING dataset_id",
                          (FIX + "dataset", "Synthetic operation evidence fixture"))
            release = one(cur, "INSERT INTO cmpe.dataset_release(dataset_id,public_id,release_label) VALUES (%s,%s,%s) RETURNING dataset_release_id",
                          (dataset, FIX + "release", "synthetic-only"))
            run = one(cur, "INSERT INTO cmpe.transformation_run(public_id,adapter_name,adapter_version,status) VALUES (%s,%s,%s,'completed') RETURNING transformation_run_id",
                      (FIX + "run", "m2-fixture", "0.3.0"))
            source_hash = m1.sha(m1.compact({"source_role": "fixture", "operation": FIX + "op-a-1"}))
            source = one(cur, """INSERT INTO cmpe.source_record(dataset_release_id,transformation_run_id,row_number,source_hash,raw_key)
                 VALUES (%s,%s,1,%s,%s::jsonb) RETURNING source_record_id""",
                 (release, run, source_hash, json.dumps({"fixture_only": True, "operation_public_id": FIX + "op-a-1"})))
            assertion = one(cur, """INSERT INTO cmpe.assertion(public_id,assertion_type,subject_public_id,predicate_key,object_public_id)
                 VALUES (%s,'synthetic_fixture',%s,'operationOrganization',%s) RETURNING assertion_id""",
                 (FIX + "assertion", FIX + "op-a-1", FIX + "org-a"))
            evidence = one(cur, "INSERT INTO cmpe.evidence_support(public_id,source_record_id,assertion_id) VALUES (%s,%s,%s) RETURNING evidence_support_id",
                           (FIX + "evidence", source, assertion))
            cur.execute("INSERT INTO cmpe.facility_operation_21_evidence VALUES (%s,%s)", (operations["a-1"], evidence))
            q = "INSERT INTO cmpe.facility_operation(public_id,organization_id,facility_id,valid_from,valid_to) VALUES (%s,%s,%s,%s,%s)"
            negative = [
                rejected(cur, "missing_organization", q, (FIX+"bad-org", None, sites["1"], None, None), "23502"),
                rejected(cur, "missing_facility", q, (FIX+"bad-site", orgs["a"], None, None, None), "23502"),
                rejected(cur, "wrong_foreign_key", q, (FIX+"bad-fk", 987654321, sites["1"], None, None), "23503"),
                rejected(cur, "reversed_interval", q, (FIX+"bad-dates", orgs["a"], sites["1"], "2026-04-01", "2026-03-31"), "23514"),
                rejected(cur, "duplicate_operation_public_id", q, (FIX+"op-a-1", orgs["b"], sites["1"], None, None), "23505"),
            ]
            cur.execute("""SELECT count(*) AS n FROM cmpe.facility_operation fo
                         JOIN cmpe.organization o ON o.organization_id=fo.organization_id
                         JOIN cmpe.facility f ON f.facility_id=fo.facility_id
                         WHERE o.public_id=%s AND f.public_id=%s""",
                        (FIX + "org-unbacked", FIX + "site-unbacked"))
            if cur.fetchone()["n"] != 0:
                raise AssertionError("Equal labels invented an operation")
    return {"fixture_source_hash": source_hash, "operations": len(operations), "sql_negative": negative,
            "same_label_without_operation": True}


def rows_from_db(url):
    with psycopg.connect(url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            cur.execute(SQL)
            return [dict(r) for r in cur.fetchall()]


def export(rows):
    g = Graph()
    for prefix, ns in [("cmpe", C), ("prov", PROV), ("dct", DCTERMS)]:
        g.bind(prefix, ns)
    for r in rows:
        op = m1.node("facility-operation", r["operation_id"])
        org = m1.node("organization", r["organization_id"])
        facility = m1.node("facility", r["facility_id"])
        for n, cls, key in [(op, C.FacilityOperation, r["operation_id"]),
                            (org, C.Organization, r["organization_id"]),
                            (facility, C.Facility, r["facility_id"])]:
            g.add((n, RDF.type, cls))
            g.add((n, DCTERMS.identifier, Literal(key)))
        g.add((org, RDF.type, C.OperatingOrganizationRole))
        g.add((facility, RDF.type, C.OperatedFacilityRole))
        g.add((op, C.operationOrganization, org))
        g.add((op, C.operationFacility, facility))
        for field, prop in [("valid_from", C.validFrom), ("valid_to", C.validTo)]:
            if r[field] is not None:
                g.add((op, prop, Literal(str(r[field]) + "T00:00:00+00:00", datatype=XSD.dateTime)))
        if r["evidence_id"]:
            source = m1.node("source-record", m1.source_key({"release_public": r["release_id"],
                  "row_number": r["row_number"], "source_hash": r["source_hash"]}))
            release = m1.node("dataset-release", r["release_id"])
            run = m1.node("provenance-activity", r["run_id"])
            evidence = m1.node("evidence-support", r["evidence_id"])
            assertion = m1.node("assertion", r["assertion_id"])
            g.add((op, PROV.wasDerivedFrom, source))
            g.add((op, DCTERMS.relation, evidence))
            g.add((source, RDF.type, C.SourceRecord))
            g.add((source, RDF.value, Literal(r["row_number"], datatype=XSD.integer)))
            g.add((source, PROV.value, Literal(r["source_hash"])))
            g.add((release, RDF.type, C.DatasetRelease))
            g.add((release, DCTERMS.identifier, Literal(r["release_id"])))
            g.add((release, C.containsSourceRecord, source))
            g.add((source, PROV.wasGeneratedBy, run))
            g.add((run, RDF.type, C.ProvenanceActivity))
            g.add((run, DCTERMS.identifier, Literal(r["run_id"])))
            g.add((evidence, DCTERMS.identifier, Literal(r["evidence_id"])))
            g.add((evidence, DCTERMS.relation, assertion))
            g.add((assertion, DCTERMS.identifier, Literal(r["assertion_id"])))
    return g


def shacl_cases(g, ontology, shapes):
    def check(data):
        ok, rep, _ = validate(data, shacl_graph=shapes, ont_graph=ontology,
                              inference="rdfs", advanced=True, meta_shacl=True)
        return bool(ok), len(list(rep.subjects(RDF.type, Namespace("http://www.w3.org/ns/shacl#").ValidationResult)))
    ok, count = check(g)
    if not ok: raise AssertionError("Exported graph fails candidate SHACL")
    op = m1.node("facility-operation", FIX + "op-a-1")
    org = m1.node("organization", FIX + "org-a")
    site = m1.node("facility", FIX + "site-1")
    org_b = m1.node("organization", FIX + "org-b")
    site_2 = m1.node("facility", FIX + "site-2")
    cases = {}
    mutations = {
        "missing_operator": ([(op, C.operationOrganization, org)], []),
        "missing_facility": ([(op, C.operationFacility, site)], []),
        "two_operators_one_relator": ([], [(op, C.operationOrganization, org_b)]),
        "two_facilities_one_relator": ([], [(op, C.operationFacility, site_2)]),
        "unbacked_direct_operates": ([], [(org_b, C.operates, site_2)]),
    }
    for name, (remove, add) in mutations.items():
        altered = g - Graph()
        for triple in remove: altered.remove(triple)
        for triple in add: altered.add(triple)
        conform, violations = check(altered)
        if conform or not violations:
            raise AssertionError(f"SHACL did not reject {name}")
        cases[name] = {"conforms": conform, "violations": violations}
    colocated = Graph()
    place = m1.node("geography", FIX + "common-place")
    colocated.add((org, RDF.type, C.Organization))
    colocated.add((site, RDF.type, C.Facility))
    colocated.add((org, DCTERMS.spatial, place))
    colocated.add((site, DCTERMS.spatial, place))
    no_op, _ = check(colocated)
    if not no_op or (org, C.operates, site) in colocated:
        raise AssertionError("Co-location implied an operation")
    return {"exported_conforms": ok, "exported_validation_results": count,
            "negative": cases, "shared_place_without_operation": True}


def dl_consistency(ontology, abox):
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "m2.rdf"
        (ontology + abox).serialize(path, format="xml")
        world = World()
        world.get_ontology(path.as_uri()).load()
        try:
            sync_reasoner(world, debug=0)
            return True
        except OwlReadyInconsistentOntologyError:
            return False


def reasoning(g, ontology):
    asserted = list(g.triples((None, C.operates, None)))
    if asserted: raise AssertionError("Direct operates must not be asserted")
    inferred = ontology + g
    DeductiveClosure(OWLRL_Semantics).expand(inferred)
    pairs = {(str(s), str(o)) for s, _, o in inferred.triples((None, C.operates, None))
             if str(s).startswith(m1.INST) and str(o).startswith(m1.INST)}
    expected = {(str(org), str(site)) for op, _, org in g.triples((None, C.operationOrganization, None))
                for site in g.objects(op, C.operationFacility)}
    if pairs != expected or len(pairs) != 3:
        raise AssertionError(f"Derived operates mismatch: {pairs!r} != {expected!r}")
    one = Graph()
    op = m1.node("facility-operation", FIX + "op-a-1")
    org_a = m1.node("organization", FIX + "org-a")
    org_b = m1.node("organization", FIX + "org-b")
    site = m1.node("facility", FIX + "site-1")
    for triple in [(op,RDF.type,C.FacilityOperation),(org_a,RDF.type,C.OperatingOrganizationRole),
                   (org_b,RDF.type,C.OperatingOrganizationRole),(site,RDF.type,C.OperatedFacilityRole),
                   (op,C.operationOrganization,org_a),(op,C.operationFacility,site)]: one.add(triple)
    positive = dl_consistency(ontology, one)
    missing = one - Graph()
    missing.remove((op, C.operationOrganization, org_a))
    owa = dl_consistency(ontology, missing)
    contradictory = one - Graph()
    contradictory.add((op,C.operationOrganization,org_b))
    contradictory.add((org_a,OWL.differentFrom,org_b))
    distinct = dl_consistency(ontology, contradictory)
    if not positive or not owa or distinct:
        raise AssertionError("HermiT results conflict with bounded relator semantics")
    return {"asserted_direct_operates": 0, "derived_pairs": sorted(pairs),
            "derived_count": len(pairs), "one_operation_consistent": positive,
            "missing_operator_open_world_consistent": owa,
            "two_distinct_operators_one_relator_consistent": distinct}


def teardown(url):
    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE cmpe.facility_operation_21_evidence")
            for table, where in [("evidence_support", "public_id"), ("assertion", "public_id"),
                                 ("source_record", "source_hash"), ("dataset_release", "public_id"),
                                 ("dataset", "public_id"), ("facility_operation", "public_id"),
                                 ("facility", "public_id"), ("organization", "public_id"),
                                 ("transformation_run", "public_id")]:
                # Names are fixed in the script; the fixture prefix is a bound value.
                if table == "source_record":
                    cur.execute("DELETE FROM cmpe.source_record WHERE source_hash=%s", (m1.sha(m1.compact({"source_role":"fixture", "operation":FIX+"op-a-1"})),))
                else:
                    cur.execute(f"DELETE FROM cmpe.{table} WHERE {where} LIKE %s", (FIX + "%",))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--database-url", default=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cmpe"))
    ap.add_argument("--output-dir", default="build/v2-21-rdb-m2")
    args = ap.parse_args()
    out = ROOT / args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    config = json.loads((HERE / "scope.json").read_text())
    cfg_check(config)
    before = m1.database_snapshot(args.database_url)
    old_before = m1.run_legacy(args.database_url, out / "before")
    seeded = seed(args.database_url)
    old_during = m1.run_legacy(args.database_url, out / "during")
    w6_report = out / "during/w6-validation.json"
    subprocess.run([sys.executable, str(ROOT / "tools/v2_data/validate_w6.py"),
                    "--database-url", args.database_url, "--kg", str(out / "during/legacy.ttl"),
                    "--report", str(w6_report)], cwd=ROOT, check=True, capture_output=True, text=True)
    w6_validation = json.loads(w6_report.read_text())
    if not w6_validation["passed"] or not w6_validation["shacl_conforms"]:
        raise AssertionError("W6 validation failed after additive fixture")
    rows = rows_from_db(args.database_url)
    if len(rows) != seeded["operations"] or sum(bool(r["evidence_id"]) for r in rows) != 1:
        raise AssertionError("Unexpected operation or evidence row count")
    graph = export(rows)
    onto = Graph().parse(ROOT / config["candidate_ontology"], format="turtle")
    shapes = Graph().parse(ROOT / config["candidate_shapes"], format="turtle")
    checks = shacl_cases(graph, onto, shapes)
    nt = m1.canonical(graph)
    (out / "facility-operation-21.nt").write_bytes(nt)
    graph.serialize(out / "facility-operation-21.ttl", format="turtle")
    reread = Graph().parse(out / "facility-operation-21.nt", format="nt")
    if m1.canonical(reread) != nt:
        raise AssertionError("RDF round trip changed graph bytes")
    q = reread.query(SPARQL)
    rdf_rows = [{str(v): r[i] for i, v in enumerate(q.vars)} for r in q]
    sql_norm = m1.normalize_rows(rows, COLUMNS)
    rdf_norm = m1.normalize_rows(rdf_rows, COLUMNS)
    if sql_norm != rdf_norm:
        raise AssertionError(f"M2 SQL/SPARQL tuple mismatch: {sql_norm!r} != {rdf_norm!r}")
    reasoner = reasoning(graph, onto)
    during = m1.database_snapshot(args.database_url)
    teardown(args.database_url)
    after = m1.database_snapshot(args.database_url)
    old_after = m1.run_legacy(args.database_url, out / "after")
    if before != after or old_before != old_after:
        raise AssertionError("Rollback failed to restore W6 rows/schema or 2.0 RDF")
    report = {"schema_version": 1, "passed": True, "scope": "W6 M011/M033/M034 copied fixture and scoped P3 relator decision",
              "w6_commit": config["w6_commit"], "model_commit": config["model_commit"],
              "fixture": seeded, "database_before": before,
              "database_during": during,
              "database_after_sha256": after["data_sha256"], "schema_after_sha256": after["schema_sha256"],
              "legacy_before": old_before, "legacy_during": old_during, "legacy_after": old_after,
              "w6_during_validation": {"passed": w6_validation["passed"],
                                      "shacl_conforms": w6_validation["shacl_conforms"]},
              "q21_02": {"rows": len(sql_norm), "passed": True,
                         "sql_normalized_sha256": m1.sha(m1.compact(sql_norm)),
                         "sparql_normalized_sha256": m1.sha(m1.compact(rdf_norm)),
                         "normalized_rows": sql_norm},
              "shacl": checks, "owl": reasoner, "rdf_roundtrip": True,
              "graph_triples": len(graph), "graph_sha256": m1.sha(nt),
              "software": {"python": platform.python_version(), "psycopg": psycopg.__version__,
                           "rdflib": __import__("rdflib").__version__, "owlready2": __import__("owlready2").VERSION,
                           "owlrl": __import__("owlrl").__version__},
              "rollback": "Drop M2-only side table and delete the namespaced synthetic fixture rows; all pre-existing W6 rows, constraints and canonical 2.0 RDF hashes match before/after.",
              "boundary": "One operation has explicitly synthetic fixture evidence; three have unknown provenance. No actual facility-operation source witness, GA, or release acceptance is claimed."}
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2, default=str) + "\n")
    print(json.dumps({"passed": True, "q21_02": report["q21_02"], "shacl": checks,
                      "owl": reasoner, "rollback": True}, indent=2))


if __name__ == "__main__":
    main()
