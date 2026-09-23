# V1 to V2 Domain Evolution

> **Page scope:** Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **V1 authority:** `main/docs/domains/`  
> **V2 authority:** V2 canonical domain taxonomy  
> **Last synchronized:** 2026-09-23  
> **Related issues/PRs:** #154, #159, #173, #206  
> **Evidence status:** V1 five-domain and current V2 17-domain taxonomies are stable at their selected baselines  
> **Future refresh:** #213 if human review changes domain placement  
> **Wiki baseline:** WB-2026.09.1 Candidate

## V1 architecture

V1 has five modeling domains:

| V1 domain | Primary concepts | All mapped concepts |
|---|---:|---:|
| Organizational / Structural | 8 | 11 |
| Ecosystem / Collaborative | 9 | 13 |
| Operational / Process | 8 | 19 |
| Governance / Regulatory | 7 | 13 |
| Digital Transformation | 7 | 7 |

These are modeling domains with cross-domain membership, not DDD bounded contexts.

## V2 architecture

V2 uses a modular taxonomy of **17 domains**:

### Core — 6 domains
- Ecosystem Organization — 8 concepts
- Facility Operations — 4
- Regulatory Governance — 3
- Pharmaceutical Product — 10
- Supply Operations — 4
- Ecosystem Observation — 3

### X-INFRA — 3 domains
- Spatiotemporal Context — 7
- Evidence Traceability — 13
- Entity Identity — 5

### Extensions — 8 domains
- Regulatory Policy — 2
- Supply Resilience — 11
- Market Access — 3
- Risk Management — 5
- Pharmacovigilance — 3
- Business Architecture — 4
- Digital Systems — 1
- Clinical Care — 1

Total: 87 conceptual elements.

## Why there is no one-to-one domain mapping

V1 domains organize broad ecosystem concerns. V2 domains/modules reflect a different research purpose: finer identity/dependence distinctions, explicit cross-cutting infrastructure and optional extension isolation.

Therefore:
- Organizational/Structural concerns contribute strongly to Ecosystem Organization and Facility Operations.
- Governance/Regulatory concerns split between Regulatory Governance, Regulatory Policy and jurisdictional infrastructure.
- Operational/Process concerns distribute across Supply Operations, Observation and extension activities.
- Ecosystem/Collaborative concerns are represented through roles, relators, supply dependencies and extension relationships rather than one preserved domain.
- Digital Transformation no longer defines a broad Core domain; durable evidence/provenance/identity infrastructure becomes X-INFRA while technology-specific digital semantics are isolated in Digital Systems.
- Business Architecture becomes an Extension rather than a Core decomposition principle.

## Architecture versus software boundary

Neither V1 domains nor V2 ontology domains are automatically deployable services or DDD bounded contexts. A separate DDD/software-architecture analysis may map them, but that is a different design decision.

## Naming normalization

V2 domain names use cohesive semantic noun phrases rather than labels joined with `&` or `/`. This naming normalization does not itself alter ontology semantics.

## Research interpretation

The change from five domains to 17 domains should be described as architectural refinement/restructuring for V2's data-grounded ontology objectives—not as a numeric proof that V2 has “more coverage.”

## Evidence

- [V1 domain index](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/domains/index.md)
- [V2 canonical domain taxonomy](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/domain-taxonomy.md)
- [V2 integrated conceptual model](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/integrated-ontouml-model.md)
