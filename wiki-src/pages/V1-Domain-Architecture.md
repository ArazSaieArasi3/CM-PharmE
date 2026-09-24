# V1 Domain Architecture

> **Version scope:** V1  
> **Status:** Stable  
> **Updated:** 2026-09-23

## Five-domain architecture

CM-PharmE v1.0.0 organizes the conceptual model into five architectural domains.

| Domain | Primary concepts | All mapped concepts |
|---|---:|---:|
| Organizational / Structural | 8 | 11 |
| Ecosystem / Collaborative | 9 | 13 |
| Operational / Process | 8 | 19 |
| Governance / Regulatory | 7 | 13 |
| Digital Transformation | 7 | 7 |

The difference between primary and all-mapped counts is intentional: a concept has one primary domain but can have cross-domain memberships.

## Domain intent

### Organizational / Structural
Internal organization structures, identity-bearing enterprise concerns and internal organizational participation.

### Ecosystem / Collaborative
External ecosystem participation, collaboration, partnership and inter-organizational relationship concerns.

### Operational / Process
Activities, processes and operational dynamics unfolding across the ecosystem.

### Governance / Regulatory
Governance, policy, compliance, regulatory relationships and constraints.

### Digital Transformation
Digital enablement, information exchange, platform/data and transformation concerns.

## Why separate domains?

The decomposition is design-oriented rather than a claim that the pharmaceutical ecosystem “naturally” consists of exactly five universal categories. It separates concerns that carry different identity, dependence, process and mediation semantics while retaining cross-domain links.

## Important boundary

These domains are conceptual-modeling domains. They are **not** automatically DDD bounded contexts, software services, microservices or organizational business units.

## Evidence and navigation

- [Domain index](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/domains/index.md)
- [Concept-domain mapping](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/mappings/concept-domain.csv)
- [V1 version statistics](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/versions/v1.0.0.md)
- [Historical domain view](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/releases/v1.0.0/model/Domains-of-CM-PharmE-1.0.png)

## Evolution note

V2 does not automatically preserve this five-domain decomposition as its Core architecture. The V1 domains remain important historical and analytical anchors, while V2 re-evaluates modular structure from new evidence and UFO/OntoUML analysis.

See [[V1 to V2 Domain Evolution]].

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V1
- **Documentation maturity:** Stable
- **Authoritative source:** `main/docs/domains/` and V1 catalogs/mappings
- **Last synchronized:** 2026-09-23
- **Last synchronized ref:** `5099888668d35f798e4759e3534e707ed906db24`
- **Related issues/PRs:** V1 domain normalization/evaluation lineage
- **Evidence status:** Stable V1 architecture
- **Future refresh:** None planned for frozen V1 baseline
- **Wiki baseline:** WB-2026.09.1

</details>
