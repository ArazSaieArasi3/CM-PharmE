-- V2-078 read-only T01/T03 browser contract.
-- Governed mappings: M009-M016, M021, M031.
-- No statement in this file mutates ontology/RDB state or invents relations.

-- T01P: MedicinalProduct detail. Source identifiers are exposed as provenance metadata,
-- never as semantic identity.
SELECT
  mp.public_id AS semantic_id,
  mp.preferred_name AS display_label,
  mp.ontology_iri AS semantic_type,
  'M013'::text AS mapping_id,
  ps.public_id AS primary_substance_id,
  ps.preferred_name AS primary_substance_label,
  'M016'::text AS primary_substance_mapping_id,
  ia.lexical_value AS source_identifier,
  sr.source_hash,
  ds.public_id AS dataset_id,
  dr.public_id AS dataset_release_id,
  CASE WHEN sr.source_record_id IS NULL THEN 'provenance-unavailable' ELSE 'source-backed' END AS provenance_status
FROM cmpe.medicinal_product mp
LEFT JOIN cmpe.pharmaceutical_substance ps ON ps.substance_id = mp.primary_substance_id
LEFT JOIN cmpe.identifier_assignment ia
  ON ia.entity_type = 'medicinal_product' AND ia.entity_public_id = mp.public_id
LEFT JOIN cmpe.source_record sr ON sr.source_record_id = ia.source_record_id
LEFT JOIN cmpe.dataset_release dr ON dr.dataset_release_id = sr.dataset_release_id
LEFT JOIN cmpe.dataset ds ON ds.dataset_id = dr.dataset_id
WHERE lower(mp.preferred_name) LIKE lower('%' || :query || '%') OR mp.public_id = :query
ORDER BY mp.public_id, ia.identifier_assignment_id;

-- T01R: Organization/Facility detail. Organization and Facility remain distinct identities.
SELECT
  o.public_id AS organization_id,
  o.preferred_name AS organization_label,
  o.ontology_iri AS organization_type,
  'M009'::text AS organization_mapping_id,
  f.public_id AS facility_id,
  f.preferred_name AS facility_label,
  f.ontology_iri AS facility_type,
  'M010'::text AS facility_mapping_id,
  fo.public_id AS relation_id,
  fo.ontology_iri AS relation_type,
  'M011'::text AS relation_mapping_id,
  fo.valid_from,
  fo.valid_to,
  'provenance-unavailable'::text AS relation_provenance_status
FROM cmpe.facility_operation fo
JOIN cmpe.organization o ON o.organization_id = fo.organization_id
JOIN cmpe.facility f ON f.facility_id = fo.facility_id
WHERE o.public_id = :query OR f.public_id = :query
   OR lower(o.preferred_name) LIKE lower('%' || :query || '%')
   OR lower(f.preferred_name) LIKE lower('%' || :query || '%')
ORDER BY fo.public_id;

-- T03A: Registered presentationOf traversal only (M015).
SELECT
  pp.public_id AS source_semantic_id,
  pp.ontology_iri AS source_semantic_type,
  'https://w3id.org/cm-pharme/2.0/presentationOf'::text AS predicate_iri,
  'M015'::text AS relation_mapping_id,
  mp.public_id AS target_semantic_id,
  mp.ontology_iri AS target_semantic_type,
  pp.packaging,
  pp.concentration,
  pp.num_in_pack,
  ia.lexical_value AS source_identifier,
  sr.source_hash,
  CASE WHEN sr.source_record_id IS NULL THEN 'provenance-unavailable' ELSE 'source-backed' END AS provenance_status
FROM cmpe.product_presentation pp
JOIN cmpe.medicinal_product mp ON mp.medicinal_product_id = pp.medicinal_product_id
LEFT JOIN cmpe.identifier_assignment ia
  ON ia.entity_type = 'product_presentation' AND ia.entity_public_id = pp.public_id
LEFT JOIN cmpe.source_record sr ON sr.source_record_id = ia.source_record_id
WHERE pp.public_id = :semantic_id OR mp.public_id = :semantic_id
ORDER BY pp.public_id;

-- T03B: Registered hasActiveSubstance traversal only (M016).
-- This is deliberately bounded to the W6 primary_substance_id hook and must not be
-- interpreted as a complete medicinal-product composition model.
SELECT
  mp.public_id AS source_semantic_id,
  mp.ontology_iri AS source_semantic_type,
  'https://w3id.org/cm-pharme/2.0/hasActiveSubstance'::text AS predicate_iri,
  'M016'::text AS relation_mapping_id,
  ps.public_id AS target_semantic_id,
  ps.ontology_iri AS target_semantic_type,
  'bounded-primary-substance-hook'::text AS traversal_boundary
FROM cmpe.medicinal_product mp
JOIN cmpe.pharmaceutical_substance ps ON ps.substance_id = mp.primary_substance_id
WHERE mp.public_id = :semantic_id OR ps.public_id = :semantic_id
ORDER BY mp.public_id;
