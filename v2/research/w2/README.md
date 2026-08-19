# W2 — Dataset Landscape, Admission and Held-out Evaluation Design

## Status
**IMPLEMENTATION COMPLETE — Gate C ready for decision.**

## Objective
Build a broad pharmaceutical data landscape, verify DOI/stable identifiers, legal reuse, access, schema, provenance, geography, temporal coverage and relation richness, and select a deliberately mixed portfolio for:
- W3 evidence-driven concept/relation discovery;
- W6 ontology-aligned RDB/KG implementation;
- W7 held-out/cross-jurisdiction evaluation;
- Gate B demonstrators A/B/C.

## Gate B constraints carried forward
A. Global Actor/Facility Geospatial Integration
B. Critical Medicine Supply Vulnerability & Resilience
C. Ontology↔RDB↔KG Consistency & Provenance

## Gate C proposal
Primary discovery/implementation combines two DOI-backed NHIF empirical anchors with FDA/openFDA, EMA, WHO and GeoNames operational/reference sources. The pharmaceutical supply dataset DOI 10.5281/zenodo.18851842 is conditional because redistribution rights are not expressed through a standard open-data license. ClinicalTrials.gov/AACT and openFDA Drug Shortages are protected held-out source families before W3 concept discovery.

## Methodological rule
Held-out sources may be profiled for feasibility, but their schemas must not be used to admit Core concepts that will later be claimed as externally covered. Approval of Gate C freezes source roles/held-out boundaries, not the V2 ontology.
