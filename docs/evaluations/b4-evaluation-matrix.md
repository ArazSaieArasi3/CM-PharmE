# B4 Evaluation Matrix — Executed Evidence

## Scope

This matrix records the B4 execution status after transferring the two CM-PharmE publication evaluation methods into repository-native evidence. It separates what was actually executed from publication-reported or still-unverified claims.

| Layer | B4 evidence | Executed result | Status | Boundary / remaining work |
|---|---|---|---|---|
| **E1 Syntax** | Canonical Turtle and generated RDF serializations | Canonical Turtle parses; four reference serializations re-parsed and remain graph-isomorphic to the 1,086-triple canonical graph | **PASS** | Does not imply logical consistency |
| **E2 Logic** | Intended ROBOT/HermiT validation | Java available, but no OWL DL reasoner binary/library was available and runtime download was blocked | **NOT VERIFIED / BLOCKED** | Must run HermiT/ELK/ROBOT before any OWL DL consistency claim |
| **E3 Structure** | `b4-structural-validation.json` | **28/28 checks PASS**; 39 concepts, 39 object properties + 1 generalization, 5 domains, 40/40 relation registry/cardinality alignment | **PASS** | Structural consistency is not semantic completeness |
| **E4 Ontological** | `anti-patterns.yaml` | No critical issue; historical Supply Chain mediation and PPP part-whole concerns remain; B4 adds Healthcare Provider role-without-explicit-mediation and Clinical Pathway part-whole review candidates | **CONDITIONAL** | Targeted semantic review remains; no complete automated OntoUML catalog was run |
| **E5 Semantic / Expert** | `b4-expert-evidence.yaml` | Four-expert manuscript evidence normalized with original boundaries; no new expert panel was run | **PARTIAL** | Publication evidence is traceable but not independently replicated |
| **E6 Data / Mapping** | Vaccine sample TTL + schema validation + manuscript/formal traceability | 33 individuals, 32 core classes, all 5 domains, 34 relation assertions, 0 unknown classes/properties, 0 domain/range violations | **PASS — BOUNDED** | Constructed sample only; manuscript-to-formal mismatches are explicitly recorded |
| **E7 Competency Questions** | Eight versioned SPARQL queries + result file | **8/8 queries executed and met their bounded expected outcomes** | **PASS — BOUNDED** | CQ6–CQ8 do not prove BACM conformance, organizational adoption, or general extensibility |
| **E8 Application** | Vaccine scenario and application-oriented CQs | Cross-domain scenario coverage demonstrated without creating new core classes | **PARTIAL / ILLUSTRATIVE** | No deployed reference architecture, operational interoperability, user outcome, or cost evidence |
| **E9 Reproducibility** | Versioned queries, sample, expected/observed results, structural results, provenance policy | Core B4 evidence is inspectable and repeatable with RDFLib-compatible tooling | **PARTIAL** | No CI runner and no executed DL reasoner yet |

## Key B4 findings

1. **The formal inventory is internally traceable:** all 39 concept IDs, 40 relation IDs, five domains, source/target mappings, lifecycle states, and cardinality registry records cross-check successfully.
2. **The eight manuscript competency questions are now executable artifacts.** All eight pass on the bounded vaccine example, while the repository preserves the weaker evidential interpretation for CQ6–CQ8.
3. **The vaccine example is schema-compatible:** it instantiates 32 existing core classes spanning all five domains and introduces no new scenario-specific class.
4. **The publication scenario is not identical to the canonical formal graph.** B4 records several narrative-to-model gaps instead of adding unsupported relations.
5. **Ontological review found no critical issue requiring redesign**, but it did not fully reproduce the manuscript's historical “Role without Relator = Clean” observation: `Healthcare Provider (CMPE-C0021)` lacks explicit/inherited mediation in the current formal graph.
6. **The historical Supply Chain Relationship mediation concern remains valid.**
7. **Part-whole semantics require targeted review**, including the manuscript-reported PPP relation and a B4 candidate involving `Clinical Pathway` as part of `Pharmaceutical Business Process`.
8. **OWL DL logical consistency remains unverified** because an executable reasoner was not available in the current runtime.

## Readiness interpretation

- **B4 evidence-package integrity:** PASS with explicit open findings.
- **Formal ontology release readiness:** **NOT YET**.
- **Semantic model redesign required:** **No evidence of a redesign-level defect at this stage.**
- **Next blocking item for stronger validation:** reproducible OWL DL reasoning plus resolution/disposition of the targeted semantic review findings.
