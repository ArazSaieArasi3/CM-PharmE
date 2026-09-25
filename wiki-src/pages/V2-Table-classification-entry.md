# classification_entry

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Code/label entry within a product-classification scheme.

## Provenance role
Classification vocabulary entry; source-specific assignment provenance is separate.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `classification_entry_id` | `BIGSERIAL` | NO | PK | — |
| `classification_scheme_id` | `BIGINT` | NO | FK to product_classification_scheme.classification_scheme_id | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `code` | `TEXT` | NO | — | — |
| `label` | `TEXT` | YES | — | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/ClassificationEntry'` |

## Primary key
`classification_entry_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `classification_scheme_id` | `product_classification_scheme.classification_scheme_id` | NO |

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table product_classification_assignment|product_classification_assignment]] | `classification_entry_id` | NO |

## UNIQUE constraints
- `public_id`
- `classification_scheme_id`, `code`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M018` | `ClassificationEntry` | class | direct | `classification_entry_id` | ATC and other entries represented as classification entries |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `classification_entry_id` | `101` |
| `classification_scheme_id` | `<product_classification_scheme.classification_scheme_id>` |
| `public_id` | `example:classification_entry:001` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `code` | `example` |
| `label` | `Example Label` |

## Common join paths
- Child to parent: `classification_entry.classification_scheme_id` = `product_classification_scheme.classification_scheme_id`.
- Parent from child: `classification_entry.classification_entry_id` = `product_classification_assignment.classification_entry_id`.

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
