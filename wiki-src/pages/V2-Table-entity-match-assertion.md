# entity_match_assertion

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Auditable cross-source match assertion with method, confidence and disposition.

## Provenance role
Match provenance via two SourceRecord references.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `entity_match_assertion_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `source_record_a_id` | `BIGINT` | NO | FK to source_record.source_record_id | — |
| `source_record_b_id` | `BIGINT` | NO | FK to source_record.source_record_id | — |
| `matched_entity_type` | `TEXT` | NO | — | — |
| `matched_public_id` | `TEXT` | NO | — | — |
| `method` | `TEXT` | NO | — | — |
| `confidence` | `NUMERIC(5,4)` | NO | CHECK confidence >= 0 AND confidence <= 1 | — |
| `status` | `TEXT` | NO | CHECK status IN ('accepted','ambiguous','rejected') | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/EntityMatchAssertion'` |

## Primary key
`entity_match_assertion_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `source_record_a_id` | `source_record.source_record_id` | NO |
| `source_record_b_id` | `source_record.source_record_id` | NO |

## Incoming references
No implemented table references this table through a physical FK.

## UNIQUE constraints
- `public_id`

## CHECK constraints
- `confidence >= 0 AND confidence <= 1`
- `status IN ('accepted','ambiguous','rejected')`
- `source_record_a_id <> source_record_b_id`

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M022` | `EntityMatchAssertion` | class | direct | `entity_match_assertion_id` | Auditable match assertion with method/confidence/status |
| `M023` | `MatchConfidence` | quality | relational_projection | `confidence` | Quality projected to bounded numeric field |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `entity_match_assertion_id` | `101` |
| `public_id` | `example:entity_match_assertion:001` |
| `source_record_a_id` | `<source_record.source_record_id>` |
| `source_record_b_id` | `<source_record.source_record_id>` |
| `matched_public_id` | `example` |
| `confidence` | `0.9500` |
| `status` | `accepted` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |

## Common join paths
- Child to parent: `entity_match_assertion.source_record_a_id` = `source_record.source_record_id`.
- Child to parent: `entity_match_assertion.source_record_b_id` = `source_record.source_record_id`.

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
