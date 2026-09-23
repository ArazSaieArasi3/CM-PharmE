# V2 Observatory and Demonstrators

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** V2 W8 artifacts and live issue state  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** #22, #143, #145, #147, #149, #151, #153, #169, #170  
> **Evidence status:** 7/8 W8 work items complete; representative-task evaluation incomplete  
> **Future refresh:** #212  
> **Wiki baseline:** WB-2026.09.1 Candidate

## Purpose

The Observatory demonstrates selected ontology/data capabilities without turning the research program into an unconstrained software product.

## Article-scope capabilities

The architecture covers:
- actor/facility map;
- entity/relationship browsers;
- KG exploration;
- bounded analytics;
- resilience/risk scenarios;
- provenance-aware semantic search.

Each capability must preserve semantic identity and provenance.

## Current W8 status

Live child-issue state on 2026-09-23:
- V2-076 design: complete;
- V2-077 actor/facility map: complete;
- V2-078 browsers: complete;
- V2-079 KG explorer: complete;
- V2-080 analytics: complete;
- V2-081 resilience/risk view: complete;
- V2-082 provenance-aware semantic/search assistance: **complete (#169 closed)**;
- V2-083 representative-task evaluation: **open (#170)**.

Therefore W8 is **7/8 complete**. Older parent-Epic text showing 6/8 is stale.

## Representative-task evidence at authoritative branch ref

The current merged V2 branch records:
- 6 PASS;
- 0 PARTIAL;
- 0 FAIL;
- 3 NOT_EXECUTED.

The missing tasks remain explicit. Open/unmerged work is not promoted to stable evidence.

## Application boundaries

Demonstrators do not establish:
- universal usability;
- production readiness;
- global pharmaceutical-market completeness;
- predictive/causal resilience validity;
- clinical/regulatory effectiveness;
- real-world entity-resolution accuracy;
- general AI novelty/performance.

## Product boundary

Multi-tenancy, enterprise auth, commercial feeds, predictive risk engines, operational SLAs, monetization and enterprise workflows are future product possibilities, not requirements/evidence for the principal ontology paper.

## Evidence

- [Observatory design](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w8/observatory-design.md)
- [Representative task suite](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/app/observatory/representative-task-suite.md)
- [Current merged task results](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/app/observatory/representative-task-results.md)
- [Semantic search](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/app/observatory/semantic_search.py)
