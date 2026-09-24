# CM-PharmE 2.0 Semantic Review

> **Version scope:** V2  
> **Status:** Semantic review in progress / Stable-to-date infrastructure  
> **Updated:** 2026-09-23

## Purpose

Formal validation and automated evaluation do not replace expert semantic inspection. The Semantic Review layer gives the author/reviewer a controlled path to inspect the complete V2 ontology, evidence and V1→V2 decisions before final publication/release.

The repository retains the historical/internal Human Ontology Review naming in some artifact paths. The Wiki uses **Semantic Review** as the reader-facing term.

## Phase 1 — complete

Merged review infrastructure includes:
- Semantic Review Control Center;
- whole-ontology overview covering 87 concepts / 17 domains;
- domain catalog;
- concept review catalog with domain, stereotype, layer, review status and evidence anchor.

These pages are review projections, not new semantic authorities.

## Phase 2 — active

Planned/active work includes:
- one Concept Evidence Passport per concept;
- direct concept-page evidence links;
- relation catalog and relation review records;
- V1→V2 Version Evolution Review Package;
- Ontology Evaluation Diagnostic Report over E1–E13;
- structured semantic-review finding register and re-review workflow.

## Concept provenance matrix

#159 requires each final V2 concept to document:
- canonical name/stereotype;
- working semantic commitment;
- V1 predecessor(s);
- migration treatment;
- dataset/authoritative evidence;
- held-out evidence where applicable;
- non-dataset supporting sources;
- formal implementation location/IRI;
- explicit evidence gaps.

Missing evidence is marked as a gap, not invented.

## Semantic safety rule

Review documentation may propose or record findings, but a semantic change becomes canonical only after explicit author disposition and merge into the V2 authority branch.

## Evidence

- [Semantic Review Control Center — repository path retains historical naming](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/README.md)
- [Whole-ontology overview](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/ontology-overview.md)
- [Domain review index](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/domains/index.md)
- [Concept review index](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/concepts/index.md)
- [Concept provenance matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/human-review-concept-provenance-matrix.md)

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Semantic review in progress / Stable-to-date infrastructure
- **Authoritative source:** `v2/review/` and review issues #159/#173
- **Last synchronized:** 2026-09-23
- **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- **Related issues/PRs:** #159, #173, PR #174
- **Evidence status:** Phase 1 review infrastructure complete; Phase 2 active
- **Future refresh:** #213
- **Wiki baseline:** WB-2026.09.1

</details>
