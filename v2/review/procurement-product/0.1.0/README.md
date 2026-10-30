# #350 — procurementProduct bounded semantics decision

The 695-element native review candidate remains untouched. The existing
association has `ProcurementActivity` and `MedicinalProduct` typed ends,
optional `0..*` bounds and a null stereotype. Under delegated AUTH-22-01,
PR-PRODUCT-01 chooses a documented **executed purchase/acquisition** involving
a medicinal product **type**. It is a source-qualified candidate claim,
not proof of physical receipt, delivered quantity, batch/consignment identity,
supplier qualification or verified world truth.

The Commission GDP 2013/C343/01, sections 4.2 and 5.2, separates transaction
records from pre-procurement supplier qualification; 5.4 discusses physical
receipt separately, and the glossary defines procuring. Those sections
motivate distinctions. The SHACL admission and candidate named-graph policy
are project choices, not legal compliance verdicts. See `sources.json` for
precise locators, `decision-card.json` for rejected/deferred alternatives and
costs, and `mapping-impact.json` for the next integration contract.

Fourteen independent and four combined cases were committed before the
admission profile and probe. `verify.py --output <dir> --check-committed`
checks the freeze hashes, native/existing experimental OWL typed ends, SHACL
admission, candidate-only named-graph projection and negative identity/time
inferences. This is a bounded decision; full-model scientific and author
disposition, other 46 older relation proposals and public Pages remain open.
