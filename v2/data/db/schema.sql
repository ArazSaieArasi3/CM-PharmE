BEGIN;
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA IF NOT EXISTS cmpe;
SET search_path TO cmpe, public;

CREATE TABLE dataset (
  dataset_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  doi TEXT,
  source_role TEXT NOT NULL CHECK (source_role IN ('primary','secondary','authoritative','conditional','fixture')),
  license_note TEXT,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/Dataset'
);

CREATE TABLE dataset_release (
  dataset_release_id BIGSERIAL PRIMARY KEY,
  dataset_id BIGINT NOT NULL REFERENCES dataset(dataset_id),
  public_id TEXT NOT NULL UNIQUE,
  release_label TEXT NOT NULL,
  source_filename TEXT,
  retrieved_at TIMESTAMPTZ,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/DatasetRelease'
);

CREATE TABLE transformation_run (
  transformation_run_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  adapter_name TEXT NOT NULL,
  adapter_version TEXT NOT NULL,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ,
  status TEXT NOT NULL CHECK (status IN ('running','completed','failed')),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/ProvenanceActivity'
);

CREATE TABLE source_record (
  source_record_id BIGSERIAL PRIMARY KEY,
  dataset_release_id BIGINT NOT NULL REFERENCES dataset_release(dataset_release_id),
  transformation_run_id BIGINT REFERENCES transformation_run(transformation_run_id),
  row_number BIGINT NOT NULL,
  source_hash CHAR(64) NOT NULL,
  raw_key JSONB NOT NULL DEFAULT '{}'::jsonb,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/SourceRecord',
  UNIQUE(dataset_release_id, row_number, source_hash)
);

CREATE TABLE geography (
  geography_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  geography_type TEXT NOT NULL CHECK (geography_type IN ('country','administrative_region','other')),
  canonical_name TEXT NOT NULL,
  country_code CHAR(2),
  source_region_code TEXT,
  geonames_id BIGINT,
  geom geometry(Geometry,4326),
  ontology_iri TEXT NOT NULL
);
CREATE INDEX geography_geom_gix ON geography USING GIST (geom);
CREATE INDEX geography_geonames_idx ON geography(geonames_id) WHERE geonames_id IS NOT NULL;

CREATE TABLE geography_alias (
  geography_alias_id BIGSERIAL PRIMARY KEY,
  geography_id BIGINT NOT NULL REFERENCES geography(geography_id),
  source_system TEXT NOT NULL,
  source_value TEXT NOT NULL,
  normalized_value TEXT NOT NULL,
  resolution_method TEXT NOT NULL,
  confidence NUMERIC(5,4) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  source_record_id BIGINT REFERENCES source_record(source_record_id),
  UNIQUE(source_system, source_value)
);

CREATE TABLE regulatory_jurisdiction (
  regulatory_jurisdiction_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  geography_id BIGINT REFERENCES geography(geography_id),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/RegulatoryJurisdiction'
);

CREATE TABLE organization (
  organization_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  preferred_name TEXT NOT NULL,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/Organization'
);

CREATE TABLE facility (
  facility_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  preferred_name TEXT NOT NULL,
  geography_id BIGINT REFERENCES geography(geography_id),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/Facility'
);

CREATE TABLE facility_operation (
  facility_operation_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  organization_id BIGINT NOT NULL REFERENCES organization(organization_id),
  facility_id BIGINT NOT NULL REFERENCES facility(facility_id),
  valid_from DATE,
  valid_to DATE,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/FacilityOperation',
  CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)
);

CREATE TABLE pharmaceutical_substance (
  substance_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  preferred_name TEXT NOT NULL,
  source_code TEXT,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/PharmaceuticalSubstance'
);

CREATE TABLE medicinal_product (
  medicinal_product_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  preferred_name TEXT NOT NULL,
  primary_substance_id BIGINT REFERENCES pharmaceutical_substance(substance_id),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/MedicinalProduct'
);

CREATE TABLE product_presentation (
  product_presentation_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  medicinal_product_id BIGINT NOT NULL REFERENCES medicinal_product(medicinal_product_id),
  packaging TEXT,
  concentration TEXT,
  num_in_pack NUMERIC,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/MedicinalProductPresentation'
);

CREATE TABLE identifier_scheme (
  identifier_scheme_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  scheme_name TEXT NOT NULL,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/IdentifierScheme'
);

CREATE TABLE identifier_assignment (
  identifier_assignment_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  identifier_scheme_id BIGINT NOT NULL REFERENCES identifier_scheme(identifier_scheme_id),
  entity_type TEXT NOT NULL CHECK (entity_type IN ('organization','facility','medicinal_product','product_presentation','substance','geography')),
  entity_public_id TEXT NOT NULL,
  lexical_value TEXT NOT NULL,
  source_record_id BIGINT REFERENCES source_record(source_record_id),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/IdentifierAssignment',
  UNIQUE(identifier_scheme_id, lexical_value, entity_type, entity_public_id)
);

