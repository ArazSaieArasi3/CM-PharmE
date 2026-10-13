# Bounded Product Knowledge case explorer

This static, read-only viewer displays the **synthetic** Productium case fixture for an Explorer concept informed by [CM-PharmE research](https://doi.org/10.1109/ICAEA69058.2025.11301544). The cited publication describes CM-PharmE v1. The fixture's external identifiers point separately to a later *research snapshot* in the CM-PharmE repository; that snapshot is not described here as a published v2 release.

This is an application slice of the Product Ontology case. It is distinct from the CM-PharmE W8 Observatory, which explores CM-PharmE's own ontology and admitted ecosystem evidence. The two graph browsers must not be counted as one evaluated product.

## Run

From this directory, run `python3 -m http.server 8000`, then open `http://localhost:8000`. The app reads `data/CASE_INSTANCE_GRAPH.nt` and supports entity/type search, incoming and outgoing relation traversal, asserted type inspection, and source visibility. It requires no backend and makes no remote API calls; external source links are opened only if selected. Run `node test.mjs` for fixture/parser checks.

## Evidence boundary

- The immutable fixture contains **197 asserted triples**, **52 product-knowledge entities**, and **15 external-domain entities**. Every subject has an asserted `dct:source` value. Its SHA-256 is `4ad7041ebbaadc5b426f29d585f3afdd39b64fd32a4691ac17dc1f9f6a60b907`.
- Product-knowledge source values name `CASE_CONTRACT.yaml`, an internal case-construction source that is **not distributed in this viewer**. A source label is not independent corroboration. External-domain source values point to a pinned CM-PharmE research snapshot.
- The viewer offers retrieval and traversal of already asserted fixture edges. It does not run a reasoner, SHACL validator, competency-question suite, SQL reconstruction, or human study. Earlier case checks retained in the Product Ontology research record have separate input/result identities and limits; loading this viewer is not a fresh rerun of those checks.
- No live pharmaceutical data, full global ecosystem coverage, user effectiveness, deployment, or real-world product validation follows from this demonstration.

This directory contains application code and a synthetic fixture, **not the conference manuscript**. Keep manuscript claims and any later release/DOI decision in the owning paper workflow.
