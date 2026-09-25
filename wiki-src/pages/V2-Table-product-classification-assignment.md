# product_classification_assignment

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Provenance-aware assignment of a medicinal product to a classification entry.

## Provenance role
Optional SourceRecord provenance for classification assignment.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `product_classification_assignment_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `medicinal_product_id` | `BIGINT` | NO | FK to medicinal_product.medicinal_product_id | — |
| `classification_entry_id` | `BIGINT` | NO | FK to classification_entry.classification_entry_id | — |
| `source_record_id` | `BIGINT` | YES | FK to source_record.source_record_id | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/ProductClassificationAssignment'` |

## Primary key
`product_classification_assignment_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `medicinal_product_id` | `medicinal_product.medicinal_product_id` | NO |
| `classification_entry_id` | `classification_entry.classification_entry_id` | NO |
| `source_record_id` | `source_record.source_record_id` | YES |

## Incoming references
No implemented table references this table through a physical FK.

## UNIQUE constraints
- `public_id`
- `medicinal_product_id`, `classification_entry_id`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M019` | `ProductClassificationAssignment` | class | direct | `medicinal_product_id↔classification_entry_id` | Contextual assignment with provenance hook |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `product_classification_assignment_id` | `101` |
| `public_id` | `example:product_classification_assignment:001` |
| `medicinal_product_id` | `<medicinal_product.medicinal_product_id>` |
| `classification_entry_id` | `<classification_entry.classification_entry_id>` |
| `source_record_id` | `<source_record.source_record_id>` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |

## Common join paths
- Child to parent: `product_classification_assignment.medicinal_product_id` = `medicinal_product.medicinal_product_id`.
- Child to parent: `product_classification_assignment.classification_entry_id` = `classification_entry.classification_entry_id`.
- Child to parent: `product_classification_assignment.source_record_id` = `source_record.source_record_id`.

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
