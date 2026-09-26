# WIDOCO Adapter — CM-PharmE

Issue: #271  
Parent: #267  
Normative adapter: OGCM-RF WIDOCO + Static Pages Publication Adapter.

## Pinned tool
- WIDOCO: **1.4.25**
- Release asset: `widoco-1.4.25-jar-with-dependencies_JDK-17.jar`
- SHA-256: `be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b`
- Java: 17

The workflow downloads the exact release asset and rejects it before execution if the checksum differs.

## Governed inputs
WIDOCO never receives an arbitrary ontology file. The candidate workflow first rebuilds V1 and V2 from the exact #269 source bindings and runs the existing documentation-input publication gate.

V1 target:
`/ontology/v1.0.0/reference/`

V2 current target:
`/ontology/v2/current/reference/`

## Feature boundary for this issue
Enabled:
- exhaustive WIDOCO/LODE reference generation;
- metadata/configuration;
- annotation-property inclusion;
- provenance support from WIDOCO;
- single-document rendering for robust static/local QA.

Deferred:
- WebVOWL → #272;
- OOPS diagnostics → broader evaluation/quality workflow, not treated as reference authority;
- public GitHub Pages deployment/render verification → #275;
- Apache `.htaccess` / server-side content negotiation → not claimed on GitHub Pages.

## Generated-content rule
Generated HTML is disposable build output and MUST NOT be manually edited. Curated research narrative remains in the Wiki. Short WIDOCO intro fragments exist only to disclose lifecycle, source ref, authority boundary and cross-surface links.

## Slice status
This first #271 slice establishes the pinned adapter and proves that V1 and V2 reference candidates can be generated from governed inputs. Exhaustive entity coverage, broken-link/asset audit and regeneration comparison remain the next bounded slice before #271 can close.
