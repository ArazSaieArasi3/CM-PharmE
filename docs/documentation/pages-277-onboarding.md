# Future-version onboarding — #277

The deployment workflow invokes `run_version_pipeline.py` for checkout, semantic
inputs, formal reference, downloads, conversion, explorers and directory aliases.
Version IDs, exact source refs, output routes, build commands and generator flags
come from the registry/contracts. No V1/V2 stage is copied to onboard a new version.

## Onboarding checklist

1. Complete the real scientific source/validation baseline and freeze its exact ref.
2. Add its registry entry: lifecycle, source paths/fingerprint, immutable/current
   route, citation state, curated Wiki explanation and supersedes/superseded_by.
3. Add its semantic build contract with an isolated `<OUTPUT_ROOT>` command,
   validation manifest, fingerprint and reference coverage authority. Extra build
   paths use `<SOURCE_ROOT>` and `<PUBLICATION_ROOT>` placeholders.
4. Add its download bundle entry and serialization inventory. Add WIDOCO/WebVOWL
   adapter entries only for enabled features, with exact source and route bindings.
   WIDOCO requires its checked config/intro; WebVOWL requires converter projection
   counts and frontend/dataset checksums. These are data/config entries.
5. Run registry/schema, common pipeline plan and source-validation gates before
   any public output is generated. Missing/inconsistent config must reject the plan.
6. Rebuild candidate artifacts with the common workflow and audit entity coverage,
   local links, downloads, provenance, exposure and exact-ref isolation.
7. Run the future-version proof against the assembled candidate; confirm previous
   version subtrees are byte-identical and source/path mutation is rejected.
8. Publish only real approved content and verify its rendered routes and curated
   Wiki journeys. Archive the exact output and update the documentation baseline.

The #277 test uses a synthetic V3 registry exclusively in temporary directories.
It exercises schema validation, three-family selection, common-stage planning,
four reference/explorer flag combinations, missing-config rejection, namespace
collision and stable-ref protection. Existing assembled V1 and V2 subtrees are
hashed before/after the temporary onboarding run. The shared explorer test checks
synthetic source binding and refuses overwrite. No synthetic V3 is added to the
production registry or published site.

The dry-run is architecture evidence, not evidence for a real V3 ontology or its
scientific validity. Real future sources must implement the validated build and
coverage interfaces; lack of those inputs blocks publication.
