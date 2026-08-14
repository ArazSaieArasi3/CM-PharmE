# Current CM-PharmE Model

The current **stable semantic baseline** is `v1.0.0`. The original Draw.io/XML/PNG artifacts are frozen under [`releases/v1.0.0/`](../../releases/v1.0.0/), while the normalized living knowledge layer is maintained through:

- [`catalog/concepts.yaml`](../../catalog/concepts.yaml)
- [`catalog/relations.yaml`](../../catalog/relations.yaml)
- [`catalog/domains.yaml`](../../catalog/domains.yaml)
- [`docs/concepts/`](../../docs/concepts/)
- [`docs/relations/`](../../docs/relations/)
- [`docs/domains/`](../../docs/domains/)

No newer semantic model version is declared merely because a newer manuscript revision exists. A future `vNext` becomes a model release candidate only when concept/relation/domain changes are explicitly identified and compared against `v1.0.0`.

This separation prevents paper revision numbers from becoming model version numbers and keeps CM-PharmE model-centric rather than publication-centric.
