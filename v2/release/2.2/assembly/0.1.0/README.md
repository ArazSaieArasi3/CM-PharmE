# Governed 2.2 reconciliation assembly — experimental review copy

Date: 2026-10-30, Asia/Tehran. Packet: #344. This implements the input
reconciliation identified in #343, using one [assembly manifest](inputs.json).

The [native review copy](ontouml-experimental.json) contains all 536 elements of
the later EvidenceRecord/ContextClass candidate plus the 150 previously separate
experimental elements (49 binary relations, 98 relation ends, three classes).
Every non-package baseline element is preserved exactly. All **22 shared-field
differences** retain the later candidate's value, including FacilityOperation,
ContextClass and EvidenceRecord. No old experimental value replaces a later one.
Package membership is merged; only explicit project labeling identifies the
new review copy. The original files and their namespaces remain unchanged.

| Reconciled review copy | Result |
|---|---:|
| Total native elements | 686 |
| Class records including six datatypes | 147 |
| Named non-datatype classes | 141 |
| Binary relations | 135 |
| Components / isolated named classes | 1 / 0 |
| Later shared-field decisions preserved | 22 / 22 |
| Individually crosswalked added relations | 49 / 49 |

The **zero-isolate result is structural and provisional**. It combines the
previous connectivity experiment with later native decisions without rollback;
it does not accept the proposed relations, prove their truthmakers or establish
complete semantic coherence. The vendored official JSON schema passes for this
serialization; full semantic OntoUML validation and native detector acceptance
remain separate. Three negative controls reject a later-field rollback, a dropped
new relation end and silently strengthened proposed cardinality.

[relation-crosswalk.csv](relation-crosswalk.csv) records each added relation's
native ID, proposed full property IRI, directed typed endpoints, prior
requirement/source locator, individual evidence path, unresolved semantic issue
and pending acceptance. All 49 proposed native endpoint pairs agree with their
existing formal declaration names. This is narrower than full formal alignment.

The manifest keeps the later formal base/deltas and older experimental formal
declarations in **separate lanes**. It deliberately does not union an older full
ontology over newer constraints. It also pins local admission profiles, whose
required fields are not universal participation claims. Native/OWL/SHACL constraint
alignment remains a named blocker for individual decisions, not a green result
inferred from matching names. All 87 original Gate-D IDs and 138 baseline formal
declarations remain accounted for by the prerequisite crosswalks. The earlier
AssetAtRisk/Vulnerability/ClinicalCareParticipant deferrals are retained for
scope reassessment; this assembly neither deletes nor automatically reinstates them.

Reproduce with rdflib==7.5.0 and jsonschema==4.26.0:

```bash
python v2/release/2.2/assembly/0.1.0/build.py \
  --output build/comprehensive-22-assembly --check-committed
```

[report.json](report.json) records the derived bytes, topology, 62 input identities,
preservation guards and explicit scientific limits. Hosted evidence is recorded
separately when verified. Comprehensive 2.2 remains **not ready**; no stable tag,
full-model public documentation, scientific acceptance or expert response is
created by this review assembly. The released 2.1.0 M1 profile is unchanged.

The next bounded packet is #345, a logisticsFacility decision card. Its recorded
blocker is concrete: the bare Facility end does not identify origin, destination
or storage participation. Compare justified participation/site alternatives and
fix independent witnesses before implementing an accepted semantic change.
