# Cross-Version Comparison Limits

> **Page scope:** Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative sources:** V1/V2 version, migration and Gate-F evidence  
> **Last synchronized:** 2026-09-23  
> **Related issues/PRs:** #104, #159, #206  
> **Evidence status:** Mandatory interpretation boundary  
> **Future refresh:** #213 and #214  
> **Wiki baseline:** WB-2026.09.1 Candidate

## Purpose

V1 and V2 can be compared descriptively, but several apparently simple numeric comparisons are methodologically invalid.

## Concept-count limitation

V1 has 39 canonical concepts; V2 Gate D has 87 conceptual elements.

This does **not** establish that V2 is “123% more complete” or any similar coverage conclusion.

Reasons:
- V2 uses finer semantic granularity;
- V2 includes first-class X-INFRA concepts absent from V1's architecture;
- several V1 generic concepts are split;
- V2 isolates extensions explicitly;
- the studies do not share a common universe/denominator of “all pharmaceutical concepts.”

## Domain-count limitation

V1 has five broad modeling domains; V2 has 17 canonical domains/modules.

Domain count reflects architecture, not quality or coverage.

## Evaluation-count limitation

V1 and V2 evaluation frameworks differ in structure, timing, datasets and purpose. A greater number of evaluation families in V2 is not itself evidence of better ontology quality.

## Coverage limitation

Gate F explicitly narrows the claim of broader ecosystem coverage. V2 may describe:
- qualitative/design expansion;
- measured coverage against its own frozen source requirements;
- held-out results for selected source families.

It must not claim a like-for-like V1→V2 percentage improvement because the common quantitative denominator does not exist.

## Data-grounding limitation

V2 uses a larger and more formalized data/evidence strategy. That supports a different evidence architecture; it does not retroactively invalidate V1's literature- and model-grounded design.

## Formalization limitation

V1 and V2 formal graphs, shapes, checks and fingerprints are generated under different model versions and engineering scopes. Raw triple/property/shape counts are not direct quality metrics.

## Application limitation

V2 implements more explicit demonstrators, but representative-task execution is bounded. Successful task execution does not prove production effectiveness, universal usability or global completeness.

## Human-evidence limitation

V1 has publication/expert evidence in its own study lineage. V2 E9 is still readiness-only with 0 real responses. No cross-version expert-validation ranking is justified.

## Valid comparison dimensions

Useful comparisons include:
- documented conceptual distinctions;
- architecture/modularity changes;
- evidence/admission process;
- provenance and traceability mechanisms;
- formal/representation architecture;
- evaluation design;
- documented limitations;
- migration decisions.

These should be presented descriptively with evidence, not converted into a synthetic overall score.

## Evidence

- [V1 version record](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/versions/v1.0.0.md)
- [V2 W3 migration matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w3/v1-v2-migration-matrix.md)
- [Gate D](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/gate-d-conceptual-freeze.md)
- [Gate F](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/gate-f-claim-sufficiency-decision.md)
