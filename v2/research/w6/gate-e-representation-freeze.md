# Gate E — Ontology/RDB/KG Representation Architecture Freeze

## Status
**W6 implementation complete — Gate E ready for user decision.**

## Proposed freeze
Approve the W6 representation architecture as the baseline for W7 evaluation.

## Candidate frozen commitments
1. W5 OWL remains the semantic authority; RDB and KG are implementation representations.
2. PostgreSQL/PostGIS is the relational reference implementation.
3. Gate-D identity distinctions remain explicit in relational keys/tables and RDF projections.
4. Dataset, release, source record, assertion, evidence and transformation provenance remain first-class.
5. Source identifiers use Scheme/Assignment semantics and do not become universal entity identities.
6. Geography remains distinct from regulatory jurisdiction; PostGIS supports spatial realization.
7. Entity resolution is represented by reversible match assertions with method/confidence/status.
8. Aggregate administrative rows are not transformed into patient individuals.
9. A relational aggregate row may project to multiple RDF observation-result metric nodes under the documented one-to-many projection rule.
10. RDF instance generation uses frozen W5 ontology IRIs and deterministic instance-IRI rules.
11. Selected representation equivalence is evaluated through registered paired SQL↔SPARQL queries; no universal SQL/SPARQL equivalence is claimed.
12. API work in W6 is a documented read contract, not a production-service deployment claim.
13. W6 CI fixtures are schema-faithful synthetic data; their PASS does not establish full external dataset quality or coverage.
14. H1–H3 remain held out for W7.

## Successful implementation evidence
A successful W6 CI run established:
- PostgreSQL/PostGIS bootstrap PASS;
- source-contract fixture ingestion PASS;
- 7 source records and 7 relational observation rows;
- 2 accepted exact cross-source match assertions;
- deterministic RDF ABox PASS;
- 398 ABox triples;
- KG SHA-256 `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`;
- ontology-term mapping checks PASS (36 registered mappings);
- provenance/representation relational checks PASS;
- SHACL PASS;
- 4/4 registered SQL↔SPARQL benchmarks PASS;
- OpenAPI syntax PASS;
- held-out integrity PASS.

## Gate E decision requested
**Approve / Modify / Reject**.

Approval authorizes W7 evaluation against this representation baseline. It does not authorize claims of empirical generalizability before W7 evidence exists.