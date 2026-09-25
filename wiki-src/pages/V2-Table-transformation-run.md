# transformation_run

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Auditable ingestion/transformation execution represented as provenance activity.

## Provenance role
Processing provenance and adapter/version trace.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `transformation_run_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `adapter_name` | `TEXT` | NO | — | — |
| `adapter_version` | `TEXT` | NO | — | — |
| `started_at` | `TIMESTAMPTZ` | NO | — | `now()` |
| `completed_at` | `TIMESTAMPTZ` | YES | — | — |
| `status` | `TEXT` | NO | CHECK status IN ('running','completed','failed') | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/ProvenanceActivity'` |

## Primary key
`transformation_run_id`

## Foreign keys
No outgoing foreign key is declared.

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table source_record|source_record]] | `transformation_run_id` | YES |

## UNIQUE constraints
- `public_id`

## CHECK constraints
- `status IN ('running','completed','failed')`

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M004` | `ProvenanceActivity` | class | direct | `transformation_run_id/public_id` | ETL run represented as provenance activity |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `transformation_run_id` | `101` |
| `public_id` | `example:transformation_run:001` |
| `status` | `completed` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `adapter_name` | `example` |
| `adapter_version` | `example` |
| `started_at` | `2026-01-01T00:00:00Z` |

## Common join paths
- Parent from child: `transformation_run.transformation_run_id` = `source_record.transformation_run_id`.

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
