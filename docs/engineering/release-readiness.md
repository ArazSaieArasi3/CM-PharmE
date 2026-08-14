# CM-PharmE Release Readiness

## Engineering readiness after B5

The repository modernization cycle B0–B5 is considered technically complete when the B5 Pull Request is merged and its `main` CI run passes. At that point the historical baseline, normalized knowledge model, formal ontology, evaluation evidence and reproducible build pipeline all live on `main`.

## Current release-decision gates

| Gate | Status after B5 | Interpretation |
|---|---|---|
| Historical v1.0.0 preservation | PASS | Immutable release artifacts retained |
| Stable IDs / lifecycle / traceability | PASS | 39 concepts, 40 relations, 5 domains |
| Formal ontology source | PASS | Modular authoring source established |
| Full B3 graph parity | PASS | 1,086-triple reference graph reconstructable |
| SHACL generation | PASS | 574 triples; 76 + 76 shapes |
| Structural validation | PASS | Repository quality gates automated |
| OWL DL logical validation | PASS | ROBOT/HermiT workflow available |
| Competency-question regression | PASS — bounded | Eight executable B4 queries |
| Deterministic distributions | PASS | TTL, RDF/XML, JSON-LD and N-Triples generated deterministically as CI/release artifacts |
| Deterministic release bundle | PASS | CI verifies byte-identical rebuild |
| Open semantic findings | OPEN | Three refinement candidates + one domain-evidence deferral |
| Independent expert/domain replication | PARTIAL | Publication evidence exists; broader replication remains future research |
| License policy | OPEN — owner decision required | Must be selected explicitly before a formal public release policy is finalized |
| `w3id.org` redirect deployment | OPEN | IRI policy exists; redirect registration is external administrative work |
| New semantic version/tag | NOT YET | Must follow intentional semantic evolution, not engineering automation |

## Closure definition

**Repository modernization B0–B5 closes after B5 is merged to `main` and the post-merge CI audit passes.**

The following work is deliberately outside that closure boundary and begins the next research cycle:

- semantic refinement and CM-PharmE v2 design;
- new paper/research questions;
- independent datasets and empirical evaluation;
- ontology-to-relational mapping and relational database implementation;
- knowledge graph / application layers;
- persistent IRI deployment and publication-administration decisions.

License selection and `w3id.org` registration are small release-governance tasks that can be completed immediately after B5 without reopening the B0–B5 modeling/evaluation cycle.