CREATE TABLE product_classification_scheme (
  classification_scheme_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  scheme_name TEXT NOT NULL,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/ProductClassificationScheme'
);

CREATE TABLE classification_entry (
  classification_entry_id BIGSERIAL PRIMARY KEY,
  classification_scheme_id BIGINT NOT NULL REFERENCES product_classification_scheme(classification_scheme_id),
  public_id TEXT NOT NULL UNIQUE,
  code TEXT NOT NULL,
  label TEXT,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/ClassificationEntry',
  UNIQUE(classification_scheme_id, code)
);

CREATE TABLE product_classification_assignment (
  product_classification_assignment_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  medicinal_product_id BIGINT NOT NULL REFERENCES medicinal_product(medicinal_product_id),
  classification_entry_id BIGINT NOT NULL REFERENCES classification_entry(classification_entry_id),
  source_record_id BIGINT REFERENCES source_record(source_record_id),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/ProductClassificationAssignment',
  UNIQUE(medicinal_product_id, classification_entry_id)
);

CREATE TABLE diagnosis_reference (
  diagnosis_reference_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  scheme TEXT NOT NULL DEFAULT 'ICD-10',
  code TEXT NOT NULL,
  label TEXT,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/DiagnosisClassificationReference',
  UNIQUE(scheme, code)
);

CREATE TABLE assertion (
  assertion_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  assertion_type TEXT NOT NULL,
  subject_public_id TEXT NOT NULL,
  predicate_key TEXT NOT NULL,
  object_lexical TEXT,
  object_public_id TEXT,
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/Assertion'
);

CREATE TABLE evidence_support (
  evidence_support_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  source_record_id BIGINT NOT NULL REFERENCES source_record(source_record_id),
  assertion_id BIGINT NOT NULL REFERENCES assertion(assertion_id),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/EvidenceSupport',
  UNIQUE(source_record_id, assertion_id)
);

CREATE TABLE observation_result (
  observation_result_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  observation_kind TEXT NOT NULL CHECK (observation_kind IN ('availability','demand','supply_capacity','inventory','lead_time','reimbursement_utilisation')),
  product_presentation_id BIGINT REFERENCES product_presentation(product_presentation_id),
  facility_id BIGINT REFERENCES facility(facility_id),
  geography_id BIGINT REFERENCES geography(geography_id),
  diagnosis_reference_id BIGINT REFERENCES diagnosis_reference(diagnosis_reference_id),
  reporting_period DATE NOT NULL,
  reporting_part TEXT,
  patient_count NUMERIC,
  package_count NUMERIC,
  cost_original NUMERIC,
  currency CHAR(3),
  cost_bgn NUMERIC,
  cost_eur NUMERIC,
  source_record_id BIGINT NOT NULL REFERENCES source_record(source_record_id),
  assertion_id BIGINT NOT NULL REFERENCES assertion(assertion_id),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/ReimbursementUtilisationObservationResult'
);
CREATE INDEX observation_period_idx ON observation_result(reporting_period);
CREATE INDEX observation_geo_idx ON observation_result(geography_id);
CREATE INDEX observation_presentation_idx ON observation_result(product_presentation_id);

CREATE TABLE entity_match_assertion (
  entity_match_assertion_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  source_record_a_id BIGINT NOT NULL REFERENCES source_record(source_record_id),
  source_record_b_id BIGINT NOT NULL REFERENCES source_record(source_record_id),
  matched_entity_type TEXT NOT NULL,
  matched_public_id TEXT NOT NULL,
  method TEXT NOT NULL,
  confidence NUMERIC(5,4) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  status TEXT NOT NULL CHECK (status IN ('accepted','ambiguous','rejected')),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/EntityMatchAssertion',
  CHECK (source_record_a_id <> source_record_b_id)
);

CREATE TABLE medicine_shortage_situation (
  shortage_id BIGSERIAL PRIMARY KEY,
  public_id TEXT NOT NULL UNIQUE,
  medicinal_product_id BIGINT REFERENCES medicinal_product(medicinal_product_id),
  product_presentation_id BIGINT REFERENCES product_presentation(product_presentation_id),
  regulatory_jurisdiction_id BIGINT REFERENCES regulatory_jurisdiction(regulatory_jurisdiction_id),
  starts_on DATE,
  ends_on DATE,
  source_record_id BIGINT REFERENCES source_record(source_record_id),
  ontology_iri TEXT NOT NULL DEFAULT 'https://w3id.org/cm-pharme/2.0/MedicineShortageSituation',
  CHECK (ends_on IS NULL OR starts_on IS NULL OR ends_on >= starts_on)
);

COMMIT;