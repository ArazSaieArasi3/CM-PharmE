# W2 Dataset Admission and Scoring Rubric

## Purpose
Make dataset/source selection explicit before W3 concept discovery. The rubric reduces cherry-picking and separates scientific authority from practical usability.

## Weighted criteria (100 points)
| Criterion | Weight | Question |
|---|---:|---|
| Stable identity / authority | 10 | Is there a DOI/version/accession or a clearly authoritative maintained source? |
| Legal reuse clarity | 12 | Are reuse, redistribution and derivative-use terms explicit enough for the intended role? |
| Reproducible access | 10 | Is data downloadable/API-accessible in a way that can be versioned or reproduced? |
| Schema / data dictionary | 10 | Are fields, structure, types and semantics documented? |
| Provenance / source quality | 8 | Is the origin, maintainer and transformation history sufficiently clear? |
| Geographic usefulness | 8 | Does it provide location/jurisdiction coverage relevant to V2? |
| Temporal coverage/versioning | 6 | Are dates, update frequency, history or snapshot versions available? |
| Identifier/linkability quality | 10 | Are stable entity/product/site identifiers or credible crosswalk fields present? |
| Relationship richness | 10 | Does the source expose relations/events rather than only flat labels? |
| Gate B demonstrator fit | 12 | Can it materially support A, B or C? |
| Reproducibility packaging | 4 | Can exact inputs/snapshots/checksums be recorded and rebuilt? |

## Hard exclusion / non-admission conditions
A source is not admitted as a primary W3/W6 dataset when any of the following applies:
1. no accessible data are available beyond a narrative publication;
2. access is restricted and permission has not been obtained;
3. reuse terms are incompatible with the intended analysis/publication role;
4. a primary benchmark has no stable version/snapshot strategy and cannot be reproduced;
5. raw data include patient-identifiable or otherwise unsuitable information for the planned open research workflow;
6. the source cannot be meaningfully related to the V2 research questions or approved demonstrators.

A source may still be retained as **methodological/schema evidence** when it is authoritative but not a redistributable empirical dataset.

## Score interpretation
- **85–100 — Strong admission:** primary implementation/discovery or strong secondary source, subject to role separation.
- **75–84 — Admit with bounded role:** secondary, enrichment, or conditional primary depending the specific weakness.
- **65–74 — Conditional/exploratory:** may inform feasibility; do not make it a central empirical anchor without resolving the weakness.
- **<65 — Not admitted to W3/W6:** future opportunity or reference only.

## Role labels
A high score does not imply every role. Each admitted source receives one or more explicit roles:
- **Discovery** — may inform concepts/relations.
- **Implementation** — may be ingested/mapped in W6.
- **Evaluation** — used to test mappings/queries/data conformance.
- **Held-out** — deliberately excluded from Core concept discovery and reserved for external/generalizability evaluation.
- **Enrichment** — identifier/geography/terminology enhancement only.
- **Methodological / schema evidence** — authoritative evidence that informs design but is not treated as an empirical dataset.

## Held-out rule
A held-out source may be profiled for feasibility in W2, but W3 may not mine it to admit Core classes/relations. If W3 later needs concepts found only in a held-out source, that fact must be recorded and the source loses its clean held-out status for those concepts.

## Licensing rule
Downloadability is not permission to redistribute. W6 will preserve source URLs/DOIs, versions and checksums and will only commit raw/derived data when the source terms explicitly permit that action. Conditional data can be accessed through local ETL instructions without copying raw files into the public release.
