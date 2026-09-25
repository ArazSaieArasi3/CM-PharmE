# dataset

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Dataset/source identity and source-role metadata.

## Provenance role
Source provenance root.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `dataset_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `title` | `TEXT` | NO | — | — |
| `doi` | `TEXT` | YES | — | — |
| `source_role` | `TEXT` | NO | CHECK source_role IN ('primary','secondary','authoritative','conditional','fixture') | — |
| `license_note` | `TEXT` | YES | — | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/Dataset'` |

## Primary key
`dataset_id`

## Foreign keys
No outgoing foreign key is declared.

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table dataset_release|dataset_release]] | `dataset_id` | NO |

## UNIQUE constraints
- `public_id`

## CHECK constraints
- `source_role IN ('primary','secondary','authoritative','conditional','fixture')`

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M001` | `Dataset` | class | direct | `dataset_id/public_id` | Dataset identity preserved |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `dataset_id` | `101` |
| `public_id` | `example:dataset:001` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `title` | `Example Title` |
| `doi` | `example` |
| `source_role` | `fixture` |
| `license_note` | `example` |

## Common join paths
- Parent from child: `dataset.dataset_id` = `dataset_release.dataset_id`.

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
