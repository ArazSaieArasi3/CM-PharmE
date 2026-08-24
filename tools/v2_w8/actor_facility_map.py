#!/usr/bin/env python3
"""Read-only V2-077 actor/facility demonstrator query CLI.

Consumes W6 PostgreSQL/PostGIS structures. It never writes semantic state.
"""
from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
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
    bbox.add_argument("--html-output", help="Optional standalone article-facing HTML render")
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


def render_html(rows: list[dict[str, Any]], bounds: tuple[float, float, float, float], output: str) -> None:
    min_lon, min_lat, max_lon, max_lat = bounds
    width, height, pad = 900.0, 520.0, 45.0
    lon_span = max(max_lon - min_lon, 1e-9)
    lat_span = max(max_lat - min_lat, 1e-9)

    def xy(lon: float, lat: float) -> tuple[float, float]:
        x = pad + (lon - min_lon) / lon_span * (width - 2 * pad)
        y = height - pad - (lat - min_lat) / lat_span * (height - 2 * pad)
        return x, y

    markers: list[str] = []
    table_rows: list[str] = []
    for row in rows:
        geom = row.get("geometry") or {}
        coords = geom.get("coordinates") or []
        if len(coords) >= 2:
            lon, lat = float(coords[0]), float(coords[1])
            x, y = xy(lon, lat)
            label = html.escape(str(row["display_label"]))
            semantic_id = html.escape(str(row["semantic_id"]))
            markers.append(
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="7"><title>{label} | {semantic_id}</title></circle>'
                f'<text x="{x + 10:.2f}" y="{y - 8:.2f}">{label}</text>'
            )
        table_rows.append(
            "<tr>"
            f"<td>{html.escape(str(row['semantic_id']))}</td>"
            f"<td>{html.escape(str(row['display_label']))}</td>"
            f"<td>{html.escape(str(row['provenance_status']))}</td>"
            f"<td>{html.escape(str(row.get('dataset_id') or 'unavailable'))}</td>"
            f"<td>{html.escape(str(row['jurisdiction_boundary']))}</td>"
            "</tr>"
        )

    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>CM-PharmE V2-077 bounded actor/facility map</title>
<style>body{{font-family:system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem}}svg{{border:1px solid #888;width:100%;height:auto}}circle{{fill:currentColor}}text{{font-size:13px}}table{{border-collapse:collapse;width:100%;margin-top:1rem}}th,td{{border:1px solid #bbb;padding:.4rem;text-align:left}}.boundary{{border-left:4px solid #777;padding:.75rem;background:#f4f4f4}}</style></head>
<body><h1>CM-PharmE V2-077 bounded actor/facility map</h1>
<p class="boundary">Controlled/article-facing demonstrator. Rendering proves only bounded query and provenance mechanics. It does not claim global facility coverage, geospatial completeness, regulatory-jurisdiction inference, usability, effectiveness, or production deployment.</p>
<p>Bounding box: [{min_lon}, {min_lat}] → [{max_lon}, {max_lat}] | Result count: {len(rows)}</p>
<svg viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="Bounded facility point map">{''.join(markers)}</svg>
<table><thead><tr><th>Semantic ID</th><th>Label</th><th>Provenance</th><th>Dataset</th><th>Jurisdiction boundary</th></tr></thead><tbody>{''.join(table_rows)}</tbody></table>
</body></html>"""
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")


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
                bounds = (a.min_lon, a.min_lat, a.max_lon, a.max_lat)
                rows = bbox_lookup(cur, bounds)
                payload = {
                    "task": "T02",
                    "bbox": list(bounds),
                    "results": rows,
                    "claim_boundary": "bounded spatial query only; no geospatial completeness/effectiveness claim",
                }
                if a.html_output:
                    render_html(rows, bounds, a.html_output)
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
