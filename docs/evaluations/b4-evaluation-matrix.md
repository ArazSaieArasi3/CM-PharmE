# B4 Evaluation Matrix — Executed Evidence

## Scope

This matrix records the B4/B4.10 execution status after transferring the two CM-PharmE publication evaluation methods into repository-native evidence and closing the initial logical-reasoning gap. It separates what was actually executed from publication-reported, bounded, or still-open claims.

| Layer | B4 evidence | Executed result | Status | Boundary / remaining work |
|---|---|---|---|---|
| **E1 Syntax** | Canonical Turtle and generated RDF serializations | Canonical/reference Turtle parses; four B3 reference serializations re-parsed and remain graph-isomorphic to the 1,086-triple packaged canonical graph | **PASS** | GitHub modular source has annotation/provenance parity differences; logical axioms are unchanged |
| **E2 Logic** | GitHub Actions + ROBOT `v1.9.10` + HermiT | Run `31796520297` completed successfully; ROBOT checksum verified; HermiT exit code `0`; no unsatisfiable debug module produced | **PASS** | Logical PASS does not establish semantic/domain completeness |
| **E3 Structure** | `b4-structural-validation.json` | **28/28 checks PASS**; 39 concepts, 39 object properties + 1 generalization, 5 domains, 40/40 relation registry/cardinality alignment | **PASS** | Structural consistency is not semantic completeness |
| **E4 Ontological** | `anti-patterns.yaml` + B4.10 finding disposition | No critical issue; three model-refinement candidates and one domain-evidence deferral remain; manuscript/formal prose discrepancy dispositioned as documentation clarification | **CONDITIONAL** | Targeted semantic review remains; no complete automated OntoUML catalog was run |
| **E5 Semantic / Expert** | `b4-expert-evidence.yaml` | Four-expert manuscript evidence normalized with original boundaries; no new expert panel was run | **PARTIAL** | Publication evidence is traceable but not independently replicated |
| **E6 Data / Mapping** | Vaccine sample TTL + schema validation + manuscript/formal traceability | 33 individuals, 32 core classes, all 5 domains, 34 relation assertions, 0 unknown classes/properties, 0 domain/range violations | **PASS — BOUNDED** | Constructed sample only; manuscript-to-formal differences are explicitly recorded |
| **E7 Competency Questions** | Eight versioned SPARQL queries + result file | **8/8 queries executed and met their bounded expected outcomes** | **PASS — BOUNDED** | CQ6–CQ8 do not prove BACM conformance, organizational adoption, or general extensibility |
| **E8 Application** | Vaccine scenario and application-oriented CQs | Cross-domain scenario coverage demonstrated without creating new core classes | **PARTIAL / ILLUSTRATIVE** | No deployed reference architecture, operational interoperability, user outcome, or cost evidence |
| **E9 Reproducibility** | Versioned queries, samples, expected/observed results, structural evidence, pinned ROBOT workflow and artifact | GitHub Actions reproduces source assembly, verifies ROBOT SHA-256, executes HermiT, uploads evidence, and enforces the exit code | **PASS — B4 SCOPE** | Full release/build automation, long-term artifact publication, and annotation-source normalization remain B5 work |

## Key B4/B4.10 findings

1. **The formal inventory is internally traceable:** all 39 concept IDs, 40 relation IDs, five domains, source/target mappings, lifecycle states, and cardinality registry records cross-check successfully.
2. **The eight manuscript competency questions are executable artifacts.** All eight pass on the bounded vaccine example while the repository preserves the weaker evidential interpretation for CQ6–CQ8.
3. **The vaccine example is schema-compatible:** it instantiates 32 existing core classes spanning all five domains and introduces no new scenario-specific class.
4. **OWL logical validation is now repository-executed:** ROBOT/HermiT completed successfully in GitHub Actions run `31796520297` against commit `a9d6b38791435de51966804e81a1ca71db24e253`.
5. **The modular GitHub source and B3 packaged canonical source differ in annotation/provenance coverage, not logical axioms.** B4.10 records zero logical-predicate differences while retaining annotation parity as an engineering follow-up.
6. **The publication scenario is not identical to the canonical formal graph.** B4 records several narrative-to-model gaps instead of adding unsupported relations; B4.10 dispositions these as documentation clarification unless future evidence requires a semantic addition.
7. **Ontological review found no critical issue requiring redesign**, but `Healthcare Provider (CMPE-C0021)` remains a model-refinement candidate because its Role dependence is not represented through explicit/inherited mediation.
8. **The historical Supply Chain Relationship mediation concern remains valid** and is dispositioned as a model-refinement candidate.
9. **Part-whole semantics require targeted review:** the PPP relation is deferred pending domain evidence; `Clinical Pathway` as part of `Pharmaceutical Business Process` is a model-refinement candidate.

## Readiness interpretation

- **B4 evidence-package integrity:** PASS with explicit open findings.
- **OWL logical validation:** **PASS for the current logical axiom set.**
- **Formal ontology stable-release readiness:** **NOT YET** because semantic dispositions and repository-engineering follow-ups remain open.
- **Semantic model redesign required:** **No evidence of a redesign-level defect.**
- **Next decision boundary:** resolve or intentionally defer the model-refinement candidates without conflating logical consistency with ontological adequacy.
