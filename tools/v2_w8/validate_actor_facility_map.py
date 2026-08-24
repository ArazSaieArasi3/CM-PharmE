#!/usr/bin/env python3
"""Deterministic V2-077 validation over the W6 PostgreSQL/PostGIS baseline."""
from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

from actor_facility_map import bbox_lookup, facility_lookup

ROOT = Path(__file__).resolve().parents[2]
MAPPING_FREEZE = ROOT / "v2/research/w8/actor-facility-mapping-freeze.csv"
W6_MAPPING = ROOT / "v2/data/mappings/ontology-rdb-mapping.csv"
FIXTURE = ROOT / "v2/app/observatory/fixtures/actor-facility-spatial-fixture.csv"
REPORT = ROOT / "build/w8/actor-facility-validation.json"
CMPE = "https://w3id.org/cm-pharme/2.0/"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def assert_mapping_contract() -> dict[str, str]:
    freeze = {r["mapping_id"]: r for r in rows(MAPPING_FREEZE)}
    canonical = {r["mapping_id"]: r for r in rows(W6_MAPPING)}
    required = {"M005", "M006", "M007", "M009", "M010", "M011", "M031"}
    missing = sorted(required - freeze.keys())
    assert not missing, f"Missing W8 mapping freeze rows: {missing}"
    for mid in required:
        assert mid in canonical, f"Unknown W6 mapping ID: {mid}"
        assert freeze[mid]["ontology_iri"] == canonical[mid]["ontology_iri"], f"IRI drift for {mid}"
    return {mid: canonical[mid]["mapping_status"] for mid in sorted(required)}


def ensure_scheme(cur) -> int:
    cur.execute("""
        INSERT INTO cmpe.identifier_scheme(public_id,scheme_name)
        VALUES ('scheme:w8-controlled-facility-id','W8 controlled facility fixture ID')
        ON CONFLICT(public_id) DO UPDATE SET scheme_name=EXCLUDED.scheme_name
        RETURNING identifier_scheme_id
    """)
    return int(cur.fetchone()["identifier_scheme_id"])


