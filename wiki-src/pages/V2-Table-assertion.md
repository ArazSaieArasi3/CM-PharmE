# assertion

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Canonical auditable assertion/evidence target.

## Provenance role
Evidence target linked to SourceRecord through evidence_support and observations.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `assertion_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `assertion_type` | `TEXT` | NO | — | — |
| `subject_public_id` | `TEXT` | NO | — | — |
| `predicate_key` | `TEXT` | NO | — | — |
| `object_lexical` | `TEXT` | YES | — | — |
| `object_public_id` | `TEXT` | YES | — | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/Assertion'` |

## Primary key
`assertion_id`

## Foreign keys
No outgoing foreign key is declared.

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table evidence_support|evidence_support]] | `assertion_id` | NO |
| [[V2 Table observation_result|observation_result]] | `assertion_id` | NO |

## UNIQUE constraints
- `public_id`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M024` | `Assertion` | class | direct | `assertion_id/public_id` | Canonical assertion/evidence target |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `assertion_id` | `101` |
| `public_id` | `example:assertion:001` |
| `predicate_key` | `example` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `assertion_type` | `example` |
| `subject_public_id` | `example` |
| `object_lexical` | `example` |

## Common join paths
- Parent from child: `assertion.assertion_id` = `evidence_support.assertion_id`.
- Parent from child: `assertion.assertion_id` = `observation_result.assertion_id`.

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
