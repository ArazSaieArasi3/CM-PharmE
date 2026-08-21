# W7-E10 — Ontology ↔ RDB ↔ KG Semantic Consistency Evaluation

## Purpose
E10 evaluates whether the semantic distinctions implemented by the CM-PharmE 2.0 ontology remain consistent through the W6 PostgreSQL/PostGIS reference realization and the generated RDF knowledge graph. The evaluation is deliberately bounded to the registered mappings, the reference realization, and the frozen SQL↔SPARQL benchmark suite.

## Reproducible execution
- GitHub Actions workflow: `CM-PharmE 2.0 W7-E10 Representation Consistency`
- Final run: `32478941799` — **SUCCESS**
- Evidence artifact: `9445329571`
- Artifact digest: `sha256:2104ba22c002642e57f71649291e2b0574328ca3ed5413e87a9f78dc52f08f8b`
- Ontology fingerprint reverified before evaluation: `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`
- Generated reference KG: **398 triples**; canonical N-Triples SHA-256 `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`

## Results
| Measure | Result |
|---|---:|
| Mandatory E10 gate | **PASS** |
| Family status | **PASS WITH WARNING** |
| Registered ontology↔RDB mappings | **36** |
| Mapping IRIs unresolved in ontology | **0** |
| Registered RDB tables missing | **0** |
| Class/cardinality preservation checks | **14/14 PASS** |
| Relation/cardinality preservation checks | **10/10 PASS** |
| Deterministic identity round-trip checks | **44/44 PASS** |
| Relational aggregate observation rows | **7** |
| Expected RDF metric ObservationResults | **28** |
| Observed RDF metric ObservationResults | **28** |
| Per-row one-to-many projection checks | **7/7 PASS** |
| Frozen SQL↔SPARQL benchmarks | **4/4 PASS** |
| Explicit non-direct mapping exceptions | **10** |

## Mapping-resolution audit
All 36 mapping-registry IRIs resolve against the frozen ontology and all registered relational tables used by the mapping registry are present in the executable reference schema.

The mapping registry intentionally does **not** describe every mapping as direct. Current status distribution is:
- direct: **26**
- bounded: **4**
- polymorphic: **2**
- relational projection: **1**
- one-to-many RDF projection: **1**
- deferred: **2**

These ten non-direct mappings are not failures. They are explicit semantic/representation boundaries and are retained in the evidence rather than hidden behind a lossless-equivalence claim.

## Entity and relation preservation
The evaluator compares relational counts and RDF class/relation counts for the represented identity layers and provenance structures. The tested set includes Dataset, DatasetRelease, SourceRecord, ProvenanceActivity, geography, Facility, PharmaceuticalSubstance, MedicinalProduct, MedicinalProductPresentation, IdentifierScheme, IdentifierAssignment, Assertion, EvidenceSupport and EntityMatchAssertion.

All **14/14 class/cardinality** and **10/10 relation/cardinality** checks passed. The relation checks include presentation→product, product→active substance, facility→physical geography, identifier scheme/entity/value, EvidenceSupport endpoints, match confidence, and SourceRecord provenance activity.

The result supports preservation of the tested distinctions; it does not imply that every ontology class or relation currently has a populated relational/KG realization.

## Deterministic identity round-trip
For every populated identity row in the tested class set, the evaluator reconstructs the deterministic W6 instance IRI and checks that the expected RDF node has the correct type. **44/44 checks passed.**

This is a bounded identity round-trip check from the reference database into the generated RDF graph. It is not a general RDF→SQL reconstruction algorithm and is not reported as universal bidirectional round-trip equivalence.

## Explicit one-to-many projection test
The W6 mapping rule for reimbursement utilization observations is intentionally not row-count preserving. One relational aggregate row can contain multiple measures (`patient_count`, `package_count`, `cost_bgn`, `cost_eur`) and is projected into a separate RDF `ReimbursementUtilisationObservationResult` for every non-null metric.

E10 tested this rule directly:
- RDB aggregate rows: **7**
- expected metric-level RDF nodes: **28**
- observed metric-level RDF nodes: **28**
- per-row projection checks: **7/7 PASS**

Thus, semantic consistency here is defined by the documented projection rule, not by raw equality between RDB row count and RDF node count.

## SQL ↔ SPARQL consistency
The frozen paired benchmark suite was rerun against the same reference realization and generated KG. **4/4** benchmark pairs returned equivalent canonicalized result sets:
1. product-presentation identity/code mapping;
2. regional/time/product observation aggregation;
3. Dataset DOI → SourceRecord provenance traversal;
4. Facility → physical geography traversal.

This establishes query-result agreement only for these registered benchmark questions. It does not establish equivalence for arbitrary SQL and SPARQL queries.

## Interpretation and warning
E10 is **PASS WITH WARNING** because the implementation deliberately contains non-direct mappings and deferred representation elements. Reporting them explicitly is methodologically preferable to treating them as hidden loss or silently promoting them to direct mappings.

The defensible claim is:

> Within the registered mapping set, W6 reference realization and frozen benchmark queries, CM-PharmE 2.0 preserves the tested entity identities, relation cardinalities, provenance/identifier/geography semantics, the documented aggregate-to-metric RDF projection, and the selected SQL↔SPARQL answers.

The evaluation does **not** establish universal, lossless, bidirectional equivalence across every ontology term, relational field, RDF graph or query.
