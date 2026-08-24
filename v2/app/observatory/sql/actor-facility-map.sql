-- V2-077 read-only query contract for T01/T02.
-- This file does not create or mutate ontology/RDB state.

-- T01A: facility lookup with bounded provenance.
-- Bind :query to a case-insensitive substring or exact public identifier.
SELECT
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
  ON ia.entity_type = 'facility'
 AND ia.entity_public_id = f.public_id
LEFT JOIN cmpe.source_record sr ON sr.source_record_id = ia.source_record_id
LEFT JOIN cmpe.dataset_release dr ON dr.dataset_release_id = sr.dataset_release_id
LEFT JOIN cmpe.dataset ds ON ds.dataset_id = dr.dataset_id
LEFT JOIN cmpe.geography g ON g.geography_id = f.geography_id
WHERE lower(f.preferred_name) LIKE lower('%' || :query || '%') OR f.public_id = :query
ORDER BY f.public_id;

-- T01B: organization lookup. W6 does not guarantee direct source-record lineage.
SELECT
  o.public_id AS semantic_id,
  o.preferred_name AS display_label,
  o.ontology_iri AS semantic_type,
  'M009'::text AS mapping_id,
  'provenance-unavailable'::text AS provenance_status
FROM cmpe.organization o
WHERE lower(o.preferred_name) LIKE lower('%' || :query || '%') OR o.public_id = :query
ORDER BY o.public_id;

-- T02: bounded facility spatial predicate.
-- Bind :min_lon, :min_lat, :max_lon, :max_lat. EPSG:4326 is explicit.
SELECT
  f.public_id AS semantic_id,
  f.preferred_name AS display_label,
  f.ontology_iri AS semantic_type,
  'M010'::text AS facility_mapping_id,
  'M031'::text AS location_mapping_id,
  g.public_id AS geography_id,
  g.ontology_iri AS geography_type,
  ST_AsGeoJSON(g.geom) AS geometry_geojson,
  ds.public_id AS dataset_id,
  dr.public_id AS dataset_release_id,
  sr.source_hash,
  CASE WHEN sr.source_record_id IS NULL THEN 'provenance-unavailable' ELSE 'source-backed' END AS provenance_status,
  'regulatory-jurisdiction-not-inferred'::text AS jurisdiction_boundary
FROM cmpe.facility f
JOIN cmpe.geography g ON g.geography_id = f.geography_id
LEFT JOIN cmpe.identifier_assignment ia
  ON ia.entity_type = 'facility'
 AND ia.entity_public_id = f.public_id
LEFT JOIN cmpe.source_record sr ON sr.source_record_id = ia.source_record_id
LEFT JOIN cmpe.dataset_release dr ON dr.dataset_release_id = sr.dataset_release_id
LEFT JOIN cmpe.dataset ds ON ds.dataset_id = dr.dataset_id
WHERE g.geom IS NOT NULL
  AND ST_Intersects(
    g.geom,
    ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326)
  )
ORDER BY f.public_id;
