# RDB-M4 scoped SupplyCapacity contract — 0.5.0

Issue #321; ORSD FR-14 / FR-15. Reuse the scoped #309 typed-bearer decision.
The candidate, author/scientific review and full publication remain under #306.

| ID | Adopted scoped implementation choice | Evidence and boundary |
|---|---|---|
| M4-D01 | SupplyCapacity remains a Mode with its own public identity in a separately versioned 2.1 projection table. | Reuse existing native intrinsic-mode restriction. `projection_version` identifies this mapping, not a newly observed capacity or a Mode change. |
| M4-D02 | Each admitted Mode has exactly one typed Organization or Facility bearer across two nullable foreign-key routes. | SQL XOR plus per-table FK; native bearer-to-Mode Characterizations; existing OWL exact-one union; closed-world SHACL. Existing entities are not merged. |
| M4-D03 | A capacity observation remains in observation_result; it never creates a Mode or assigns a bearer merely because a measurement exists. | Separate public IDs and graph kinds. The new capacity table rejects an existing observation public ID. The exporter selects capacities only from the capacity table. |
| M4-D04 | Preserve unknown capacity provenance. Where a source is asserted, source/assertion/evidence must all be present and mutually aligned with the typed bearer and Mode. | One synthetic capacity has a synthetic source route; another is explicitly unknown. Do not fabricate a real source or promote unresolved M025 EvidenceSupport semantics. |
| M4-D05 | Preserve all pre-existing W6 rows, schema, views, defaults, sequences and canonical old graph after reversible cleanup. | Use an additive table/guard and collision-checked explicit negative fixture keys. Legacy four-pair queries run before/during/after; a separate capacity-observation query checks the new scoped projection. |
| M4-D06 | Freeze expectations and fixtures before implementation; keep source/evidence and closed/open-world interpretations distinct. | OWL missing bearer can be consistent; two organization IRIs can co-refer unless explicitly different. SHACL/SQL reject incomplete/multiple bearers. No capacity is globally required for an Organization or Facility. |

## Finite execution stages

1. Freeze this contract, fixture specification, pinned inputs and independent oracles.
2. Execute two capacity routes, a separate observation, SQL/RDF query parity,
   source-alignment/identity boundaries, native anchors, SHACL/OWL and rollback.
3. Inspect hosted PostgreSQL/PostGIS evidence, register outcomes and close only the
   bounded #321 contract if all acceptance criteria pass.

All new records are synthetic test fixtures. The historical NHIF sample supplies
no SupplyCapacity witness. Synthetic source identity proves provenance mechanics,
not empirical truth. Existing P1 nonregression is not real capacity validation.
The observation's fixture quantity is packages per reporting period. It is neither
a production-rate claim nor a source of a Mode. A general measurement-to-Mode
aboutness relation, temporal capacity identity and richer units remain separate
scientific questions; this slice does not silently settle them.

The frozen W6 generic exporter is retained, including its historical metric
representation. M4 provides an explicit 2.1 SupplyCapacityObservationResult view for
the selected observation_kind; it does not rewrite the old output or claim that
W6 historically exported every capacity observation with the new 2.1 subtype.
