# V2 Database Data Dictionary

> **Version scope:** V2  
> **Status:** Generated physical reference  
> **Updated:** 2026-09-25

This dictionary is generated from the authoritative V2 schema. It describes the physical database representation, not the domain ontology.

## dataset

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `dataset_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `title` | `TEXT` | NO | NO | — | NO | — |
| `doi` | `TEXT` | YES | NO | — | NO | — |
| `source_role` | `TEXT` | NO | NO | — | NO | `CHECK source_role IN ('primary','secondary','authoritative','conditional','fixture')` |
| `license_note` | `TEXT` | YES | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/Dataset'` |

Detailed table semantics: [[V2 Table dataset]]

## dataset_release

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `dataset_release_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `dataset_id` | `BIGINT` | NO | NO | `dataset.dataset_id` | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `release_label` | `TEXT` | NO | NO | — | NO | — |
| `source_filename` | `TEXT` | YES | NO | — | NO | — |
| `retrieved_at` | `TIMESTAMPTZ` | YES | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/DatasetRelease'` |

Detailed table semantics: [[V2 Table dataset_release]]

## transformation_run

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `transformation_run_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `adapter_name` | `TEXT` | NO | NO | — | NO | — |
| `adapter_version` | `TEXT` | NO | NO | — | NO | — |
| `started_at` | `TIMESTAMPTZ` | NO | NO | — | NO | `DEFAULT now()` |
| `completed_at` | `TIMESTAMPTZ` | YES | NO | — | NO | — |
| `status` | `TEXT` | NO | NO | — | NO | `CHECK status IN ('running','completed','failed')` |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/ProvenanceActivity'` |

Detailed table semantics: [[V2 Table transformation_run]]

## source_record

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `source_record_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `dataset_release_id` | `BIGINT` | NO | NO | `dataset_release.dataset_release_id` | NO | — |
| `transformation_run_id` | `BIGINT` | YES | NO | `transformation_run.transformation_run_id` | NO | — |
| `row_number` | `BIGINT` | NO | NO | — | NO | — |
| `source_hash` | `CHAR(64)` | NO | NO | — | NO | — |
| `raw_key` | `JSONB` | NO | NO | — | NO | `DEFAULT '{}'::jsonb` |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/SourceRecord'` |

Detailed table semantics: [[V2 Table source_record]]

## geography

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `geography_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `geography_type` | `TEXT` | NO | NO | — | NO | `CHECK geography_type IN ('country','administrative_region','other')` |
| `canonical_name` | `TEXT` | NO | NO | — | NO | — |
| `country_code` | `CHAR(2)` | YES | NO | — | NO | — |
| `source_region_code` | `TEXT` | YES | NO | — | NO | — |
| `geonames_id` | `BIGINT` | YES | NO | — | NO | — |
| `geom` | `geometry(Geometry,4326)` | YES | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | — |

Detailed table semantics: [[V2 Table geography]]

## geography_alias

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `geography_alias_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `geography_id` | `BIGINT` | NO | NO | `geography.geography_id` | NO | — |
| `source_system` | `TEXT` | NO | NO | — | NO | — |
| `source_value` | `TEXT` | NO | NO | — | NO | — |
| `normalized_value` | `TEXT` | NO | NO | — | NO | — |
| `resolution_method` | `TEXT` | NO | NO | — | NO | — |
| `confidence` | `NUMERIC(5,4)` | NO | NO | — | NO | `CHECK confidence >= 0 AND confidence <= 1` |
| `source_record_id` | `BIGINT` | YES | NO | `source_record.source_record_id` | NO | — |

Detailed table semantics: [[V2 Table geography_alias]]

## regulatory_jurisdiction

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `regulatory_jurisdiction_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `name` | `TEXT` | NO | NO | — | NO | — |
| `geography_id` | `BIGINT` | YES | NO | `geography.geography_id` | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/RegulatoryJurisdiction'` |

Detailed table semantics: [[V2 Table regulatory_jurisdiction]]

## organization

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `organization_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `preferred_name` | `TEXT` | NO | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/Organization'` |

Detailed table semantics: [[V2 Table organization]]

## facility

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `facility_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `preferred_name` | `TEXT` | NO | NO | — | NO | — |
| `geography_id` | `BIGINT` | YES | NO | `geography.geography_id` | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/Facility'` |

