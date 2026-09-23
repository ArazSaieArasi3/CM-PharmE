# V2 Reproducibility and Release Plan

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** E13 reproducibility evidence, V2 paper/release program  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** #23, #102, #171, #214, #217  
> **Evidence status:** Computational reproducibility established for current evaluated scope; final research release/DOI not yet frozen  
> **Future refresh:** #214  
> **Wiki baseline:** WB-2026.09.1 Candidate

## E13 reproducibility evidence

The V2 computational pipeline records:
- clean rebuild of W5/W6/W7 computable evidence;
- 54/54 aggregate checks passing;
- reproduced ontology fingerprint;
- reproduced KG fingerprint;
- repeated deterministic serialization/manifests;
- PostgreSQL/PostGIS bootstrap;
- regenerated W6 validation and 4/4 SQL↔SPARQL benchmark evidence;
- regeneration of executable E1–E8 and E10–E12 evidence.

Human E9 evidence is intentionally excluded from automated rebuild.

## Interpretation boundary

This is repository-level computational reproducibility. It is not:
- independent third-party replication;
- expert validation;
- proof of external-source completeness;
- production reproducibility at arbitrary scale.

## Final research-release plan

The Paper Track still requires:
1. complete current manuscript integration;
2. complete W8/Gate G evidence as applicable;
3. truthful final disposition of E9;
4. target-journal decision;
5. final manuscript↔repository↔data traceability audit;
6. final research package;
7. DOI/release decision;
8. Gate H freeze.

No DOI, GitHub Release or final release identifier should be invented before it actually exists.

## Wiki relationship

At final freeze:
- the V2 research/model release and Wiki baseline remain distinct identifiers;
- the exact Wiki commit/ref must be archived;
- citation guidance must point to the actual final research package;
- #214 and #217 coordinate final documentation freeze and snapshot.

## Evidence

- [E13 report](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/e13-reproducibility-independent-rebuild.md)
- [E13 manuscript evidence](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/manuscript/w7-e13-reproducibility-evidence.md)
- [Paper/release program](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/README.md)
