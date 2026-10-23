# G3-P5b — bounded legacy OLED adapter proof

The archived OLED/RefOntoUML parser and one actual anti-pattern implementation were compiled and exercised on **three small, officially schema-valid OntoUML JSON models** derived from the G3-P4a candidate. This establishes a narrowly tested JSON→XMI structural bridge. It **does not** establish an official full-model or 20-pattern anti-pattern result.

## Executed probe

- The archive `nemo-ufes/ontouml-lightweight-editor` was pinned to commit `42b926f6c2859dc87e49a96b8482eae28d02e7d5`; Java 17 with Eclipse ECJ 3.39.0 compiled the archived `RefOntoUML` parser and `BinOverAntipattern`. A bundled native sample loaded as 26 classes and 18 associations, calibrating the runtime.
- `make_toys.py` selected the actual `Organization`, `Facility`, `SupplyCapacity` classes and their primary capacity route as needed. Each toy JSON passed `ontouml-schema@1.0.2` and `ontouml-js@1.0.0` parsing. `to_refontouml.py` converted the fully typed, explicitly cardinalized subset to XMI; Python readback verified class and association counts, stable element ID crosswalk, relation-end types, order and bounds. The actual archived Java parser then independently loaded the XMI.
- **Positive BinOver:** Organization→Organization association, detected **1** occurrence. **Negative BinOver:** Organization→Facility association, detected **0**. **Typed route witness:** Organization→SupplyCapacity parsed as `CharacterizationImpl`, two ends, cardinalities `0..1` and `0..*` (reported by EMF as `0..-1`); BinOver **0**. See `probe-results.json` and the individual toy inputs/XMI.
- Four deliberate invalid inputs (missing cardinality, untyped end, unsupported Event stereotype, and omitted end subsetting) were **rejected** by the strict adapter. Nothing was filled with a guessed default. The full 536-element model is explicitly **refused**.

## Why the full model is still refused

`audit_full.py` produces `full-feasibility.json` against the exact G3-P4a native SHA. The old RefOntoUML Ecore has no direct `Event` or `Situation` classifier for **12** current classes (10 Event, 2 Situation). **11** relation ends are untyped; **66** ends in **33** relations have unspecified cardinality; **14** ends use subsetting or redefinition that this adapter does not yet map. All **144** classes carry explicit modern `restrictedTo` nature metadata without a direct legacy field; the toy report lists this information loss rather than hiding it. The native `SupplyCapacity` XOR explanatory note also has no executable legacy equivalent.

The blockers overlap: these counts are not independent defects. A conversion that coerces Event to a generic Class, supplies multiplicities, invents end types, or discards specialization could change detector findings. No such conversion has been submitted as evidence of cleanliness.

## Reproduce

Clone the archived OLED repository at the pinned commit with sparse checkout for `br.ufes.inf.nemo.antipattern`, `br.ufes.inf.nemo.ontouml`, and `br.ufes.inf.nemo.common`. Place the official ECJ 3.39.0 compiler JAR in a temporary path and install `ontouml-js@1.0.0`, `ontouml-schema@1.0.2`, `ajv@8.20.0`, `ajv-formats@3.0.1` in a temporary `node_modules`. Run:

```
python run_probe.py /path/to/pinned/oled /path/to/ecj-3.39.0.jar /path/to/node_modules
```

The report records the archive commit, compiler hash, library probe, model hash, Java classpath order, each toy output, structural checks and refusal guards. These dependencies are external to this review package; the complete reproducible source, input mini-models and evidence outputs are included here.

## Gate and exact next bounded task

Issue #310 and G3-P5 remain open; PR #305 remains draft. Next **G3-P5c**: establish a defensible treatment for the 12 Event/Situation classes and 144 explicit modern nature restrictions in a compatible full detector, with positive/negative witnesses and a machine-checked mapping/loss ledger. Then address end typing, unknown bounds and specialization; expand toy sensitivity to all 20 catalogue patterns before any full-candidate run and scientific disposition.
