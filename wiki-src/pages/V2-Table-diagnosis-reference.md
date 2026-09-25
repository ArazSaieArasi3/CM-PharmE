# diagnosis_reference

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Diagnosis-classification reference retained for market-access/reimbursement observations.

## Provenance role
Linked through provenance-bearing observation_result rows.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `diagnosis_reference_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `scheme` | `TEXT` | NO | — | `'ICD-10'` |
| `code` | `TEXT` | NO | — | — |
| `label` | `TEXT` | YES | — | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/DiagnosisClassificationReference'` |

## Primary key
`diagnosis_reference_id`

## Foreign keys
No outgoing foreign key is declared.

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table observation_result|observation_result]] | `diagnosis_reference_id` | YES |

## UNIQUE constraints
- `public_id`
- `scheme`, `code`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M030` | `DiagnosisClassificationReference` | class | direct | `diagnosis_reference_id` | Market-access extension reference |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `diagnosis_reference_id` | `101` |
| `public_id` | `example:diagnosis_reference:001` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `scheme` | `example` |
| `code` | `example` |
| `label` | `Example Label` |

## Common join paths
- Parent from child: `diagnosis_reference.diagnosis_reference_id` = `observation_result.diagnosis_reference_id`.

## Boundaries
- Reference/research realization only.
- Fixture rows are deterministic test data, not population evidence.
- Relational convenience must not collapse protected ontology distinctions.
- Missing mappings remain explicit rather than inferred.

## Authoritative sources
- v2/data/db/schema.sql
- v2/data/mappings/ontology-rdb-mapping.csv
- v2/data/mappings/source-field-ontology-mapping.csv


---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 PostgreSQL/PostGIS DDL and mapping registry
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #236, #237
- **Evidence status:** Generated physical reference with curated purpose/provenance note
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
