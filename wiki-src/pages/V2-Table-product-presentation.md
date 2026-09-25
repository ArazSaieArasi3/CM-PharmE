# product_presentation

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Presentation/package-level medicinal-product identity and retained source presentation attributes.

## Provenance role
Source-derived presentation identity used by identifiers and observations.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `product_presentation_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `medicinal_product_id` | `BIGINT` | NO | FK to medicinal_product.medicinal_product_id | — |
| `packaging` | `TEXT` | YES | — | — |
| `concentration` | `TEXT` | YES | — | — |
| `num_in_pack` | `NUMERIC` | YES | — | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/MedicinalProductPresentation'` |

## Primary key
`product_presentation_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `medicinal_product_id` | `medicinal_product.medicinal_product_id` | NO |

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table observation_result|observation_result]] | `product_presentation_id` | YES |
| [[V2 Table medicine_shortage_situation|medicine_shortage_situation]] | `product_presentation_id` | YES |

## UNIQUE constraints
- `public_id`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M014` | `MedicinalProductPresentation` | class | direct | `product_presentation_id/public_id` | Presentation/package-level identity layer |
| `M015` | `presentationOf` | object_property | direct | `medicinal_product_id` | Foreign key implements presentation→product relation |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `product_presentation_id` | `101` |
| `public_id` | `example:product_presentation:001` |
| `medicinal_product_id` | `<medicinal_product.medicinal_product_id>` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `packaging` | `example` |
| `concentration` | `example` |
| `num_in_pack` | `1` |

## Common join paths
- Child to parent: `product_presentation.medicinal_product_id` = `medicinal_product.medicinal_product_id`.
- Parent from child: `product_presentation.product_presentation_id` = `observation_result.product_presentation_id`.
- Parent from child: `product_presentation.product_presentation_id` = `medicine_shortage_situation.product_presentation_id`.

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
