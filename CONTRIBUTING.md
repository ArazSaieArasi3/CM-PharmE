# Contributing to CM-PharmE

CM-PharmE is a research ontology repository. Contributions must preserve traceability between the conceptual model, formal ontology, evaluation evidence, and generated artifacts.

## Semantic source rule

- Edit ontology semantics only under `ontology/source/modules/` and the corresponding authoritative registries/mappings.
- Do **not** hand-edit generated distributions such as `cm-pharme.owl`, generated RDF/JSON-LD/N-Triples/TriG/N-Quads, Manchester/Functional views, SHACL output, reasoned OWL, validation reports, or release ZIPs.
- A generated artifact must be reproducible from the committed source.

## Required checks for semantic changes

A semantic change should include, as applicable:

1. stable-ID/lifecycle handling;
2. concept/relation and cardinality traceability;
3. updated competency questions or expectations where behavior changes;
4. updated sample/data mappings where relevant;
5. structural and graph-fingerprint review;
6. SHACL execution review;
7. OWL profile and HermiT reasoning review;
8. explicit disposition of any OntoUML/UFO semantic finding;
9. documentation of whether the change requires a new semantic version.

## Evidence discipline

Automated PASS results must not be described as stronger evidence than they provide. Logical consistency is not domain completeness; executable competency questions are not independent empirical validation; an illustrative scenario is not operational deployment; and reproducible serializations are not standards conformance.

## Current-version boundary

The current stable semantic baseline remains CM-PharmE 1.0. Repository engineering and publication documentation do not automatically create a new semantic release. Substantive concept/relation redesign belongs to the governed next-version research cycle.
