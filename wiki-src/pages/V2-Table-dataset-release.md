# dataset_release

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
A versioned/retrieved release of a Dataset.

## Provenance role
Version/retrieval-level provenance.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `dataset_release_id` | `BIGSERIAL` | NO | PK | — |
| `dataset_id` | `BIGINT` | NO | FK to dataset.dataset_id | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `release_label` | `TEXT` | NO | — | — |
| `source_filename` | `TEXT` | YES | — | — |
| `retrieved_at` | `TIMESTAMPTZ` | YES | — | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/DatasetRelease'` |

## Primary key
`dataset_release_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `dataset_id` | `dataset.dataset_id` | NO |

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table source_record|source_record]] | `dataset_release_id` | NO |

## UNIQUE constraints
- `public_id`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M002` | `DatasetRelease` | class | direct | `dataset_release_id/public_id` | Release distinct from Dataset |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `dataset_release_id` | `101` |
| `dataset_id` | `<dataset.dataset_id>` |
| `public_id` | `example:dataset_release:001` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `release_label` | `Example Release Label` |
| `source_filename` | `example` |
| `retrieved_at` | `2026-01-01T00:00:00Z` |

## Common join paths
- Child to parent: `dataset_release.dataset_id` = `dataset.dataset_id`.
- Parent from child: `dataset_release.dataset_release_id` = `source_record.dataset_release_id`.

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
