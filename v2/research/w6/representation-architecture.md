# W6 Ontology↔RDB↔KG Representation Architecture

## Architectural principle
CM-PharmE 2.0 uses the W5 OWL ontology as the semantic authority and represents the same selected semantics through two implementation views: a normalized PostgreSQL/PostGIS reference database and an RDF ABox/knowledge graph. Neither representation is treated as a new conceptual model.

## Layered architecture
1. **W5 semantic authority** — frozen classes, properties, IRIs and Gate-D distinctions.
2. **Source-contract layer** — admitted source schemas, versions, DOI/authority metadata and semantic boundaries.
3. **Staging/transformation layer** — source-record fingerprints and transformation-run provenance.
4. **Canonical relational layer** — normalized PostgreSQL/PostGIS structures for entities, classifications, observations, identifiers, assertions and provenance.
5. **RDF ABox layer** — deterministic RDF projection using W5 ontology IRIs and stable instance IRIs.
6. **Query/access layer** — stable SQL views, SPARQL benchmark queries and a bounded OpenAPI contract.
7. **Regression layer** — ontology↔RDB registry, SHACL, unknown-term checks, provenance checks, deterministic KG fingerprint and paired SQL↔SPARQL equivalence.

## Protected semantic distinctions
The relational implementation explicitly prevents common source-schema conflations:
- `Organization` and `Facility` use different tables and keys.
- Physical `Geography` and `RegulatoryJurisdiction` are distinct tables.
- `MedicinalProduct`, `PharmaceuticalSubstance` and `MedicinalProductPresentation` are separate identities.
- Product identifiers are represented through `IdentifierScheme` + `IdentifierAssignment`; lexical identifiers are not entity primary identities.
- `Assertion`, `SourceRecord` and `EvidenceSupport` remain distinct.
- `ObservationResult` is not a patient, source row or observation activity.
- aggregate source measures remain measurements; W6 does not fabricate patient instances or observation events that the sources do not provide.

## Relational-to-RDF observation projection
A relational administrative row can carry multiple reported measures (for example patient count, package count and cost). To avoid conflating distinct measured values into one RDF value-bearing observation node, the W6 exporter deterministically projects one relational aggregate row to separate RDF `ReimbursementUtilisationObservationResult` nodes for each populated metric. These nodes share source-record/provenance, context and product-presentation links.

This is a documented one-to-many representation projection, not an ontology change.

## Geospatial treatment
PostGIS provides a geometry-ready `geography` entity with EPSG:4326 storage and spatial indexes. Source aliases are resolved separately with method and confidence. The current CI fixture validates normalization mechanics only; it does not claim that GeoNames identifiers or production-quality coordinates have been populated for the test regions.

## Entity resolution
Cross-source entity integration is represented as an `EntityMatchAssertion` with two source records, a matched canonical entity, method, confidence and explicit status. Ambiguous candidates are designed to remain unresolved rather than being silently merged.

The W6 CI fixture creates exact deterministic product-presentation matches only. It is not an accuracy benchmark for real-world entity resolution.

## Provenance invariant
For ingested observations the implemented lineage is:

`Dataset → DatasetRelease → SourceRecord → Assertion → EvidenceSupport`

with `TransformationRun` recording the ingestion/provenance activity. RDF output also retains source-record and transformation links.

## Representation equivalence
W6 does not claim universal equivalence between SQL and SPARQL. It defines four registered paired benchmark queries and normalizes their result sets before comparison. The current fixture baseline passes all four.

## Gate E freeze proposal
If Gate E is approved, W7 may add evaluation datasets, larger source executions and held-out mappings without silently changing the representation rules above. Material reversal of a Gate-D/W5 identity distinction or a change to the RDB↔RDF projection contract requires a documented architecture-change decision.