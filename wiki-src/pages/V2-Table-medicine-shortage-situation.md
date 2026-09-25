# medicine_shortage_situation

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Contextual medicine-shortage situation linked to product/presentation/jurisdiction and optional source provenance.

## Provenance role
Optional SourceRecord provenance.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `shortage_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `medicinal_product_id` | `BIGINT` | YES | FK to medicinal_product.medicinal_product_id | — |
| `product_presentation_id` | `BIGINT` | YES | FK to product_presentation.product_presentation_id | — |
| `regulatory_jurisdiction_id` | `BIGINT` | YES | FK to regulatory_jurisdiction.regulatory_jurisdiction_id | — |
| `starts_on` | `DATE` | YES | — | — |
| `ends_on` | `DATE` | YES | — | — |
| `source_record_id` | `BIGINT` | YES | FK to source_record.source_record_id | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/MedicineShortageSituation'` |

## Primary key
`shortage_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `medicinal_product_id` | `medicinal_product.medicinal_product_id` | YES |
| `product_presentation_id` | `product_presentation.product_presentation_id` | YES |
| `regulatory_jurisdiction_id` | `regulatory_jurisdiction.regulatory_jurisdiction_id` | YES |
| `source_record_id` | `source_record.source_record_id` | YES |

## Incoming references
No implemented table references this table through a physical FK.

## UNIQUE constraints
- `public_id`

## CHECK constraints
- `ends_on IS NULL OR starts_on IS NULL OR ends_on >= starts_on`

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M029` | `MedicineShortageSituation` | class | direct | `shortage_id/public_id` | Contextual shortage situation table |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `shortage_id` | `101` |
| `public_id` | `example:medicine_shortage_situation:001` |
| `medicinal_product_id` | `<medicinal_product.medicinal_product_id>` |
| `product_presentation_id` | `<product_presentation.product_presentation_id>` |
| `regulatory_jurisdiction_id` | `<regulatory_jurisdiction.regulatory_jurisdiction_id>` |
| `source_record_id` | `<source_record.source_record_id>` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |

## Common join paths
- Child to parent: `medicine_shortage_situation.medicinal_product_id` = `medicinal_product.medicinal_product_id`.
- Child to parent: `medicine_shortage_situation.product_presentation_id` = `product_presentation.product_presentation_id`.
- Child to parent: `medicine_shortage_situation.regulatory_jurisdiction_id` = `regulatory_jurisdiction.regulatory_jurisdiction_id`.
- Child to parent: `medicine_shortage_situation.source_record_id` = `source_record.source_record_id`.

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
