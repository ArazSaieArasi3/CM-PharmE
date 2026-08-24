# W7-E10 manuscript evidence — ontology↔RDB↔KG semantic consistency

## Methods-ready statement
Cross-representation semantic consistency was evaluated prospectively over the registered ontology↔RDB mapping registry, the executable PostgreSQL/PostGIS reference realization, and the deterministically generated RDF knowledge graph. The evaluation checked ontology-IRI and relational-table resolution, selected class and relation cardinality preservation, deterministic identity round-trip from relational identities to RDF instance IRIs, identifier/provenance/geography semantics, the explicit one-to-many projection of relational reimbursement aggregates to metric-level RDF observation results, and a frozen suite of paired SQL and SPARQL benchmark queries.

## Results-ready evidence
Final GitHub Actions run `32478941799` completed successfully; artifact `9445329571`, digest `sha256:2104ba22c002642e57f71649291e2b0574328ca3ed5413e87a9f78dc52f08f8b`.

Key results:
- 36 registered ontology↔RDB mappings; 0 unknown ontology IRIs; 0 missing registered tables;
- 14/14 selected class/cardinality checks passed;
- 10/10 selected relation/cardinality checks passed;
- 44/44 deterministic relational-identity→RDF-node checks passed;
- 7 relational reimbursement aggregate rows produced the expected 28 metric-level RDF ObservationResult nodes; 7/7 per-row projection checks passed;
- 4/4 frozen paired SQL↔SPARQL benchmarks returned equivalent canonicalized answer sets;
- 10 non-direct mappings remain explicitly documented: 4 bounded, 2 polymorphic, 1 relational projection, 1 one-to-many RDF projection, and 2 deferred mappings.

## Claim boundary
These results support semantic consistency for the registered mappings, reference realization and frozen benchmark queries. They do not demonstrate universal lossless or bidirectional equivalence between all ontology semantics, all relational fields and arbitrary RDF/KG/query representations. Non-direct and deferred mappings must remain visible as representation boundaries rather than being described as direct equivalences.
