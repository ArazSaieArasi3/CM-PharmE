# ContextClass typed projection candidate — 0.1.0

Issue #322; parent #310 and scientific release #306 remain open. Profile
**CMPE-ContextClassProjection/0.1.0**. This is a separate full native review
candidate derived from the pinned P3 model, not a replacement of that historical
snapshot or the four-rule source-policy evidence bundle.

[Decision](decision.md), [exact contract](contract.json) and
[independent oracles](fixed-oracles.json) were frozen at
`be6dd2c67ff2bb33071813a4360790f83d4f5efe` before implementation.
Four unknown Boolean values and four unknown bounds are replaced by documented
candidate design decisions. Two primitive target readOnly declarations change
from false to true under the explicit assignment-identity policy. Two relations
become derived unstereotyped Associations. Exactly **14 fields** change; all
536 element IDs, role types, nature and specialization references are preserved.
The unstereotyped Association is deliberate in this native profile; broader
scientific relation-category acceptance is not claimed.

| View | Primitive edge | Typed source | Typed target | Target / inverse |
|---|---|---|---|---|
| contextClassificationEntry | classificationEntry | ContextualMedicineClassificationAssignment | AppliedClassificationEntryRole | 1 / 0..* |
| contextClassificationProduct | classificationEntity | ContextualMedicineClassificationAssignment | ClassifiedMedicinalProductRole | 0..1 / 0..* |

Materialization requires an existing primitive fact and eligible explicit named
types/subtypes. It does not infer a product Role from Product alone, invent a
primitive edge from a shortcut, or derive evidenceRecord. Substance assignments
therefore remain admitted without a product projection. A generic assignment
need not appear in a contextual view. Exact SHACL projection checks and the
operational rule implement the views; OWL restrictions alone do not establish
exactness or temporal immutability.

Local verification passes **12/12 SHACL cases**, **89/89 historical SHACL
expectations before and after only these two projection rules**, **10/10 bounded
identity traces**, **4/4 OWL/HermiT expectations**, **4/4 bounded native subsetting
rows** and **6/6 unauthorized-change refusals**. Native schema and guarded
serialization pass; 78 parser-defaulted unknown Booleans are restored to source
nulls. [local-results.json](local-results.json) retains exact evidence. The
historical full-C experiment's 88/89 observation is preserved; this scoped
migration does not include the evidenceRecord rule that changed that contract.
Hosted results are recorded after execution.

The new candidate has **78 unknown readOnly flags and 62 unknown cardinalities**,
compared with 82/66 in the pinned P3 source. Eleven untyped Properties and fourteen
specialized Properties remain; these inventories overlap and are not detector
findings. The model has not passed a complete modern validator or full 20-family
anti-pattern execution. Independent author/scientific acceptance remains pending.
No production migration, final release or merge is authorized by this evidence.

Reproduce with Python dependencies from contract.json, Java 17 and Node:

```sh
npm ci --ignore-scripts --prefix v2/ontology/candidates/2.1.0-alpha.1-contextclass-projection/runtime
python v2/ontology/candidates/2.1.0-alpha.1-contextclass-projection/verify_slice.py \
  --node-modules v2/ontology/candidates/2.1.0-alpha.1-contextclass-projection/runtime/node_modules
```

The actual native serialization is guarded using original JSON as authoritative;
raw parsed booleans must not be used as domain facts. [ontouml.json](ontouml.json)
is the generated candidate, [traceability.csv](traceability.csv) records the
14 changes, [owl-delta.ttl](owl-delta.ttl) is only the bounded restriction delta,
and [combined.shacl.ttl](combined.shacl.ttl) is the reproducible shape output.
Next bounded task: evidenceRecord/EvidenceSupport semantics, including its
separate historical contract-transition decision. PR #305 stays draft.
