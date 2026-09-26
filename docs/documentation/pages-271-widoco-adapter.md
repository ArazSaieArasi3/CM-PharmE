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

## Acceptance status

#271 is accepted when the CI evidence remains green for both current supported version families.

Verified on the closeout run:
- V1 canonical research inventory: 39 classes and 39 object properties; helper/meta OWL entities are reported separately rather than miscounted as domain concepts.
- V1 generated coverage: 42/42 declared OWL classes, 41/41 declared object properties, 0/0 datatype properties.
- V2 generated coverage: 81/81 classes, 52/52 object properties, 5/5 datatype properties.
- local broken links/assets: 0 for V1 and 0 for V2.
- independent regeneration comparison: 22/22 generated files byte-identical for V1 and 22/22 byte-identical for V2.
- volatile-field ignore rules: none required.

## Known adapter limitations and boundaries

1. **Static publication only.** GitHub Pages is treated as static hosting. Apache `.htaccess` behavior and HTTP content negotiation are not claimed.
2. **Generated reference, not semantic authority.** WIDOCO/LODE output is a projection of governed ontology inputs. Canonical source modules and their validation evidence remain authoritative.
3. **WebVOWL is separate.** Interactive visualization is intentionally implemented and governed under #272, not conflated with this formal-reference adapter.
4. **OOPS is not an authority gate here.** OOPS integration is not enabled by this adapter and cannot substitute for repository-native validation, reasoning, SHACL, or claim-boundary evidence.
5. **External rendered links are deferred.** Candidate QA proves local HTML/CSS target integrity. Public HTTP(S), browser-rendered routes and deployed-asset checks belong to #275.
6. **V1 inventory layering is explicit.** The canonical research inventory is 39 concept classes and 39 relation object properties, while the formal graph also contains 3 meta/helper classes and 2 meta/helper object properties. Both layers are exposed; they are not conflated.
7. **V1 datatype-property authority is not invented.** The exact-ref V1 validation report does not freeze an independent datatype-property count; the current governed input contains zero and that fact is reported without promoting it into a new historical claim.
8. **V2 is evolving.** V2 output remains Stable-to-date / Evolving and must not be cited as a frozen `v2.0.0` release until the separate semantic release event occurs.
9. **Adapter compatibility normalization is deterministic.** WIDOCO relative semantic IRIs/backslash backlinks are normalized automatically by the adapter. Manual generated-HTML maintenance remains prohibited.
10. **Toolchain pinning is part of reproducibility.** Rebuild evidence is valid for the pinned WIDOCO 1.4.25 / JDK 17 adapter and exact source/config refs. Tool upgrades require a new governed comparison.

## Reproducibility interpretation

The closeout workflow performs two independent candidate generations from the same governed inputs and compares the resulting candidate trees byte-for-byte. The accepted closeout run required **no volatile-field allowlist**: both V1 and V2 regenerated as 22 identical files with zero differing paths and zero differing hashes.

This establishes reproducible generated-reference behavior for the pinned inputs/toolchain. It does **not** imply independent scientific replication of CM-PharmE, human validation, or universal semantic correctness.
