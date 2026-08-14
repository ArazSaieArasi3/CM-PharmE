# CM-PharmE Release Readiness

## Post-closure engineering status

The repository modernization cycle B0–B5 is **closed**. PR #4 was merged into `main`, and the post-merge ontology CI run on the resulting `main` commit completed successfully. The historical baseline, normalized knowledge model, formal ontology, evaluation evidence and reproducible build pipeline therefore all live on `main`.

Closure evidence:

- B5 merge commit on `main`: `00010410d15c6e35eb267e93178b84beef1485d0`
- post-merge GitHub Actions run: `31805218368`
- workflow conclusion: **success**

## Current release-decision gates

| Gate | Status after B5 | Interpretation |
|---|---|---|
| Historical v1.0.0 preservation | PASS | Immutable release artifacts retained |
| Stable IDs / lifecycle / traceability | PASS | 39 concepts, 40 relations, 5 domains |
| Formal ontology source | PASS | Modular authoring source established |
| Full B3 graph parity | PASS | 1,086-triple reference graph reconstructable |
| SHACL generation | PASS | 574 triples; 76 + 76 shapes |
| Structural validation | PASS | Repository quality gates automated |
| OWL DL logical validation | PASS | ROBOT/HermiT workflow verified on `main` |
| Competency-question regression | PASS — bounded | Eight executable B4 queries |
| Deterministic distributions | PASS | TTL, RDF/XML, JSON-LD and N-Triples generated deterministically as CI/release artifacts |
| Deterministic release bundle | PASS | CI verifies byte-identical rebuild |
| Repository modernization B0–B5 | CLOSED | Merge and post-merge `main` CI closure criteria satisfied |
| Open semantic findings | OPEN | Three refinement candidates + one domain-evidence deferral |
| Independent expert/domain replication | PARTIAL | Publication evidence exists; broader replication remains future research |
| License policy | OPEN — owner decision required | Must be selected explicitly before a formal public release policy is finalized |
| `w3id.org` redirect deployment | OPEN | IRI policy exists; redirect registration is external administrative work |
| New semantic version/tag | NOT YET | Must follow intentional semantic evolution, not engineering automation |

## Closure definition and outcome

The defined closure criterion was: **B5 merged to `main` plus a successful post-merge CI audit on `main`.** That criterion has now been satisfied.

The following work is deliberately outside the closed B0–B5 modernization cycle and belongs to subsequent governance or research cycles:

- semantic refinement and CM-PharmE v2 design;
- new paper/research questions;
- independent datasets and empirical evaluation;
- ontology-to-relational mapping and relational database implementation;
- knowledge graph / application layers;
- persistent IRI deployment and publication-administration decisions.

License selection and `w3id.org` registration are release-governance follow-ups and do not reopen the closed B0–B5 modeling/evaluation cycle.
