# G2 source-bounded connectivity checkpoint

2026-10-05. Candidate implementation in draft PR #305; not a release or a global
OntoUML conformance claim. This snapshot extends the G1 checkpoint at commit
`17219243186df6b86056cfeeb906de2d9862c8c9` without editing it.

## What was decided and implemented

All **15** rows of the connectivity register were inspected against the W3/W4
specifications, W2 source boundaries, W6 source/mapping contracts and W7-E6
findings. Four were already implemented; five now have bounded implementations;
six remain explicitly deferred. This is a technical disposition under the
user's instruction to execute the next gate, not a claim of new expert sign-off.

| Register item | Candidate properties | Meaning / boundary |
|---|---|---|
| C03 | observationAboutProduct; observationAboutPresentation | Separate information-aboutness targets; both specialize observationResultAbout. The parent is not globally restricted to Product. |
| C04 | assertionAboutProduct | Product-specific assertion topic. Other entity/relation targets remain for G3; asserted content is not thereby true. |
| C06 | riskAssessmentConcernsDependency | Dependency as assessment topic, specializing riskAssessmentConcerns. No risk score, asset or vulnerability instance is inferred. |
| C08 | disruptionAffectsDependency | Evidence-supported impact specialization of disruptionAffects; no causal shortage conclusion. |
| C11 | reimbursementDiagnosisContext | Diagnosis-classification context of an aggregate reimbursement/utilization result, not a patient diagnosis. |

No new classes, global restrictions on the generic parent properties, mandatory
participation, or artificial hub classes were introduced. The six new properties
have `0..*` multiplicities on both ends in the native projection. Their exact
OntoUML relation stereotypes remain G3 questions, explicitly unfilled rather than
being labeled formal/material without justification.

Existing C01/C02/C05/C15 patterns remain. Deferred items are:

- **C07:** optional safety source S3 has no activated, frozen mapping here.
- **C09/C10:** procurement/stockout need conditional C1 row-level participant,
  product/presentation, facility and time evidence. Source licensing and
  redistribution boundaries remain; no raw C1 data was republished.
- **C12:** digital support needs an admitted concrete use case beyond V1 lineage.
- **C13:** no source-backed service offerer/specification commitment.
- **C14:** preserve the G1 clinical-role deferral; no Organization-only shortcut.

The exact original evidence pointers, disposition and rationale for every item
are in `connection-dispositions.json`. Source paths and hashes are in
`source-evidence.json`. No held-out source was used for concept admission.

## Results

| Measure | G1 | G2 |
|---|---:|---:|
| Active concepts | 125 | 125 |
| Classes / datatypes | 119 / 6 | 119 / 6 |
| Object properties | 57 | 63 |
| Named-class graph components | 19 | 15 |
| Largest component | 79 classes | 105 classes |
| Isolated classes | 17 | 14 |

Connectivity uses the same named-subclass plus named domain/range projection as
G1. Anonymous expressions, datatypes and untyped endpoints are excluded. These
numbers are not comparable to a different drawing's component count, and graph
connectivity alone is not semantic quality. The three previously isolated types
now connected are DiagnosisClassificationReference, DisruptionEvent and
RiskAssessmentActivity; another previously separate component is also joined.

## Executed validation

- The unchanged **120 G1 scenarios** pass under the G2 ontology and constraints.
- **24 G2 cases** pass: a positive, wrong-source-type, wrong-target-type and
  multiple-target case for each of the six new properties. Wrong types are
  rejected using SHACL without domain/range inference masking the input error.
- All G1 class declarations, protected distinctions and logical axioms remain;
  only candidate version/status annotations are replaced. No deferred class is
  reactivated and no existing parent property's range is narrowed.
- Official OntoUML JSON schema validates **434 elements**, with zero errors;
  identifier/reference checks pass separately.
- **HermiT and Pellet 2.3.1** each pass schema-only and schema with the G1/G2 and
  NHIF synthetic witnesses, with zero unsatisfiable named classes.
- **OWLAPI 3.4.3 OWL 2 DL profile:** zero violations for both inputs. Exact
  versions, scopes and input hashes are in `reasoner-results.json`.

## A concrete mapping gap addressed in the candidate

The frozen W7-E6 report explicitly documented diagnosis fields as relationally
retained but absent from the W6 RDF projection. This candidate adds a separate
experimental projection using the repository's **seven pre-existing synthetic
NHIF fixture rows**, preserving the frozen adapter and its published scores.

- 7 source rows → 21 metric observation results (patient count, package count,
  BGN cost), with 42 new presentation/diagnosis link assertions.
- SQL and SPARQL return exactly the same 21 observation/presentation/diagnosis/
  source-row tuples; SHACL passes. All seven source rows remain traceable.
- No Patient individual is created from aggregate counts.
- Presentation witness identifiers use the fixture scope plus NHIF code and
  packaging/concentration/package size. This is a fixture-specific construction,
  not a claim that a lexical code is universal entity identity.
- Diagnosis labels are fixture labels, not independently validated ICD content.

Loadable SQL, RDF and measured results are in `lab/nhif-candidate-projection.sql`,
`lab/nhif-candidate-projection.ttl` and `lab/nhif-projection-results.json`.
Lab provenance metadata is retained in the projection but excluded from the
OWL reasoner input, whose scope is declared. The original W6 adapter is unchanged.
This work does **not** constitute ingestion or evaluation of full real NHIF data.

## Remaining gates and exact next step

G2 technical inspection is complete for 15/15 register rows; six evidence/scope
deferrals remain. This is bounded progress, not an unconditional release gate.

**Next: G3-1 — resolve the nine inherited Role grounding definitions.**
For each role, identify its identity provider, actual relational/event context,
whether the role can end while its bearer persists, the defining relation and
cardinalities, and a rejecting counterexample. Start with ManufacturerRole and
ManufacturingSiteRole; a facility operation or registration alone must not be
misrepresented as proof of a manufacturing occurrence.

Then G3-2 resolves **42** relation records (36 carried from G1 plus six new G2
relations) requiring OntoUML stereotype and/or multiplicity disposition, and
G3-3 runs the selected native semantic validator and anti-pattern engine. The
schema pass above does not replace either. Nine old Role definitions and all
14 graph isolates are explicitly visible in `model-validation.json`.

G4 still requires full source-mapping/held-out regression and Wiki/Pages/article
traceability. G5 requires author review of unresolved findings and the final
scope before the comprehensive OntoUML diagram and release designation. No final
diagram, merge, tag or publication claim is made by this checkpoint.

## Reproduce

Use the G1 pinned requirements, Java 17+ with its compiler module, and the
unchanged G1 snapshot. From repository root:

```bash
python tools/v2_ontology/g2_connections.py
```

The script runs the model build, G1 regression, new bridge checks, fixture
projection, both reasoners and profile checks. RDF blank-node ordering and
artifact byte hashes may vary; graph semantics and outcomes are the comparison
targets. Source hashes refer to the pinned evidence revision above.
