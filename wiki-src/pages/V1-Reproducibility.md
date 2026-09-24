# V1 Reproducibility

> **Page scope:** V1  
> **Documentation maturity:** Stable  
> **Authoritative source:** V1 build/validation/CI artifacts on `main`  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `5099888668d35f798e4759e3534e707ed906db24`  
> **Related issues/PRs:** V1 engineering/reproducibility closure  
> **Evidence status:** Repository-level reproducibility for supported computational checks  
> **Future refresh:** None unless V1 build evidence is corrected  
> **Wiki baseline:** WB-2026.09.1

## Reproducibility objective

The V1 repository separates authoritative source from generated artifacts and makes supported checks repeatable through deterministic build/validation controls.

## Reproducible elements

The repository documents:
- deterministic reconstruction of the canonical ontology graph;
- serialization generation and equivalence checks;
- SHACL validation;
- positive and negative competency-query regressions;
- ROBOT metrics/profile assessment;
- HermiT logical reasoning;
- graph fingerprints;
- dual-build byte reproducibility;
- deterministic release ZIP/integrity evidence.

## What reproducibility means here

A successful repository rebuild shows that the encoded computational pipeline can reproduce its declared artifacts/results under the supported environment.

It does **not** by itself mean:
- independent third-party scientific replication;
- empirical validation of all domain claims;
- proof of universal completeness;
- deployed production validation.

## How to inspect

- [Build guide](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/engineering/BUILD.md)
- [Validation guide](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/engineering/VALIDATION.md)
- [Release readiness](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/engineering/release-readiness.md)
- [Ontology source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/ontology/README.md)
- [Evaluation assets](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/evaluation/README.md)

## Reuse discipline

When citing or reusing V1, identify the semantic/model release and, where reproducibility matters, the repository ref or release artifact used.
