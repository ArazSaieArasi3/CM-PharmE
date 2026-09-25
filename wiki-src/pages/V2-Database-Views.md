# V2 Database Views

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

The V2 database defines 4 research/query views in addition to the 24 base tables. Views are not included in the table count.

## v_product_presentations

**Referenced tables:** [[V2 Table identifier_assignment|identifier_assignment]], [[V2 Table identifier_scheme|identifier_scheme]], [[V2 Table medicinal_product|medicinal_product]], [[V2 Table pharmaceutical_substance|pharmaceutical_substance]], [[V2 Table product_presentation|product_presentation]].

This view is a query projection over implemented tables; it does not create new ontology semantics.

## v_observations

**Referenced tables:** [[V2 Table dataset|dataset]], [[V2 Table dataset_release|dataset_release]], [[V2 Table diagnosis_reference|diagnosis_reference]], [[V2 Table facility|facility]], [[V2 Table geography|geography]], [[V2 Table medicinal_product|medicinal_product]], [[V2 Table observation_result|observation_result]], [[V2 Table product_presentation|product_presentation]], [[V2 Table source_record|source_record]].

This view is a query projection over implemented tables; it does not create new ontology semantics.

## v_provenance_lineage

**Referenced tables:** [[V2 Table assertion|assertion]], [[V2 Table dataset|dataset]], [[V2 Table dataset_release|dataset_release]], [[V2 Table evidence_support|evidence_support]], [[V2 Table source_record|source_record]], [[V2 Table transformation_run|transformation_run]].

This view is a query projection over implemented tables; it does not create new ontology semantics.

## v_entity_matches

**Referenced tables:** [[V2 Table entity_match_assertion|entity_match_assertion]], [[V2 Table source_record|source_record]].

This view is a query projection over implemented tables; it does not create new ontology semantics.

## Authority
- v2/data/db/views.sql
- v2/data/db/schema.sql



---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 SQL views and DDL
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #236, #237
- **Evidence status:** Query views documented separately from the 24-table count
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
