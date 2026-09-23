# Reproducibility Guide

> **Page scope:** Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative sources:** V1 build/validation assets; V2 E13/W5/W6/W7 reproducibility assets  
> **Last synchronized:** 2026-09-23  
> **Related issues/PRs:** V1 engineering closure; V2 #102, #207, #217  
> **Evidence status:** Repository-level computational reproducibility documented for selected V1/V2 scopes  
> **Future refresh:** #214 and #217  
> **Wiki baseline:** WB-2026.09.1 Candidate

## What reproducibility means here

CM-PharmE uses reproducibility to mean that declared computational artifacts/checks can be regenerated or re-executed from controlled source, tooling and evidence.

This is different from:
- independent third-party scientific replication;
- expert validation;
- empirical proof of domain completeness;
- production-scale operational replication.

## V1 reproducibility path

V1 supports:
- deterministic ontology graph reconstruction;
- serialization generation/equivalence checks;
- SHACL execution;
- competency-query regressions;
- ROBOT metrics/profile assessment;
- HermiT logical reasoning;
- graph fingerprints;
- dual-build byte checks;
- deterministic release packaging.

Primary guides:
- [Build](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/engineering/BUILD.md)
- [Validation](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/engineering/VALIDATION.md)
- [Release readiness](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/engineering/release-readiness.md)

## V2 reproducibility path

V2 E13 performs a clean rebuild of the computable W5–W7 evidence.

Current evidence includes:
- 54/54 aggregate checks;
- V2 ontology fingerprint reproduced;
- PostgreSQL/PostGIS bootstrap;
- deterministic W6 KG regeneration;
- KG fingerprint reproduced;
- 4/4 SQL↔SPARQL benchmark regeneration;
- executable E1–E8 and E10–E12 evidence regeneration.

Human E9 is intentionally excluded because real human responses cannot be fabricated by a build pipeline.

Primary evidence:
- [E13 report](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/e13-reproducibility-independent-rebuild.md)
- [E13 baseline](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/evaluation/protocol/e13-reproducibility-baseline.json)
- [W5 closure](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w5/W5-CLOSURE.md)
- [W6 closure](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w6/W6-CLOSURE.md)

## Reproducibility checklist for a researcher

For a reproducible citation/use:
1. identify V1 or V2;
2. record semantic/model version;
3. record repository ref/commit;
4. identify input/source fixtures or datasets;
5. use documented tooling/environment;
6. retain generated manifests/fingerprints;
7. record warnings and negative findings;
8. distinguish computed evidence from human evidence.

## Wiki reproducibility

The Wiki itself has a separate reproducibility layer:
- source-controlled pages under `wiki-src/`;
- page inventory;
- baseline manifest;
- automated documentation QA;
- actual GitHub Wiki publish verification (#218);
- source snapshot/archive procedure (#217).

A Wiki source commit is not a substitute for a research model release, and a Wiki baseline identifier is not a semantic version.

## Related pages

[[V1 Reproducibility]] · [[V2 Reproducibility and Release Plan]] · [[Wiki Versioning and Lifecycle]]
