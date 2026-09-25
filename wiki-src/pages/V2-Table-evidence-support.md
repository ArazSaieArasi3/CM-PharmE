# evidence_support

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Relator linking a SourceRecord to an Assertion.

## Provenance role
Direct evidence relation between SourceRecord and Assertion.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `evidence_support_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `source_record_id` | `BIGINT` | NO | FK to source_record.source_record_id | — |
| `assertion_id` | `BIGINT` | NO | FK to assertion.assertion_id | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/EvidenceSupport'` |

## Primary key
`evidence_support_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `source_record_id` | `source_record.source_record_id` | NO |
| `assertion_id` | `assertion.assertion_id` | NO |

## Incoming references
No implemented table references this table through a physical FK.

## UNIQUE constraints
- `public_id`
- `source_record_id`, `assertion_id`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M025` | `EvidenceSupport` | class | direct | `source_record_id↔assertion_id` | Relator linking source record and assertion |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `evidence_support_id` | `101` |
| `public_id` | `example:evidence_support:001` |
| `source_record_id` | `<source_record.source_record_id>` |
| `assertion_id` | `<assertion.assertion_id>` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |

## Common join paths
- Child to parent: `evidence_support.source_record_id` = `source_record.source_record_id`.
- Child to parent: `evidence_support.assertion_id` = `assertion.assertion_id`.

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
