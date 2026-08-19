# W5 External Mapping Policy

## Principle
External vocabularies and standards are used through modular, conservative mappings. CM-PharmE 2.0 does not claim conformance to an external standard merely because related concepts or identifiers are referenced.

## Current W5 mappings
- PROV-O: `skos:closeMatch` hints for provenance/activity/entity concepts where useful.
- GeoNames: `rdfs:seeAlso` for geographic normalization semantics; GeoNames identifiers may be represented through the Identifier pattern.
- NDC, ATC, ChEMBL and regulatory identifiers: represented as Identifier Scheme/Assignment instances during later data integration rather than as ontology entity IRIs.
- COVER/ROSE: Risk/Resilience alignment remains a documented target; no `owl:equivalentClass` assertion is made in W5.

## Equivalence rule
`owl:equivalentClass`, `owl:equivalentProperty` and strong identity mappings require dedicated semantic evidence. `skos:closeMatch`, `rdfs:seeAlso` or explicit Mapping Assertions are preferred when correspondence is useful but not proven equivalent.

## Deferred mappings
IDMP, FHIR and other healthcare/pharmaceutical standards remain candidates for later modular mapping work. They are not part of the W5 Formal Gate unless a separately evaluated mapping module is added.

## Evaluation rule
Mapping coverage, correctness and standards-conformance claims belong to W7 or a dedicated mapping evaluation. W5 only establishes the mapping architecture and conservative initial hooks.
