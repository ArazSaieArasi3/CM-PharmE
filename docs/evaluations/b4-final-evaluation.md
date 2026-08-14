# CM-PharmE B4/B4.10 — Final Evaluation Report

## Purpose

B4 evaluates CM-PharmE by turning the design and evaluation procedures reported in the published conference paper and the later journal manuscript under review into repository-native, inspectable evidence. B4.10 closes the initial OWL reasoner gap and assigns explicit dispositions to the semantic findings exposed by B4.

The repository does not treat manuscript prose as validation by itself; it records provenance, executes what can be executed, and preserves the evidential boundary of what remains qualitative, illustrative, conditional, or open.

The stable semantic baseline remains `v1.0.0`. B4/B4.10 does not assign a new semantic version and applies no core semantic changes.

## Inputs

B4/B4.10 used the canonical 39-concept / 40-relation / 5-domain registries, the B3 formal ontology and cardinality registry, the two CM-PharmE publication records, eight manuscript competency questions, eight manuscript OntoUML-informed anti-pattern categories, the vaccine-distribution scenario, publication-derived expert-review observations, and the repository-controlled ROBOT/HermiT workflow.

## 1. Structural and traceability validation

A computational cross-check was run over the B3 canonical reference ontology and registries.

**Result: PASS — 28/28 checks.**

Validated items include 39 canonical concept classes; 39 OWL object properties plus one generalization record (`CMPE-R0006`); five domains; stable-ID agreement between registries and the formal graph; 40 unique relation IDs; source/target and cardinality-registry agreement; lifecycle agreement; definitions, primary domains, and stereotypes for all concepts; valid relation domain/range references; 42 qualified cardinality restrictions; absence of historical converter cardinality classes; and graph equivalence of the four B3 reference serializations to the 1,086-triple packaged canonical graph.

This establishes strong structural traceability, not semantic completeness by itself.

## 2. Executable competency questions

The eight competency questions reported in the journal manuscript were implemented as SPARQL queries and executed against the ontology plus a constructed vaccine-distribution sample.

**Result: 8/8 bounded expected outcomes PASS.**

- CQ1 enterprise structure/capability/governance: PASS
- CQ2 ecosystem collaboration/partnership: PASS
- CQ3 process and clinical participation: PASS
- CQ4 governance/pharmacovigilance traceability: PASS, with manuscript-to-formal traceability note
- CQ5 digital-enabler connections: PASS
- CQ6 business-architecture / ontology traceability sample: PASS as a traceability query, not BACM conformance
- CQ7 five-domain application coverage: PASS as illustrative coverage, not adoption evidence
- CQ8 bounded extension scenario: PASS; 32 existing core classes across all five domains and zero scenario-defined classes

The executable queries improve reproducibility, but they do not transform CQ7 or CQ8 into empirical validation.

## 3. Vaccine-distribution scenario

A machine-readable Turtle sample was created using **only existing CM-PharmE classes and canonical relations**.

Schema check:

- 33 scenario individuals;
- 32 distinct core classes instantiated;
- all 5 domains represented;
- 34 CM-PharmE relation assertions;
- 0 unknown class assertions;
- 0 unknown relation predicates;
- 0 explicit domain/range compatibility violations.

**Result: PASS — bounded illustrative instantiation.**

### Publication-to-formal traceability findings

B4 identified places where the journal manuscript's application prose is broader or more direct than the canonical relation graph, including governance/compliance constraints, the pharmacovigilance reporting path, RWE/surveillance/risk interpretation, and application-oriented EHR/blockchain descriptions.

B4.10 disposition: **no ontology change merely to mirror manuscript prose**. These differences remain documentation/traceability findings unless future domain evidence establishes that a missing direct relation is part of the core semantics.

## 4. OntoUML-informed anti-pattern re-evaluation

The eight historical categories were rechecked using repository heuristics plus targeted semantic inspection.

### Confirmed clean within the checked scope

- Type–Role Confusion
- Event as Object
- Mode vs. Attribute Confusion
- Relation as Class

### Historical low-risk finding retained

- Overloaded Association: no single stable property was found with multiple conflicting domain/range definitions; generic `material relation` terminology remains provisional.

### Findings requiring disposition

B4.10 records five explicit decisions:

