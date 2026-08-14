# Mappings

This area contains explicit, machine-readable traceability mappings among CM-PharmE semantic entities and will later expand to datasets, upper ontologies, external ontologies, publications, evaluations, and applications.

## Available in B2

- [`concept-domain.csv`](concept-domain.csv) — maps each concept to its primary domain and optional cross-domain memberships.
- [`concept-relation.csv`](concept-relation.csv) — maps each canonical relation to its source and target concepts.

The corresponding `v1.0.0` snapshots are frozen under [`releases/v1.0.0/mappings/`](../releases/v1.0.0/mappings/) so later changes to the living mappings do not rewrite the historical release.

## Future mapping layers

Planned mappings include Concept↔Dataset, Concept↔UFO/BFO, external ontology crosswalks, Publication↔Model Version, Evaluation↔Version, and Application↔Model/Ontology Version. Where appropriate, ontology mappings will adopt SSSOM or another explicit provenance-aware mapping representation rather than ad-hoc duplicated documentation.
