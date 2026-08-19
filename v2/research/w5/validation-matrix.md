# W5 Formal Validation Matrix

| Gate | Method / tool | Mandatory for Formal Gate | What PASS establishes | What PASS does not establish |
|---|---|---:|---|---|
| Source parse | RDFLib Turtle parser | Yes | all authoritative modules are syntactically parseable | domain correctness |
| Conceptual registry coverage | project-native Gate-D JSON + RDFLib | Yes | all 87 conceptual elements are represented as OWL classes or declared datatypes | official OntoUML-tool validation |
| Formal inventory | deterministic count checks | Yes | expected classes/datatypes/properties are present | conceptual completeness |
| Protected distinctions | OWL disjointness checks | Yes | selected Gate-D non-equivalences are explicitly protected | every UFO constraint is expressible in OWL |
| RDF serialization equivalence | RDFLib graph isomorphism | Yes | TTL/RDF/XML/OWL/JSON-LD/N-Triples represent the same RDF graph | semantic adequacy of the graph |
| Deterministic build | two independent canonical builds | Yes | canonical N-Triples and manifest are reproducible | reproducibility of external datasets |
| SHACL syntax/profile | RDFLib + pySHACL Meta-SHACL | Yes | shapes are executable and structurally valid | that all future source data conform |
| SHACL smoke | pySHACL over formal smoke fixture | Yes | core research-integrity shapes can validate a known-valid sample | empirical data quality |
| OWL profile | ROBOT/OWLAPI `validate-profile --profile DL` | Yes | formal artifact satisfies the selected OWL 2 DL profile check | logical consistency by itself |
| Logical reasoning | ROBOT + HermiT | Yes | current axiom set is reasoner-processable without reported inconsistency/unsatisfiable named-class failure | truth/completeness of domain claims |
| Review views | ROBOT Manchester + Functional Syntax | Required artifact | human-reviewable formal views are generated | independent formal validation |
| Baseline fingerprint | SHA-256 of canonical graph | Yes after bootstrap | semantic-regression baseline is fixed | immutability of future approved versions |

## Formal Gate policy
No mandatory failure is downgraded merely to declare W5 complete. The first CI run may bootstrap the exact canonical fingerprint; the fingerprint must then be committed and the full Formal Gate rerun before the gate can be presented for approval.
