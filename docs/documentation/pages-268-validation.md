# PAGES-01 Validation and OGCM-RF #71 Conformance

Issue: #268  
Parent: #267  
Status target: PASS for the authority/version-registry contract.

## Executable checks

The project-local registry validator and negative-test harness cover:

1. baseline V1/V2 registry validation;
2. exact SHA-bound source refs;
3. lifecycle-specific route requirements;
4. hypothetical V3 onboarding through one registry entry and the common pipeline contract;
5. route-collision rejection;
6. stable V1 immutable-route mutation rejection;
7. stable V1 exact-source-ref rebinding rejection;
8. stable V1 entry-removal rejection.

The V3 entry is synthetic test data only, has generated-reference/WebVOWL publication disabled, and is never added to the production registry.

## Downstream-consumption proof

`tools/pages/plan_pages_build.py` consumes the registry through the same validator/resolver and produces the build plan for enabled versions. This prevents the registry from becoming documentation-only metadata.

Current production plan resolves:
- V1 → `ontology/v1.0.0/`
- V2 → `ontology/v2/current/`

## OGCM-RF #71 conformance mapping

| OGCM-RF #71 requirement | CM-PharmE disposition |
|---|---|
| Semantic Source defines | PASS — canonical ontology/evidence roots declared |
| Wiki explains | PASS — `wiki-src/` declared curated source |
| Pages exposes generated reference | PASS — generated-output roles declared; deployment remains downstream |
| Generated reference is not authority | PASS — explicit allocation/duplication rules |
| WebVOWL is exploratory | PASS — Pages role only; formal authority remains source |
| Exact source/ref binding | PASS — 40-char commit SHA required by validator |
| Current vs immutable paths | PASS — V1 immutable, V2 evolving/current |
| Historical overwrite prohibited | PASS — policy + baseline guard |
| Future versions use same architecture | PASS — V3 dry-run through registry/common pipeline |
| Public sensitive-content boundary | PASS at contract level — actual public-output review remains #275/#278 |
| Rendered Pages verification | DEFERRED — #275/#278 because Pages is not deployed yet |
| Wiki↔Pages backlinks | DEFERRED — #274 after public routes exist |

## Disposition

**PASS for #268 contract scope.**

The deferred rendered-publication and backlink checks are not #268 failures; they belong to the explicitly dependent deployment/integration issues. R0 still requires #269 before it can pass.
