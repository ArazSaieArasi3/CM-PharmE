#!/usr/bin/env python3
"""Bootstrap the W6 PostgreSQL/PostGIS schema and ingest deterministic fixtures.

The fixture contracts mirror the published NHIF outpatient/inpatient schemas.
They validate representation mechanics and are not empirical study results.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row

CMPE = "https://w3id.org/cm-pharme/2.0/"


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--database-url", default=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cmpe"))
    p.add_argument("--schema", default="v2/data/db/schema.sql")
    p.add_argument("--views", default="v2/data/db/views.sql")
    p.add_argument("--outpatient", default="v2/data/fixtures/nhif_outpatient_fixture.csv")
    p.add_argument("--inpatient", default="v2/data/fixtures/nhif_inpatient_fixture.csv")
    p.add_argument("--geography", default="v2/data/fixtures/geography_alias_fixture.csv")
    p.add_argument("--manifest", default="v2/data/sources/source-manifest.json")
    p.add_argument("--reset", action="store_true")
    p.add_argument("--report", default="build/w6/ingest-report.json")
    return p.parse_args()


def norm(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", norm(value)).strip("-") or "value"


def digest(value: str, n: int = 20) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:n]


def row_hash(row: dict[str, str]) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def read_csv(path: str) -> list[dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def one(cur, sql: str, params: tuple[Any, ...]) -> int:
    cur.execute(sql, params)
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("Expected RETURNING row")
    return int(next(iter(row.values())))


def upsert_dataset(cur, spec: dict[str, Any]) -> tuple[int, int]:
    dataset_id = one(cur, """
        INSERT INTO cmpe.dataset(public_id,title,doi,source_role,license_note)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT(public_id) DO UPDATE SET title=EXCLUDED.title, doi=EXCLUDED.doi,
          source_role=EXCLUDED.source_role, license_note=EXCLUDED.license_note
        RETURNING dataset_id
    """, (spec["id"], spec["id"], spec.get("doi"), spec["role"], spec.get("license_note")))
    release_public = f"{spec['id']}:release:{spec.get('doi') or 'contract'}"
    release_id = one(cur, """
        INSERT INTO cmpe.dataset_release(dataset_id,public_id,release_label,source_filename)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT(public_id) DO UPDATE SET source_filename=EXCLUDED.source_filename
        RETURNING dataset_release_id
    """, (dataset_id, release_public, spec.get("doi") or "contract", spec.get("file_contract")))
    return dataset_id, release_id


def upsert_geographies(cur, geography_path: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for row in read_csv(geography_path):
        public_id = f"geo:BG:nhif-region:{row['source_region_code']}"
        geo_id = one(cur, """
            INSERT INTO cmpe.geography(public_id,geography_type,canonical_name,country_code,source_region_code,geonames_id,ontology_iri)
            VALUES (%s,'administrative_region',%s,%s,%s,%s,%s)
            ON CONFLICT(public_id) DO UPDATE SET canonical_name=EXCLUDED.canonical_name,
              source_region_code=EXCLUDED.source_region_code, geonames_id=EXCLUDED.geonames_id
            RETURNING geography_id
        """, (public_id, row["canonical_name"], row["country_code"], row["source_region_code"],
              int(row["geonames_id"]) if row.get("geonames_id") else None, CMPE + "AdministrativeRegion"))
        cur.execute("""
            INSERT INTO cmpe.geography_alias(geography_id,source_system,source_value,normalized_value,resolution_method,confidence)
            VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT(source_system,source_value) DO UPDATE SET geography_id=EXCLUDED.geography_id,
              normalized_value=EXCLUDED.normalized_value,resolution_method=EXCLUDED.resolution_method,confidence=EXCLUDED.confidence
        """, (geo_id, row["source_system"], row["source_value"], norm(row["source_value"]), row["resolution_method"], row["confidence"]))
        result[row["source_region_code"]] = geo_id
    return result


def upsert_scheme(cur, public_id: str, scheme_name: str, table: str, id_field: str) -> int:
    allowed = {
        "identifier_scheme": ("identifier_scheme_id", "scheme_name"),
        "product_classification_scheme": ("classification_scheme_id", "scheme_name"),
    }
    if table not in allowed or allowed[table][0] != id_field:
        raise ValueError("Unsupported scheme table")
    name_field = allowed[table][1]
    return one(cur, f"""
        INSERT INTO cmpe.{table}(public_id,{name_field}) VALUES (%s,%s)
        ON CONFLICT(public_id) DO UPDATE SET {name_field}=EXCLUDED.{name_field}
        RETURNING {id_field}
    """, (public_id, scheme_name))


def insert_row(cur, row: dict[str, str], source_spec: dict[str, Any], release_id: int,
               run_id: int, row_number: int, geo_by_code: dict[str, int], inpatient: bool) -> dict[str, Any]:
    h = row_hash(row)
    raw_key = {
        "region_num": row.get("region_num"),
        "nhif_code": row.get("nhif_code"),
        "icd_code": row.get("icd_code"),
        "period": row.get("period"),
        "part": row.get("part"),
        "hospital_code": row.get("hospital_code"),
    }
    source_record_id = one(cur, """
        INSERT INTO cmpe.source_record(dataset_release_id,transformation_run_id,row_number,source_hash,raw_key)
        VALUES (%s,%s,%s,%s,%s::jsonb)
        ON CONFLICT(dataset_release_id,row_number,source_hash) DO UPDATE SET transformation_run_id=EXCLUDED.transformation_run_id
        RETURNING source_record_id
    """, (release_id, run_id, row_number, h, json.dumps(raw_key, sort_keys=True)))

    region_code = row["region_num"]
    if region_code not in geo_by_code:
        raise ValueError(f"Unresolved fixture region code: {region_code}")
    geography_id = geo_by_code[region_code]

    substance_name = row["atc_name"].strip()
    substance_public = "substance:source-label:" + digest(norm(substance_name))
    substance_id = one(cur, """
        INSERT INTO cmpe.pharmaceutical_substance(public_id,preferred_name,source_code)
        VALUES (%s,%s,NULL)
        ON CONFLICT(public_id) DO UPDATE SET preferred_name=EXCLUDED.preferred_name
        RETURNING substance_id
    """, (substance_public, substance_name))

    product_key = f"{norm(row['market_name'])}|{substance_public}"
    product_public = "product:source-normalized:" + digest(product_key)
    product_id = one(cur, """
        INSERT INTO cmpe.medicinal_product(public_id,preferred_name,primary_substance_id)
        VALUES (%s,%s,%s)
        ON CONFLICT(public_id) DO UPDATE SET preferred_name=EXCLUDED.preferred_name,primary_substance_id=EXCLUDED.primary_substance_id
        RETURNING medicinal_product_id
    """, (product_public, row["market_name"].strip(), substance_id))

    presentation_key = "|".join([row["nhif_code"].strip(), norm(row["packaging"]), norm(row["concentration"]), row["num_in_pack"].strip()])
    presentation_public = "presentation:nhif:" + digest(presentation_key)
    presentation_id = one(cur, """
        INSERT INTO cmpe.product_presentation(public_id,medicinal_product_id,packaging,concentration,num_in_pack)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT(public_id) DO UPDATE SET medicinal_product_id=EXCLUDED.medicinal_product_id,
          packaging=EXCLUDED.packaging,concentration=EXCLUDED.concentration,num_in_pack=EXCLUDED.num_in_pack
        RETURNING product_presentation_id
    """, (presentation_public, product_id, row["packaging"].strip(), row["concentration"].strip(), row["num_in_pack"] or None))

    id_scheme = upsert_scheme(cur, "scheme:nhif-product-code", "NHIF product code", "identifier_scheme", "identifier_scheme_id")
    identifier_public = "identifier-assignment:nhif:" + digest(presentation_public + "|" + row["nhif_code"])
    cur.execute("""
        INSERT INTO cmpe.identifier_assignment(public_id,identifier_scheme_id,entity_type,entity_public_id,lexical_value,source_record_id)
        VALUES (%s,%s,'product_presentation',%s,%s,%s)
        ON CONFLICT(identifier_scheme_id,lexical_value,entity_type,entity_public_id) DO UPDATE SET source_record_id=EXCLUDED.source_record_id
    """, (identifier_public, id_scheme, presentation_public, row["nhif_code"].strip(), source_record_id))

    atc_scheme = upsert_scheme(cur, "scheme:atc", "ATC", "product_classification_scheme", "classification_scheme_id")
    atc_public = "classification:atc:" + slug(row["atc_code"])
    atc_entry_id = one(cur, """
        INSERT INTO cmpe.classification_entry(classification_scheme_id,public_id,code,label)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT(classification_scheme_id,code) DO UPDATE SET label=EXCLUDED.label
        RETURNING classification_entry_id
    """, (atc_scheme, atc_public, row["atc_code"].strip(), row["atc_name"].strip()))
    assign_public = "classification-assignment:" + digest(product_public + "|" + atc_public)
    cur.execute("""
        INSERT INTO cmpe.product_classification_assignment(public_id,medicinal_product_id,classification_entry_id,source_record_id)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT(medicinal_product_id,classification_entry_id) DO UPDATE SET source_record_id=EXCLUDED.source_record_id
    """, (assign_public, product_id, atc_entry_id, source_record_id))

    diagnosis_public = "diagnosis:icd10:" + slug(row["icd_code"])
    diagnosis_id = one(cur, """
        INSERT INTO cmpe.diagnosis_reference(public_id,scheme,code,label)
        VALUES (%s,'ICD-10',%s,%s)
        ON CONFLICT(scheme,code) DO UPDATE SET label=EXCLUDED.label
        RETURNING diagnosis_reference_id
    """, (diagnosis_public, row["icd_code"].strip(), row["icd_name"].strip()))

    facility_id = None
    facility_public = None
    if inpatient:
        facility_public = "facility:nhif:" + row["hospital_code"].strip()
        facility_id = one(cur, """
            INSERT INTO cmpe.facility(public_id,preferred_name,geography_id)
            VALUES (%s,%s,%s)
            ON CONFLICT(public_id) DO UPDATE SET preferred_name=EXCLUDED.preferred_name,geography_id=EXCLUDED.geography_id
            RETURNING facility_id
        """, (facility_public, row["hospital_name"].strip(), geography_id))
        facility_scheme = upsert_scheme(cur, "scheme:nhif-hospital-code", "NHIF hospital code", "identifier_scheme", "identifier_scheme_id")
        cur.execute("""
            INSERT INTO cmpe.identifier_assignment(public_id,identifier_scheme_id,entity_type,entity_public_id,lexical_value,source_record_id)
            VALUES (%s,%s,'facility',%s,%s,%s)
            ON CONFLICT(identifier_scheme_id,lexical_value,entity_type,entity_public_id) DO UPDATE SET source_record_id=EXCLUDED.source_record_id
        """, ("identifier-assignment:hospital:" + digest(facility_public), facility_scheme, facility_public, row["hospital_code"].strip(), source_record_id))

    assertion_public = "assertion:observation:" + h
    assertion_id = one(cur, """
        INSERT INTO cmpe.assertion(public_id,assertion_type,subject_public_id,predicate_key,object_lexical)
        VALUES (%s,'source-observation',%s,'reimbursement-utilisation',%s)
        ON CONFLICT(public_id) DO UPDATE SET object_lexical=EXCLUDED.object_lexical
        RETURNING assertion_id
    """, (assertion_public, presentation_public, h))
    cur.execute("""
        INSERT INTO cmpe.evidence_support(public_id,source_record_id,assertion_id)
        VALUES (%s,%s,%s)
        ON CONFLICT(source_record_id,assertion_id) DO NOTHING
    """, ("evidence-support:" + h, source_record_id, assertion_id))

    obs_public = "observation:" + h
    cur.execute("""
        INSERT INTO cmpe.observation_result(
          public_id,observation_kind,product_presentation_id,facility_id,geography_id,diagnosis_reference_id,
          reporting_period,reporting_part,patient_count,package_count,cost_original,currency,cost_bgn,cost_eur,
          source_record_id,assertion_id)
        VALUES (%s,'reimbursement_utilisation',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT(public_id) DO UPDATE SET patient_count=EXCLUDED.patient_count,package_count=EXCLUDED.package_count,
          cost_original=EXCLUDED.cost_original,cost_bgn=EXCLUDED.cost_bgn,cost_eur=EXCLUDED.cost_eur
    """, (obs_public, presentation_id, facility_id, geography_id, diagnosis_id, row["period"], row.get("part") or None,
          row.get("patients_num") or None, row.get("pack_num") or None, row.get("costs") or None,
          row.get("currency") or None, row.get("costs_bgn") or None, row.get("costs_eur") or None,
          source_record_id, assertion_id))

    return {
        "source_spec": source_spec["id"], "source_record_id": source_record_id,
        "presentation_public": presentation_public, "presentation_key": presentation_key,
        "facility_public": facility_public, "nhif_code": row["nhif_code"].strip()
    }


def main():
    a = args()
    manifest = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    specs = {s["id"]: s for s in manifest["sources"]}
    out_spec = specs["P1-NHIF-OUTPATIENT"]
    in_spec = specs["P2-NHIF-INPATIENT"]
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)

    with psycopg.connect(a.database_url, row_factory=dict_row) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            if a.reset:
                cur.execute("DROP SCHEMA IF EXISTS cmpe CASCADE")
            cur.execute(Path(a.schema).read_text(encoding="utf-8"), prepare=False)
            cur.execute(Path(a.views).read_text(encoding="utf-8"), prepare=False)

            geo = upsert_geographies(cur, a.geography)
            _, out_release = upsert_dataset(cur, out_spec)
            _, in_release = upsert_dataset(cur, in_spec)
            run_public = "run:w6-fixture:" + digest(Path(a.outpatient).read_text() + Path(a.inpatient).read_text())
            run_id = one(cur, """
                INSERT INTO cmpe.transformation_run(public_id,adapter_name,adapter_version,status)
                VALUES (%s,'w6-nhif-fixture-loader','1.0.0','running')
                ON CONFLICT(public_id) DO UPDATE SET status='running',started_at=now(),completed_at=NULL
                RETURNING transformation_run_id
            """, (run_public,))

            records: list[dict[str, Any]] = []
            for i, row in enumerate(read_csv(a.outpatient), 1):
                records.append(insert_row(cur, row, out_spec, out_release, run_id, i, geo, inpatient=False))
            for i, row in enumerate(read_csv(a.inpatient), 1):
                records.append(insert_row(cur, row, in_spec, in_release, run_id, i, geo, inpatient=True))

            by_key: dict[str, list[dict[str, Any]]] = {}
            for r in records:
                by_key.setdefault(r["presentation_key"], []).append(r)
            match_count = 0
            for key, group in by_key.items():
                left = [r for r in group if r["source_spec"] == "P1-NHIF-OUTPATIENT"]
                right = [r for r in group if r["source_spec"] == "P2-NHIF-INPATIENT"]
                if not left or not right:
                    continue
                for x in left[:1]:
                    for y in right[:1]:
                        match_public = "entity-match:" + digest(f"{x['source_record_id']}|{y['source_record_id']}|{key}")
                        cur.execute("""
                            INSERT INTO cmpe.entity_match_assertion(public_id,source_record_a_id,source_record_b_id,
                              matched_entity_type,matched_public_id,method,confidence,status)
                            VALUES (%s,%s,%s,'product_presentation',%s,'exact-source-code-plus-presentation-normalization',1.0,'accepted')
                            ON CONFLICT(public_id) DO NOTHING
                        """, (match_public, x["source_record_id"], y["source_record_id"], x["presentation_public"]))
                        match_count += 1

            cur.execute("UPDATE cmpe.transformation_run SET status='completed',completed_at=now() WHERE transformation_run_id=%s", (run_id,))

            tables = ["dataset","dataset_release","source_record","geography","facility","pharmaceutical_substance",
                      "medicinal_product","product_presentation","identifier_assignment","classification_entry",
                      "observation_result","assertion","evidence_support","entity_match_assertion"]
            counts = {}
            for table in tables:
                cur.execute(f"SELECT count(*) AS n FROM cmpe.{table}")
                counts[table] = int(cur.fetchone()["n"])

    report = {
        "schema_version": 1,
        "mode": "schema-faithful-fixture",
        "primary_source_contract": out_spec["doi"],
        "secondary_source_contract": in_spec["doi"],
        "full_external_dataset_ingestion": false,
        "aggregate_patient_semantics_preserved": true,
        "accepted_cross_source_match_assertions_created": match_count,
        "counts": counts,
        "held_out_used": false,
    }
    Path(a.report).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
