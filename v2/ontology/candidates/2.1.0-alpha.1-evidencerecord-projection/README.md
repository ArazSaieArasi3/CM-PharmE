# EvidenceRecord typed projection candidate — 0.1.0

Issue #323; parent #310 and scientific release #306 remain open. Profile
**CMPE-EvidenceRecordProjection/0.1.0**, admission contract
**CMPE-QualifiedEvidenceWitness/0.2.0**. Separate native candidate based on
#322, with exactly seven field changes and all previous artifacts preserved.

[Decision](decision.md), [exact permitted delta](contract.json) and
[independent outcomes](fixed-oracles.json) were frozen at
`799cb885a9bb0a65c4d8aad5601b328c91d73a07` before implementation.
EvidenceRecord becomes a derived unstereotyped Association over an eligible
existing evidenceItem fact, with target EvidenceSourceRecordRole 0..1 and inverse
0..*. Target readOnly=true, inverse=false. Primitive evidenceItem target becomes
readOnly=true under the explicit established-support-identity policy. This does
not make the supported assertion true or infer record identity from external codes.
The native schema supports the selected association representation; independent
scientific relation-category and identity acceptance remain pending.

## Explicit witness-contract transition

The historical `X-BA-COMMITMENT-missing-source-evidence` witness already contains
an evidenceItem fact and explicit EvidenceSourceRecordRole. It lacks only the
redundant shortcut. The original false expectation and full-C **88/89** observation
remain unchanged. The prospective contract admits it after deriving that view.
The existing primitive evidence must still be present and qualified; genuine
missing-primitive and missing-role replacements remain rejected. No primitive fact
or qualified role is fabricated from SourceRecord alone or an asserted shortcut.

Local evidence: **12/12 new SHACL**, **12/12 preserved ContextClass**,
**10/10 finite identity**, **6/6 HermiT** expectations, two bounded subsetting rows,
six unauthorized-change refusals and native schema/guarded serialization pass.
For all 89 historical rows, the previous ContextClass contract passes **89/89**;
the new model matches the original historical oracle on **88/89**, and the
explicitly versioned prospective contract on **89/89**, with exactly one declared
transition. This is a semantic migration, not a silently updated historical test.
[local-results.json](local-results.json) retains every original/prospective outcome.
Hosted evidence is recorded after execution.

[ontouml.json](ontouml.json) preserves all 536 identities, modern nature, roles
and specialization references. Relative to #322, unknown readOnly/cardinality
inventories decrease **78/62 to 76/60**; eleven untyped and fourteen specialized
Properties remain. [input-impact.json](input-impact.json) separately lists the
primitive mediation input inventory; these counts are not detector findings.
Raw parser defaults are restored to original source nulls before further use.

```sh
npm ci --ignore-scripts --prefix v2/ontology/candidates/2.1.0-alpha.1-evidencerecord-projection/runtime
python v2/ontology/candidates/2.1.0-alpha.1-evidencerecord-projection/verify_slice.py \
  --node-modules v2/ontology/candidates/2.1.0-alpha.1-evidencerecord-projection/runtime/node_modules
```

The OWL delta makes the inherited required primitive evidenceItem explicit and
adds bounded view restrictions. Operational typed projection plus exact SHACL is
still needed; OWL does not implement complete temporal/closed-world semantics.
Passing selected checks does not certify a complete modern validator, full
20-family anti-pattern execution, independent scientific acceptance, production
migration or final release. #310/#306/#315 remain open; PR #305 stays draft.
Next publication work is an explicitly experimental RC scope/claim freeze and
reproducible package, as documented in the release-planning route.