Detailed table semantics: [[V2 Table facility]]

## facility_operation

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `facility_operation_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `organization_id` | `BIGINT` | NO | NO | `organization.organization_id` | NO | — |
| `facility_id` | `BIGINT` | NO | NO | `facility.facility_id` | NO | — |
| `valid_from` | `DATE` | YES | NO | — | NO | — |
| `valid_to` | `DATE` | YES | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/FacilityOperation'` |

Detailed table semantics: [[V2 Table facility_operation]]

## pharmaceutical_substance

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `substance_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `preferred_name` | `TEXT` | NO | NO | — | NO | — |
| `source_code` | `TEXT` | YES | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/PharmaceuticalSubstance'` |

Detailed table semantics: [[V2 Table pharmaceutical_substance]]

## medicinal_product

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `medicinal_product_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `preferred_name` | `TEXT` | NO | NO | — | NO | — |
| `primary_substance_id` | `BIGINT` | YES | NO | `pharmaceutical_substance.substance_id` | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/MedicinalProduct'` |

Detailed table semantics: [[V2 Table medicinal_product]]

## product_presentation

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `product_presentation_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `medicinal_product_id` | `BIGINT` | NO | NO | `medicinal_product.medicinal_product_id` | NO | — |
| `packaging` | `TEXT` | YES | NO | — | NO | — |
| `concentration` | `TEXT` | YES | NO | — | NO | — |
| `num_in_pack` | `NUMERIC` | YES | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/MedicinalProductPresentation'` |

Detailed table semantics: [[V2 Table product_presentation]]

## identifier_scheme

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `identifier_scheme_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `scheme_name` | `TEXT` | NO | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/IdentifierScheme'` |

Detailed table semantics: [[V2 Table identifier_scheme]]

## identifier_assignment

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `identifier_assignment_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `identifier_scheme_id` | `BIGINT` | NO | NO | `identifier_scheme.identifier_scheme_id` | NO | — |
| `entity_type` | `TEXT` | NO | NO | — | NO | `CHECK entity_type IN ('organization','facility','medicinal_product','product_presentation','substance','geography')` |
| `entity_public_id` | `TEXT` | NO | NO | — | NO | — |
| `lexical_value` | `TEXT` | NO | NO | — | NO | — |
| `source_record_id` | `BIGINT` | YES | NO | `source_record.source_record_id` | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/IdentifierAssignment'` |

Detailed table semantics: [[V2 Table identifier_assignment]]

## product_classification_scheme

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `classification_scheme_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `scheme_name` | `TEXT` | NO | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/ProductClassificationScheme'` |

Detailed table semantics: [[V2 Table product_classification_scheme]]

## classification_entry

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `classification_entry_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `classification_scheme_id` | `BIGINT` | NO | NO | `product_classification_scheme.classification_scheme_id` | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `code` | `TEXT` | NO | NO | — | NO | — |
| `label` | `TEXT` | YES | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/ClassificationEntry'` |

Detailed table semantics: [[V2 Table classification_entry]]

## product_classification_assignment

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `product_classification_assignment_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `medicinal_product_id` | `BIGINT` | NO | NO | `medicinal_product.medicinal_product_id` | NO | — |
| `classification_entry_id` | `BIGINT` | NO | NO | `classification_entry.classification_entry_id` | NO | — |
| `source_record_id` | `BIGINT` | YES | NO | `source_record.source_record_id` | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/ProductClassificationAssignment'` |

Detailed table semantics: [[V2 Table product_classification_assignment]]

## diagnosis_reference

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `diagnosis_reference_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `scheme` | `TEXT` | NO | NO | — | NO | `DEFAULT 'ICD-10'` |
| `code` | `TEXT` | NO | NO | — | NO | — |
| `label` | `TEXT` | YES | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/DiagnosisClassificationReference'` |

Detailed table semantics: [[V2 Table diagnosis_reference]]

## assertion

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `assertion_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `assertion_type` | `TEXT` | NO | NO | — | NO | — |
| `subject_public_id` | `TEXT` | NO | NO | — | NO | — |
| `predicate_key` | `TEXT` | NO | NO | — | NO | — |
| `object_lexical` | `TEXT` | YES | NO | — | NO | — |
| `object_public_id` | `TEXT` | YES | NO | — | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/Assertion'` |

