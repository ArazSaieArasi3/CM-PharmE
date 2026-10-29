BEGIN;
SET search_path TO cmpe, public;

CREATE OR REPLACE VIEW v_product_presentations AS
SELECT
  pp.public_id AS presentation_id,
  mp.public_id AS product_id,
  mp.preferred_name AS product_name,
  ps.public_id AS substance_id,
  ps.preferred_name AS substance_name,
  pp.packaging,
  pp.concentration,
  pp.num_in_pack,
  ia.lexical_value AS nhif_code
FROM product_presentation pp
JOIN medicinal_product mp ON mp.medicinal_product_id = pp.medicinal_product_id
LEFT JOIN pharmaceutical_substance ps ON ps.substance_id = mp.primary_substance_id
LEFT JOIN identifier_assignment ia
  ON ia.entity_type = 'product_presentation'
 AND ia.entity_public_id = pp.public_id
LEFT JOIN identifier_scheme ids ON ids.identifier_scheme_id = ia.identifier_scheme_id
WHERE ids.scheme_name = 'NHIF product code' OR ids.scheme_name IS NULL;

CREATE OR REPLACE VIEW v_observations AS
SELECT
  o.public_id AS observation_id,
  o.observation_kind,
  pp.public_id AS presentation_id,
  mp.public_id AS product_id,
  f.public_id AS facility_id,
  g.public_id AS geography_id,
  g.canonical_name AS geography_name,
  d.code AS diagnosis_code,
  o.reporting_period,
  o.reporting_part,
  o.patient_count,
  o.package_count,
  o.cost_original,
  o.currency,
  o.cost_bgn,
  o.cost_eur,
  sr.source_hash,
  dr.public_id AS dataset_release_id,
  ds.public_id AS dataset_id
FROM observation_result o
LEFT JOIN product_presentation pp ON pp.product_presentation_id = o.product_presentation_id
LEFT JOIN medicinal_product mp ON mp.medicinal_product_id = pp.medicinal_product_id
LEFT JOIN facility f ON f.facility_id = o.facility_id
LEFT JOIN geography g ON g.geography_id = o.geography_id
LEFT JOIN diagnosis_reference d ON d.diagnosis_reference_id = o.diagnosis_reference_id
JOIN source_record sr ON sr.source_record_id = o.source_record_id
JOIN dataset_release dr ON dr.dataset_release_id = sr.dataset_release_id
JOIN dataset ds ON ds.dataset_id = dr.dataset_id;

CREATE OR REPLACE VIEW v_provenance_lineage AS
SELECT
  a.public_id AS assertion_id,
  a.subject_public_id,
  a.predicate_key,
  a.object_lexical,
  a.object_public_id,
  es.public_id AS evidence_support_id,
  sr.source_record_id,
  sr.source_hash,
  sr.row_number,
  dr.public_id AS dataset_release_id,
  ds.public_id AS dataset_id,
  ds.doi,
  tr.public_id AS transformation_run_id,
  tr.adapter_name,
  tr.adapter_version
FROM assertion a
JOIN evidence_support es ON es.assertion_id = a.assertion_id
JOIN source_record sr ON sr.source_record_id = es.source_record_id
JOIN dataset_release dr ON dr.dataset_release_id = sr.dataset_release_id
JOIN dataset ds ON ds.dataset_id = dr.dataset_id
LEFT JOIN transformation_run tr ON tr.transformation_run_id = sr.transformation_run_id;

CREATE OR REPLACE VIEW v_entity_matches AS
SELECT
  ema.public_id AS match_id,
  ema.matched_entity_type,
  ema.matched_public_id,
  ema.method,
  ema.confidence,
  ema.status,
  a.source_hash AS source_hash_a,
  b.source_hash AS source_hash_b
FROM entity_match_assertion ema
JOIN source_record a ON a.source_record_id = ema.source_record_a_id
JOIN source_record b ON b.source_record_id = ema.source_record_b_id;

COMMIT;