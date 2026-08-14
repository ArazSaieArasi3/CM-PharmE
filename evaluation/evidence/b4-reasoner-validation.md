# B4 Logical / Reasoner Validation Attempt

## Objective

Execute an OWL DL reasoner against the CM-PharmE B3 canonical formal ontology and record consistency / unsatisfiable-class evidence.

## Target toolchain

- ROBOT: `v1.9.10` (current official GitHub release checked during B4 execution)
- Intended reasoner: HermiT via `robot reason --reasoner hermit`
- Java runtime available in the execution environment: OpenJDK 21
- Canonical input: B3 `ontology/source/cm-pharme.ttl`

The official ROBOT documentation states that the `reason` operation performs logical validation before classification and fails on inconsistency or unsatisfiable classes.

## Intended command

```bash
java -jar robot.jar reason \
  --reasoner hermit \
  --input ontology/source/cm-pharme.ttl \
  --output evaluation/evidence/cm-pharme-b4-reasoned.owl
```

## Execution result

**Status: BLOCKED / NOT EXECUTED**

The B4 execution environment contains Java but does not contain ROBOT, HermiT, ELK, JFact, Owlready2, or another OWL DL reasoner. Attempts to obtain the official ROBOT JAR were prevented by the runtime's external-network / binary-download restrictions. The official `v1.9.10` release metadata was verified separately, including the published ROBOT JAR SHA-256:

`16a73c074f3df359a7338a84b4e0788785fe06117f931bb9796e9619ea776105`

No substitute structural check is reported as a DL reasoner result.

## What was executed instead

B4 re-ran repository-local checks that do **not** replace DL reasoning:

- RDF/Turtle parsing;
- 39 concept / 40 relation / 5 domain inventory checks;
- domain/range and stable-ID referential integrity;
- 40/40 cardinality registry alignment;
- OWL restriction target checks;
- graph-isomorphism checks for the locally validated RDF serializations;
- targeted anti-pattern heuristics;
- executable SPARQL competency questions over a representative scenario.

These checks passed within their stated scope.

## Evidential boundary

E2 Logical Validation remains **NOT VERIFIED** until a documented HermiT/ELK/ROBOT execution is performed from repository artifacts. Consequently, B4 does not claim OWL DL consistency, absence of unsatisfiable named classes, or complete logical soundness.

This gap should be closed in the next automation/reasoner step, ideally through a reproducible GitHub Actions workflow.
