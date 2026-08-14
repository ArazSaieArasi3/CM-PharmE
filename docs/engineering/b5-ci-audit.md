# B5 — Final CI Audit

## Scope

This audit records the final branch-level verification of the B5 reproducible ontology build and CI engineering cycle. It is an engineering/evidence audit only; B5 does not declare a new semantic model release and does not apply the open B4.10 semantic refinement candidates.

## Validated source state

- branch: `automation/b5-reproducible-build-v1`
- validated commit: `237f228c6b5cc5ccdb5edd1e4d2d4db23baded4b`
- GitHub Actions workflow: `CM-PharmE Ontology CI`
- workflow run ID: `31803512755`
- workflow conclusion: **success**

The later commit adding this audit file is documentation-only and does not change ontology source, evaluation inputs, build tooling or CI behavior.

## Full source parity

B5 closes the B4.10 annotation/provenance parity gap.

- reconstructed ontology triples: **1,086**
- B3 reference ontology triples: **1,086**
- canonical ontology graph SHA-256: `cc823a8aff4d7e7818f8470f2dbad6ca8045ff92e5637fbf3503bc105170a83f`
- SHACL triples: **574**
- SHACL NodeShapes: **76**
- SHACL PropertyShapes: **76**
- canonical SHACL graph SHA-256: `2a79cc94a2118a0f6f6edb6eb3b72ed9ad20f278ebda60e9e258b0e3d0a9e893`

The parity restoration consists of B3 annotation/provenance recovery and wording alignment. The logical axiom set and B4.10 semantic finding dispositions were not changed.

## Quality gates

All gates passed in run `31803512755`:

- two independent clean ontology builds completed successfully;
- the two build directories were byte-identical;
- full ontology graph fingerprint matched the B3 reference;
- full SHACL graph fingerprint matched the B3 reference;
- 39 concept classes validated;
- 39 object properties + 1 generalization record validated;
- five domains validated;
- 42 OWL restrictions validated;
- 76 SHACL NodeShapes and 76 PropertyShapes validated;
- Turtle, RDF/XML/OWL, RDF/XML, expanded JSON-LD and canonical N-Triples were graph-isomorphic to the source;
- all manifest artifact SHA-256 values matched;
- historical `example.org` and converter-cardinality artifacts were absent;
- R0011 deprecation / R0027 replacement was preserved;
- R0031 normalization was preserved;
- C0025 remained the canonical Relator treatment;
- all eight competency-query regression assertions passed;
- ROBOT `v1.9.10` checksum verification passed;
- HermiT logical validation completed with exit code `0`;
- two independently generated release ZIP bundles were byte-identical.

## Deterministic release-bundle evidence

- bundle files: **11**
- bundle size: **72,219 bytes**
- deterministic bundle SHA-256: `878343b01e48f97808d35faf367ddf2d9382434394c8354cf2bba7b04097dccd`

The bundle is a reproducible engineering artifact and is not itself a semantic release.

## GitHub Actions evidence artifact

- artifact name: `cm-pharme-b5-ontology-ci-evidence`
- artifact ID: `9220207993`
- artifact size: **136,795 bytes**
- artifact digest: `sha256:54744988c4a138a3694976e93ff6bdaa0b7b7bdec75e9694fda806c61f0ba8e3`

The third-party ROBOT JAR is intentionally excluded from the evidence artifact. The evidence retains the verified tool version/checksum, reasoned OWL, reasoner log, exit code, summary, generated distributions, build/quality reports, checksums and deterministic release bundle.

## Evaluation regression status

The eight B4 competency questions remain executable regression tests over the constructed vaccine scenario:

- CQ1: PASS
- CQ2: PASS
- CQ3: PASS
- CQ4: PASS
- CQ5: PASS — 6 rows
- CQ6: PASS — 6 rows
- CQ7: PASS — 5 represented domains
- CQ8: PASS — 32 mapped core classes, 5 represented domains, 0 scenario-specific classes

These remain bounded evaluation/regression evidence and are not generalized to empirical deployment validation.

## B5 branch-level conclusion

**B5 implementation and branch-level CI: PASS.**

No blocking engineering defect remains for opening the B5 integration Pull Request. The repository-modernization cycle is not formally closed until B5 is merged into `main` and the post-merge `main` CI run passes.

## Explicitly outside B5 closure

The following are separate subsequent decisions or research cycles:

- semantic refinement / CM-PharmE v2;
- new semantic version/tag/release;
- additional independent expert/domain validation;
- real-world datasets and empirical evaluation;
- ontology-to-relational mapping and relational database implementation;
- knowledge graph / application development;
- license selection;
- external `w3id.org` redirect registration.