Detailed table semantics: [[V2 Table assertion]]

## evidence_support

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `evidence_support_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `source_record_id` | `BIGINT` | NO | NO | `source_record.source_record_id` | NO | — |
| `assertion_id` | `BIGINT` | NO | NO | `assertion.assertion_id` | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/EvidenceSupport'` |

Detailed table semantics: [[V2 Table evidence_support]]

## observation_result

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `observation_result_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `observation_kind` | `TEXT` | NO | NO | — | NO | `CHECK observation_kind IN ('availability','demand','supply_capacity','inventory','lead_time','reimbursement_utilisation')` |
| `product_presentation_id` | `BIGINT` | YES | NO | `product_presentation.product_presentation_id` | NO | — |
| `facility_id` | `BIGINT` | YES | NO | `facility.facility_id` | NO | — |
| `geography_id` | `BIGINT` | YES | NO | `geography.geography_id` | NO | — |
| `diagnosis_reference_id` | `BIGINT` | YES | NO | `diagnosis_reference.diagnosis_reference_id` | NO | — |
| `reporting_period` | `DATE` | NO | NO | — | NO | — |
| `reporting_part` | `TEXT` | YES | NO | — | NO | — |
| `patient_count` | `NUMERIC` | YES | NO | — | NO | — |
| `package_count` | `NUMERIC` | YES | NO | — | NO | — |
| `cost_original` | `NUMERIC` | YES | NO | — | NO | — |
| `currency` | `CHAR(3)` | YES | NO | — | NO | — |
| `cost_bgn` | `NUMERIC` | YES | NO | — | NO | — |
| `cost_eur` | `NUMERIC` | YES | NO | — | NO | — |
| `source_record_id` | `BIGINT` | NO | NO | `source_record.source_record_id` | NO | — |
| `assertion_id` | `BIGINT` | NO | NO | `assertion.assertion_id` | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/ReimbursementUtilisationObservationResult'` |

Detailed table semantics: [[V2 Table observation_result]]

## entity_match_assertion

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `entity_match_assertion_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `source_record_a_id` | `BIGINT` | NO | NO | `source_record.source_record_id` | NO | — |
| `source_record_b_id` | `BIGINT` | NO | NO | `source_record.source_record_id` | NO | — |
| `matched_entity_type` | `TEXT` | NO | NO | — | NO | — |
| `matched_public_id` | `TEXT` | NO | NO | — | NO | — |
| `method` | `TEXT` | NO | NO | — | NO | — |
| `confidence` | `NUMERIC(5,4)` | NO | NO | — | NO | `CHECK confidence >= 0 AND confidence <= 1` |
| `status` | `TEXT` | NO | NO | — | NO | `CHECK status IN ('accepted','ambiguous','rejected')` |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/EntityMatchAssertion'` |

Detailed table semantics: [[V2 Table entity_match_assertion]]

## medicine_shortage_situation

| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |
|---|---|---|---|---|---|---|
| `shortage_id` | `BIGSERIAL` | NO | YES | — | NO | — |
| `public_id` | `TEXT` | NO | NO | — | YES | — |
| `medicinal_product_id` | `BIGINT` | YES | NO | `medicinal_product.medicinal_product_id` | NO | — |
| `product_presentation_id` | `BIGINT` | YES | NO | `product_presentation.product_presentation_id` | NO | — |
| `regulatory_jurisdiction_id` | `BIGINT` | YES | NO | `regulatory_jurisdiction.regulatory_jurisdiction_id` | NO | — |
| `starts_on` | `DATE` | YES | NO | — | NO | — |
| `ends_on` | `DATE` | YES | NO | — | NO | — |
| `source_record_id` | `BIGINT` | YES | NO | `source_record.source_record_id` | NO | — |
| `ontology_iri` | `TEXT` | NO | NO | — | NO | `DEFAULT 'https://w3id.org/cm-pharme/2.0/MedicineShortageSituation'` |

Detailed table semantics: [[V2 Table medicine_shortage_situation]]



---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** v2/data/db/schema.sql
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #236, #237
- **Evidence status:** Generated field-level physical dictionary
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
