# W7-E7 Manuscript Evidence Note — Source-Semantic Coverage

## Safe result statement
Across 97 normalized semantic requirements extracted from the admitted discovery, conditional and secondary source families, CM-PharmE 2.0 exactly represented 74 (76.29%) and represented a further 14 at bounded/partial granularity, for 88/97 (90.72%) represented-or-partial requirements. Nine source semantics remained explicitly not represented. Concept requirements were 48/63 exact and 55/63 represented-or-partial; relation requirements were 26/34 exact and 33/34 represented-or-partial.

## Module-evidence statement
Fifty-four of the 87 Gate-D conceptual elements were directly evidenced by at least one requirement in the evaluated source-semantic registry: 24/32 Core, 14/25 cross-cutting infrastructure and 16/30 Extension elements. This is a source-evidence coverage descriptor, not an ontology-completeness score.

## Important gaps retained
The first-pass registry retains nine not-represented semantics: route of administration; product-label artifact; alternative geographic name; reorder/stock policy; GMP/GDP certificate/status; substance synonym; exceptional funding decision/record; funding-organization→access-decision relation; and an explicit adverse-event case/event type.

One critical requirement is partial rather than exact: the outpatient observation→administrative-region association is represented in the W6 reference KG with external `dct:spatial`, but no dedicated CM-PharmE internal property currently expresses that association.

## V1 comparison
Use the W3 V1→V2 migration matrix for continuity and novelty accounting. Do not report a numerical V1-vs-V2 source coverage improvement percentage because no equivalent frozen V1 source-semantic requirement registry exists. A defensible statement is that the W3 migration analysis documents ten material V2 advances, including Organization/Role/Facility separation, explicit product-substance-presentation semantics, jurisdiction/geography/time, contextual essential/critical classification, shortage/observation semantics, provenance, and identifier/entity-match infrastructure.

## Claim boundaries
Do not state that:
- 90.72% is global pharmaceutical-domain completeness;
- the remaining 9 semantics are absent from the domain;
- discovery-source coverage demonstrates cross-jurisdiction generalizability;
- all 87 ontology elements require direct dataset-schema evidence;
- the held-out sources were used in E7.

Held-out H1 ClinicalTrials.gov/AACT, H2 openFDA Drug Shortages and H3 reserved national EML schemas remain untouched until W7-E8.

## Evidence
GitHub Actions run `32366637722`: SUCCESS. Artifact `9405520553`, digest `sha256:e0080b5a074bcf36a39c5ac353d86beba89dd49e84c48a357ab43731871fc70e`.
