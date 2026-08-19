# W3 — Evidence-Driven Concept & Relation Discovery

## Status
Active on `v2/w3-concept-discovery`.

## Objective
Build the pre-UFO CM-PharmE 2.0 concept/relation inventory from the frozen V1 lineage and Gate C-approved discovery sources, while keeping protected held-out sources out of Core concept admission.

## Discovery inputs
- CM-PharmE 1.x concept/relation lineage.
- P1/P2 NHIF DOI-backed empirical anchors.
- P3 FDA DECRS + WDD/3PL.
- P4 openFDA NDC + FDA/openFDA SPL.
- P5 EMA Critical Medicines + EMA shortage JSON/reporting evidence.
- P6 WHO Model List/eEML.
- P7 GeoNames for normalization only.
- C1 supply-operations dataset metadata/schema where permitted; no public raw redistribution.
- C2 EudraGMDP public semantic/schema evidence; no unverified automated ingestion.
- S1/S2/S3 only where their approved enrichment/extension role applies.

## Protected held-out boundary
W3 does **not** use H1 ClinicalTrials.gov/AACT, H2 openFDA Drug Shortages, or H3 selected national EML schemas to justify admission of Core concepts or relations. Their existence/access feasibility is known from W2, but their schemas are reserved for W7 generalizability tests.

## Discovery workflow
1. Extract source-level candidate concepts and relationship structures.
2. Normalize synonyms and distinguish entities, roles, sites, events, observations, classifications and identifiers.
3. Separate geography, jurisdiction and temporal context.
4. Establish evidence/provenance and entity-resolution semantics.
5. Reconcile each V1 concept with the new evidence.
6. Build evidence→candidate traceability.
7. Apply explicit admission rules: Core / Extension / Cross-cutting Infrastructure / Deferred / Rejected.
8. Stop at the Concept Inventory Gate before final UFO/OntoUML stereotyping.

## Methodological boundary
Candidate UFO interpretations recorded in W3 are hypotheses for W4, not final stereotypes. W3 decides *what needs to be conceptualized and why*; W4 decides *what those candidates ontologically are* under UFO/OntoUML.
