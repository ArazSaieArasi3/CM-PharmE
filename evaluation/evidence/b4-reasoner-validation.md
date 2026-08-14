# B4.10 Logical / Reasoner Validation

## Objective

Execute a reproducible OWL DL reasoner workflow against the CM-PharmE B3 logical ontology and record consistency / unsatisfiable-class evidence without substituting structural checks for formal reasoning.

## Toolchain

- GitHub Actions workflow: `.github/workflows/ontology-reasoner.yml`
- ROBOT: `v1.9.10`
- ROBOT JAR SHA-256: `16a73c074f3df359a7338a84b4e0788785fe06117f931bb9796e9619ea776105`
- Reasoner: HermiT via `robot reason --reasoner hermit`
- Java: Temurin 21
- Python: 3.12
- RDFLib: `7.5.0`

ROBOT's documented `reason` behavior performs logical validation before classification and exits non-zero on inconsistency or unsatisfiable classes.

## Reproducible source assembly

The GitHub ontology is authored as recursive Turtle modules under `ontology/source/modules/`. `tools/ontology/assemble_modules.py` parses all modules, unions them as an RDF graph, serializes the validation input, and writes a checksum manifest.

Validated assembly:

- module count: **49**
- assembled unique RDF triples: **888**
- assembled Turtle SHA-256: `61d9d4a3ce8f3307da42945ca8f41cdc8829cd31411c9e501957c5d075dde28a`

A separate parity check against the B3 packaged canonical Turtle (1,086 triples) found annotation/provenance differences but **zero logical-predicate differences**. Therefore the workflow reasons over the same logical axiom set while annotation parity remains a separate engineering follow-up. See `b4-10-source-parity.json`.

## Executed GitHub Actions run

- workflow name: **Ontology DL Reasoner Validation**
- run ID: `31796520297`
- run number: `2`
- event: `push`
- validated branch: `evaluation/b4-paper-grounded-validation-v1`
- validated commit: `a9d6b38791435de51966804e81a1ca71db24e253`
- overall run conclusion: **success**
- HermiT/ROBOT exit code: **0**

All workflow stages completed successfully, including:

1. repository checkout;
2. Python and Java setup;
3. RDFLib installation;
4. modular-source assembly;
5. ROBOT download and SHA-256 verification;
6. ROBOT/HermiT logical validation and classification;
7. machine-readable summary creation;
8. evidence artifact upload;
9. final enforcement of reasoner exit code.

## Artifact evidence

- artifact name: `cm-pharme-b4-10-hermit-evidence`
- artifact ID: `9217570209`
- artifact digest: `sha256:e22464b746e420b81db8ef6bec8e0a08b71cd2afb0a9145bdb2674f589461af8`
- retention: 30 days from the run
- reasoned OWL SHA-256: `a6e6333f886d418917dff60dbbb96f8c608ed2f9792de9f8bd93382842bc0e9f`

The uploaded artifact contains the assembled Turtle source, source assembly manifest, ROBOT version record, HermiT exit code, reasoner summary, reasoned OWL output, and reasoner log. No unsatisfiable debug module was produced by the successful run.

## Result

**Status: PASS — repository-executed ROBOT/HermiT logical validation.**

The successful ROBOT/HermiT execution provides evidence that, for the validated logical axiom set:

- ROBOT completed logical validation and classification;
- HermiT did not report ontology inconsistency;
- HermiT did not report unsatisfiable named classes that would make ROBOT `reason` fail.

## Evidential boundary

This closes the specific B4 gap around executable OWL logical validation. It does **not** prove:

- pharmaceutical-domain completeness;
- empirical effectiveness;
- correctness of every UFO/OntoUML modeling choice;
- reference-architecture adoption;
- FHIR, IDMP, BACM, or other standards conformance;
- correctness of application-level manuscript prose;
- semantic adequacy of the open role/mediation and part-whole findings.

Those concerns remain separated into the relevant B4 evaluation layers and semantic finding dispositions.
