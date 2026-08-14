# Mappings

This area contains explicit, machine-readable traceability mappings among CM-PharmE semantic entities and is designed to expand toward datasets, upper ontologies, external ontologies, publications, evaluations, and applications.

## Current mappings

- [`concept-domain.csv`](concept-domain.csv) — maps each concept to its primary domain and optional cross-domain memberships.
- [`concept-relation.csv`](concept-relation.csv) — maps each canonical relation to its source and target concepts.
- [`cardinality/`](cardinality/) — records relation endpoint multiplicities and cardinality provenance used by the formal ontology.

The corresponding `v1.0.0` snapshots are frozen under [`releases/v1.0.0/mappings/`](../releases/v1.0.0/mappings/) so later changes to the living mappings do not rewrite the historical release.

## Foundational-ontology and OntoUML boundary

CM-PharmE currently records cautious conceptual correspondence with UFO/OntoUML categories without asserting unsupported external equivalence. See the [Official OntoUML Ecosystem References](../docs/references/ontouml-ecosystem.md) and [`../ontology/mappings/ufo-stereotypes.ttl`](../ontology/mappings/ufo-stereotypes.ttl).

## Future mapping layers

Planned mappings include Concept↔Dataset, more explicit Concept↔UFO/OntoUML crosswalks, external ontology mappings, Publication↔Model Version, Evaluation↔Version, and Application↔Model/Ontology Version. Where appropriate, ontology mappings will adopt SSSOM or another explicit provenance-aware mapping representation rather than ad-hoc duplicated documentation.

Future mappings should distinguish correspondence, close match, transformation, and formal equivalence rather than collapsing them into a single relationship.