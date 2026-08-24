#!/usr/bin/env python3
"""Read-only V2-077 actor/facility demonstrator query CLI.

Consumes W6 PostgreSQL/PostGIS structures. It never writes semantic state.
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Any

import psycopg
from psycopg.rows import dict_row


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--database-url", default=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cmpe"))
    sub = p.add_subparsers(dest="command", required=True)

    lookup = sub.add_parser("lookup")
    lookup.add_argument("query")
    lookup.add_argument("--kind", choices=("facility", "organization", "all"), default="all")

    bbox = sub.add_parser("bbox")
    bbox.add_argument("min_lon", type=float)
    bbox.add_argument("min_lat", type=float)
    bbox.add_argument("max_lon", type=float)
    bbox.add_argument("max_lat", type=float)
    return p


def facility_lookup(cur, query: str) -> list[dict[str, Any]]:
    cur.execute(
        """
        SELECT DISTINCT ON (f.public_id)
          f.public_id AS semantic_id,
          f.preferred_name AS display_label,
          f.ontology_iri AS semantic_type,
          'M010'::text AS mapping_id,
          CASE WHEN sr.source_record_id IS NULL THEN 'provenance-unavailable' ELSE 'source-backed' END AS provenance_status,
          ds.public_id AS dataset_id,
          dr.public_id AS dataset_release_id,
          sr.source_hash,
          g.public_id AS geography_id,
          g.canonical_name AS geography_name,
          CASE WHEN g.geom IS NULL THEN 'unknown/not-supplied' ELSE 'source-backed-or-controlled' END AS location_status
        FROM cmpe.facility f
        LEFT JOIN cmpe.identifier_assignment ia
          ON ia.entity_type='facility' AND ia.entity_public_id=f.public_id
        LEFT JOIN cmpe.source_record sr ON sr.source_record_id=ia.source_record_id
        LEFT JOIN cmpe.dataset_release dr ON dr.dataset_release_id=sr.dataset_release_id
        LEFT JOIN cmpe.dataset ds ON ds.dataset_id=dr.dataset_id
        LEFT JOIN cmpe.geography g ON g.geography_id=f.geography_id
        WHERE lower(f.preferred_name) LIKE lower(%s) OR f.public_id=%s
        ORDER BY f.public_id, sr.source_record_id NULLS LAST
        """,
        (f"%{query}%", query),
    )
    return list(cur.fetchall())


def organization_lookup(cur, query: str) -> list[dict[str, Any]]:
    cur.execute(
        """
        SELECT
          o.public_id AS semantic_id,
          o.preferred_name AS display_label,
          o.ontology_iri AS semantic_type,
          'M009'::text AS mapping_id,
          'provenance-unavailable'::text AS provenance_status
        FROM cmpe.organization o
        WHERE lower(o.preferred_name) LIKE lower(%s) OR o.public_id=%s
        ORDER BY o.public_id
        """,
        (f"%{query}%", query),
    )
    return list(cur.fetchall())


def bbox_lookup(cur, bounds: tuple[float, float, float, float]) -> list[dict[str, Any]]:
    min_lon, min_lat, max_lon, max_lat = bounds
    if min_lon > max_lon or min_lat > max_lat:
        raise ValueError("Invalid bounding box ordering")
    cur.execute(
        """
        SELECT DISTINCT ON (f.public_id)
          f.public_id AS semantic_id,
          f.preferred_name AS display_label,
          f.ontology_iri AS semantic_type,
          'M010'::text AS facility_mapping_id,
          'M031'::text AS location_mapping_id,
          g.public_id AS geography_id,
          g.ontology_iri AS geography_type,
          ST_AsGeoJSON(g.geom)::json AS geometry,
          ds.public_id AS dataset_id,
          dr.public_id AS dataset_release_id,
          sr.source_hash,
          CASE WHEN sr.source_record_id IS NULL THEN 'provenance-unavailable' ELSE 'source-backed' END AS provenance_status,
          'regulatory-jurisdiction-not-inferred'::text AS jurisdiction_boundary
        FROM cmpe.facility f
        JOIN cmpe.geography g ON g.geography_id=f.geography_id
        LEFT JOIN cmpe.identifier_assignment ia
          ON ia.entity_type='facility' AND ia.entity_public_id=f.public_id
        LEFT JOIN cmpe.source_record sr ON sr.source_record_id=ia.source_record_id
        LEFT JOIN cmpe.dataset_release dr ON dr.dataset_release_id=sr.dataset_release_id
        LEFT JOIN cmpe.dataset ds ON ds.dataset_id=dr.dataset_id
        WHERE g.geom IS NOT NULL
          AND ST_Intersects(g.geom, ST_MakeEnvelope(%s,%s,%s,%s,4326))
        ORDER BY f.public_id, sr.source_record_id NULLS LAST
        """,
        (min_lon, min_lat, max_lon, max_lat),
    )
    return list(cur.fetchall())


def main() -> None:
    a = parser().parse_args()
    with psycopg.connect(a.database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            if a.command == "lookup":
                rows: list[dict[str, Any]] = []
                if a.kind in ("facility", "all"):
                    rows.extend(facility_lookup(cur, a.query))
                if a.kind in ("organization", "all"):
                    rows.extend(organization_lookup(cur, a.query))
                payload = {"task": "T01", "query": a.query, "results": rows}
            else:
                rows = bbox_lookup(cur, (a.min_lon, a.min_lat, a.max_lon, a.max_lat))
                payload = {
                    "task": "T02",
                    "bbox": [a.min_lon, a.min_lat, a.max_lon, a.max_lat],
                    "results": rows,
                    "claim_boundary": "bounded spatial query only; no geospatial completeness/effectiveness claim",
                }
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