1. **Healthcare Provider (`CMPE-C0021`) — Role without explicit/inherited mediation:** `model-refinement-candidate`.
2. **Supply Chain Relationship / `CMPE-R0024` — mediation specificity:** `model-refinement-candidate`.
3. **PPP Structure / `CMPE-R0010` — part-whole semantics:** `defer-pending-domain-evidence`.
4. **Clinical Pathway / `CMPE-R0029` — Relator→Perdurant part-whole semantics:** `model-refinement-candidate`.
5. **Manuscript scenario prose versus formal graph:** `no-change-documentation-clarification`.

No semantic change was applied in B4.10. See `b4-10-semantic-finding-disposition.md` and `evaluation/evidence/b4-10-semantic-findings.yaml`.

## 5. Expert / semantic evidence

The later manuscript's four-expert qualitative review has been normalized into repository evidence without inventing new quotations, scores, demographics, or consensus statistics. Documented feedback concerned terminology precision, role-definition clarity, and retention of the five-domain structure.

**Result: PARTIAL.**

The evidence is traceable, but B4 did not perform a new independent expert panel. It therefore supports research provenance and refinement history rather than independent semantic validation.

## 6. Logical / reasoner validation

B4.10 introduced a repository-controlled GitHub Actions workflow using ROBOT `v1.9.10`, HermiT, Java 21, Python 3.12, and RDFLib `7.5.0`. The ROBOT JAR is pinned by SHA-256 before execution.

Validated GitHub Actions run:

- run ID: `31796520297`
- run number: `2`
- validated commit: `a9d6b38791435de51966804e81a1ca71db24e253`
- ROBOT/HermiT exit code: `0`
- run conclusion: **success**
- artifact ID: `9217570209`
- artifact digest: `sha256:e22464b746e420b81db8ef6bec8e0a08b71cd2afb0a9145bdb2674f589461af8`

**Result: PASS — executable OWL logical validation.**

ROBOT performs logical validation before classification and fails on inconsistency or unsatisfiable classes. The successful run therefore provides evidence that HermiT did not detect logical inconsistency or unsatisfiable named classes in the validated logical axiom set.

### Source-parity boundary

The GitHub modular source assembled to 888 triples while the B3 packaged canonical reference contains 1,086 triples. A graph-difference check found that the delta consists only of annotation/provenance predicates and contains **zero logical-predicate differences**. Thus the HermiT run evaluates the same logical axiom set, while annotation parity remains a repository-engineering follow-up.

Logical consistency does not resolve the open ontological-semantic questions described above.

## 7. Evaluation status by layer

See [`b4-evaluation-matrix.md`](b4-evaluation-matrix.md) for the E1–E9 evidence matrix.

- E1 Syntax — PASS
- E2 Logic — **PASS**
- E3 Structure — PASS
- E4 Ontological — CONDITIONAL
- E5 Semantic / Expert — PARTIAL
- E6 Data / Mapping — PASS, bounded
- E7 Competency Questions — PASS, bounded
- E8 Application — PARTIAL / illustrative
- E9 Reproducibility — **PASS for B4 scope**

## Final conclusion

B4/B4.10 materially strengthens CM-PharmE evaluation compared with publication-only evidence. It converts the eight competency questions into executable tests, creates a machine-readable cross-domain scenario, computationally verifies structural and registry traceability, turns historical anti-pattern and expert observations into versioned evidence, and now executes reproducible ROBOT/HermiT logical validation in GitHub Actions.

The evaluation also exposes useful discrepancies rather than hiding them. Three semantic findings remain model-refinement candidates, one is deferred pending domain evidence, and one manuscript/formal discrepancy is resolved as documentation clarification. No finding currently requires redesign of the five-domain architecture, and no reasoner-detected logical defect was found.

The appropriate conclusion is:

**B4/B4.10 evaluation evidence package: PASS with open, explicitly dispositioned semantic findings.**

**OWL logical validation: PASS for the current logical axiom set.**

**CM-PharmE stable-release readiness: NOT YET.**

Remaining blockers are no longer basic logical consistency. They are targeted semantic disposition/refinement decisions, annotation/provenance normalization of the GitHub modular source, stronger independent expert/domain evidence where required, and the broader build/release automation work planned for B5.
