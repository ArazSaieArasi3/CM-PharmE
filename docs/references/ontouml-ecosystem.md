# Official OntoUML Ecosystem References

CM-PharmE uses UFO/OntoUML as an ontological foundation for concept and relation clarification. This page records authoritative OntoUML ecosystem references that help readers interpret those commitments and connect CM-PharmE to the maintained OntoUML tooling and model ecosystem.

These links are **references**, not claims that CM-PharmE is currently serialized in, conformant with, or formally equivalent to every referenced artifact.

## Official resources

### OntoUML Metamodel

- Repository: https://github.com/OntoUML/ontouml-metamodel
- Persistent entry point: https://w3id.org/ontouml/metamodel

The metamodel defines the concepts officially supported by the OntoUML language and serves as a reference for the OntoUML-as-a-Service ecosystem.

### OntoUML Vocabulary

- Repository: https://github.com/OntoUML/ontouml-vocabulary
- Persistent vocabulary IRI: https://w3id.org/ontouml/vocabulary
- Documentation: https://w3id.org/ontouml/vocabulary/doc

The vocabulary is an OWL implementation of the OntoUML Metamodel intended for linked-data serialization, exchange, and publication of OntoUML models.

### OntoUML Schema

- Repository: https://github.com/OntoUML/ontouml-schema
- Persistent schema entry point: https://w3id.org/ontouml/schema

The schema provides a JSON Schema representation for exchanging OntoUML models. A future CM-PharmE interoperability cycle may evaluate whether a native OntoUML Schema serialization should be produced; no such conformance is claimed by the current repository.

### OntoUML/UFO Catalog

- Repository: https://github.com/OntoUML/ontouml-models
- Persistent entry point: https://w3id.org/ontouml-models/git

The catalog provides a FAIR collection of OntoUML/UFO models and is relevant to future comparative, dataset, and empirical-evaluation work. CM-PharmE is not currently presented as a catalog submission.

## How CM-PharmE currently uses OntoUML/UFO

The current model uses conceptual stereotype categories such as `Kind`, `Role`, `Relator`, and `Mode`, together with a conservative treatment of temporally unfolding constructs and relation patterns such as mediation and characterization. The formal ontology keeps these as CM-PharmE metamodel terms with documented conceptual correspondence; it does **not** assert unsupported `owl:equivalentClass` links to external OntoUML resources.

See:

- [Research and Model Development Method](../methodology/research-and-model-development.md)
- [CM-PharmE Ontology](../../ontology/README.md)
- [UFO/OntoUML correspondence notes](../../ontology/mappings/ufo-stereotypes.ttl)
- [Evaluation](../evaluations/index.md)

## Future interoperability opportunity

A later research cycle may evaluate mappings to the OntoUML Metamodel/Vocabulary, OntoUML Schema serialization, and comparative use of the OntoUML/UFO Catalog. Such work should preserve provenance and licensing constraints and should distinguish documented correspondence from formal equivalence or conformance.