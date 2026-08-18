# W2 — Dataset Landscape, Admission and Held-out Evaluation Design

## Status
Implementation in progress on `v2/w2-data-landscape`.

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

Cross-source entity resolution may be promoted only if overlapping identifiers/records allow construction of a defensible gold subset.

## Methodological rule
Held-out sources are reserved before W3 concept discovery. They may be profiled for feasibility, but their schemas must not be used to admit Core concepts that will later be claimed as externally validated by those same sources.
