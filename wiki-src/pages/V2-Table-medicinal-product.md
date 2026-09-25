# medicinal_product

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Canonical medicinal-product identity with a bounded primary-substance implementation hook.

## Provenance role
Source-normalized identity with mapping/evidence trace through downstream assertions and records.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `medicinal_product_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `preferred_name` | `TEXT` | NO | — | — |
| `primary_substance_id` | `BIGINT` | YES | FK to pharmaceutical_substance.substance_id | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/MedicinalProduct'` |

## Primary key
`medicinal_product_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `primary_substance_id` | `pharmaceutical_substance.substance_id` | YES |

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table product_presentation|product_presentation]] | `medicinal_product_id` | NO |
| [[V2 Table product_classification_assignment|product_classification_assignment]] | `medicinal_product_id` | NO |
| [[V2 Table medicine_shortage_situation|medicine_shortage_situation]] | `medicinal_product_id` | YES |

## UNIQUE constraints
- `public_id`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M013` | `MedicinalProduct` | class | direct | `medicinal_product_id/public_id` | Product identity layer |
| `M016` | `hasActiveSubstance` | object_property | bounded | `primary_substance_id` | W6 reference schema models one primary substance hook; richer composition may require extension |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `medicinal_product_id` | `101` |
| `public_id` | `example:medicinal_product:001` |
| `preferred_name` | `Example Preferred Name` |
| `primary_substance_id` | `<pharmaceutical_substance.substance_id>` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |

## Common join paths
- Child to parent: `medicinal_product.primary_substance_id` = `pharmaceutical_substance.substance_id`.
- Parent from child: `medicinal_product.medicinal_product_id` = `product_presentation.medicinal_product_id`.
- Parent from child: `medicinal_product.medicinal_product_id` = `product_classification_assignment.medicinal_product_id`.
- Parent from child: `medicinal_product.medicinal_product_id` = `medicine_shortage_situation.medicinal_product_id`.

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