def seed_controlled_fixture(cur) -> None:
    cur.execute("""
        INSERT INTO cmpe.dataset(public_id,title,source_role,license_note)
        VALUES ('W8-CONTROLLED-SPATIAL-FIXTURE','W8 controlled spatial fixture','fixture','Controlled non-empirical V2-077 test data')
        ON CONFLICT(public_id) DO UPDATE SET title=EXCLUDED.title, source_role=EXCLUDED.source_role, license_note=EXCLUDED.license_note
        RETURNING dataset_id
    """)
    dataset_id = int(cur.fetchone()["dataset_id"])
    cur.execute("""
        INSERT INTO cmpe.dataset_release(dataset_id,public_id,release_label,source_filename)
        VALUES (%s,'W8-CONTROLLED-SPATIAL-FIXTURE:release:1','1','v2/app/observatory/fixtures/actor-facility-spatial-fixture.csv')
        ON CONFLICT(public_id) DO UPDATE SET source_filename=EXCLUDED.source_filename
        RETURNING dataset_release_id
    """, (dataset_id,))
    release_id = int(cur.fetchone()["dataset_release_id"])
    cur.execute("""
        INSERT INTO cmpe.transformation_run(public_id,adapter_name,adapter_version,status,completed_at)
        VALUES ('run:w8-controlled-spatial','V2-077 controlled spatial fixture','1','completed',now())
        ON CONFLICT(public_id) DO UPDATE SET status='completed', completed_at=now()
        RETURNING transformation_run_id
    """)
    run_id = int(cur.fetchone()["transformation_run_id"])
    scheme_id = ensure_scheme(cur)

    for idx, row in enumerate(rows(FIXTURE), start=1):
        payload = json.dumps(row, sort_keys=True, separators=(",", ":"))
        source_hash = digest(payload)
        cur.execute("""
            INSERT INTO cmpe.source_record(dataset_release_id,transformation_run_id,row_number,source_hash,raw_key)
            VALUES (%s,%s,%s,%s,%s::jsonb)
            ON CONFLICT(dataset_release_id,row_number,source_hash) DO UPDATE SET transformation_run_id=EXCLUDED.transformation_run_id
            RETURNING source_record_id
        """, (release_id, run_id, idx, source_hash, json.dumps({"facility_public_id": row["facility_public_id"]})))
        source_record_id = int(cur.fetchone()["source_record_id"])

        geography_id = None
        if row["geography_public_id"]:
            cur.execute("""
                INSERT INTO cmpe.geography(public_id,geography_type,canonical_name,country_code,geom,ontology_iri)
                VALUES (%s,'other',%s,NULL,ST_SetSRID(ST_Point(%s,%s),4326),%s)
                ON CONFLICT(public_id) DO UPDATE SET canonical_name=EXCLUDED.canonical_name, geom=EXCLUDED.geom
                RETURNING geography_id
            """, (row["geography_public_id"], row["geography_name"], float(row["longitude"]), float(row["latitude"]), CMPE + "GeographicFeature"))
            geography_id = int(cur.fetchone()["geography_id"])

        cur.execute("""
            INSERT INTO cmpe.facility(public_id,preferred_name,geography_id)
            VALUES (%s,%s,%s)
            ON CONFLICT(public_id) DO UPDATE SET preferred_name=EXCLUDED.preferred_name, geography_id=EXCLUDED.geography_id
            RETURNING facility_id
        """, (row["facility_public_id"], row["preferred_name"], geography_id))
        cur.fetchone()

        assignment_public = "identifier-assignment:w8:" + digest(row["facility_public_id"])[:20]
        cur.execute("""
            INSERT INTO cmpe.identifier_assignment(public_id,identifier_scheme_id,entity_type,entity_public_id,lexical_value,source_record_id)
            VALUES (%s,%s,'facility',%s,%s,%s)
            ON CONFLICT(identifier_scheme_id,lexical_value,entity_type,entity_public_id) DO UPDATE SET source_record_id=EXCLUDED.source_record_id
        """, (assignment_public, scheme_id, row["facility_public_id"], row["facility_public_id"], source_record_id))


def main() -> None:
    statuses = assert_mapping_contract()
    db = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cmpe")
    with psycopg.connect(db, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            seed_controlled_fixture(cur)
            conn.commit()

            alpha = facility_lookup(cur, "facility:w8-controlled:alpha")
            assert len(alpha) == 1
            assert alpha[0]["semantic_type"] == CMPE + "Facility"
            assert alpha[0]["mapping_id"] == "M010"
            assert alpha[0]["provenance_status"] == "source-backed"

            no_location = facility_lookup(cur, "facility:w8-controlled:no-location")
            assert len(no_location) == 1
            assert no_location[0]["location_status"] == "unknown/not-supplied"

            spatial = bbox_lookup(cur, (5.0, 5.0, 15.0, 15.0))
            assert [r["semantic_id"] for r in spatial] == ["facility:w8-controlled:alpha"]
            assert spatial[0]["location_mapping_id"] == "M031"
            assert spatial[0]["jurisdiction_boundary"] == "regulatory-jurisdiction-not-inferred"

            wide = bbox_lookup(cur, (0.0, 0.0, 30.0, 30.0))
            assert {r["semantic_id"] for r in wide} == {
                "facility:w8-controlled:alpha",
                "facility:w8-controlled:beta",
            }
            assert "facility:w8-controlled:no-location" not in {r["semantic_id"] for r in wide}

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "PASS",
        "mapping_contract": statuses,
        "fixtures": {
            "F-T01-01": "PASS",
            "F-T01-02": "PASS_BY_QUERY_BOUNDARY",
            "F-T02-01": "PASS",
            "F-T02-02": "PASS",
            "F-T02-03": "PASS",
        },
        "claim_boundary": {
            "controlled_fixture_only": True,
            "geospatial_completeness_claim": False,
            "usability_effectiveness_claim": False,
            "regulatory_jurisdiction_inferred_from_geometry": False,
        },
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
