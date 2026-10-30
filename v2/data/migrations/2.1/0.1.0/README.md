# CM-PharmE 2.0→2.1 relational delta inventory — 0.1.0

This is the completed **read-only #317 inventory and conditional migration contract** for the CM-PharmE 2.1 research candidate. No W6 schema, source record, ontology or `main` content was changed. The current ontology remains draft [PR #305](https://github.com/ArazSaieArasi3/CM-PharmE/pull/305), not release 2.1.

## Pinned comparison and reproducer

| Layer | Pinned ref / input | Interpretation |
|---|---|---|
| W6 integrated 2.0 line | `v2/research-program` at `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`; `v2/data/db/schema.sql`, `views.sql`, 36-row `ontology-rdb-mapping.csv`, 2.0 ontology source modules, 2.0 SHACL | W6 reference architecture, not full external ingestion or 2.1 coverage. The candidate branch carries byte-identical copies of these W6 inputs. |
| 2.1 candidate | `v2/connectivity-audit-2-1-candidate` at `1356b155a73c7586a368b9f0816a70004cfa6d73`; `2.1.0-alpha.1-g3-p4a-supply-capacity/{ontouml.json,active.ttl,constraints.ttl}` | Latest integrated P4a model snapshot, with broader P3 decisions still pending. |
| Requirements | ORSD document 0.2.0 `requirements.json` | Stable row IDs and exact named anchors, pending author semantic review. |

All 14 source file SHA-256 values are in [pinned-inputs.json](pinned-inputs.json). Reproduce from repository root with RDFLib 7.6.0:

```bash
python v2/data/migrations/2.1/0.1.0/build_inventory.py
```

The script fails if any pinned input changes. It regenerates [term-delta.csv](term-delta.csv), [w6-mapping-crosswalk.csv](w6-mapping-crosswalk.csv), [simple-shape-delta.csv](simple-shape-delta.csv) and [inventory-results.json](inventory-results.json). The old `formal-baseline.json` describes an earlier 642-triple W5 formal checkpoint; **this** pinned integrated 2.0 source-module set has 664 triples. Do not substitute one fingerprint for the other.

## What differs

| Declared local term type | W6 2.0 | 2.1 candidate | Shared names | Added names | Absent in candidate |
|---|---:|---:|---:|---:|---:|
| OWL classes | 81 | 138 | 78 | 60 | 3 |
| Object properties | 52 | 86 | 52 | 34 | 0 |
| Datatype properties | 5 | 5 | 5 | 0 | 0 |

The three absent classes are `AssetAtRisk`, `Vulnerability` and `ClinicalCareParticipant`, documented as deliberate candidate deferrals in G3-F. The 232-row term inventory also marks **45 retained terms with changes to selected explicit OWL signature components**; this is a review queue, not a count of approved semantic changes. The simple SHACL structural comparison yields 107 asymmetric constraint records, including the `FacilityOperation` endpoint cardinality/type change. It deliberately does not cover SPARQL constraints, composite and qualified paths or logical equivalence. Same local name across `/2.0/` and `/2.1/` is **not** proof of meaning-preserving identity.

The 36 W6 mapping registry terms all have a declared candidate term by local name, including M023 `MatchConfidence`, which the registry calls a `quality` but OWL declares as a class. Only 34 registry rows name an existing table; M035 `DataSourceResource` and M036 `ObservationActivity` were explicitly deferred in W6. These counts establish identifier/table availability only. `export_kg.py` currently lacks a `facility_operation` export branch; its registry row M011 does not imply an executable RDF round trip.

## Decisions required before DDL

The [14-row decision ledger](decision-ledger.csv) classifies each material change by old table/column, candidate semantics, scientific state, compatibility, reversibility and ORSD ID. In particular:

- **FacilityOperation:** W6 has one `organization_id` per operation and its 2.0 SHACL requires exactly one. The 2.1 candidate's `operationOrganization` SHACL requires at least one `OperatingOrganizationRole` with no max; `operationFacility` is exactly one `OperatedFacilityRole`. Retain the current schema while #306 adjudicates multi-operator semantics; a join table is a conditional migration, not a decision already made. The direct `operates` triple also needs an explicit derivation/export policy (FR-01/FR-03).
- **SupplyCapacity:** the Mode existed as a 2.0 class but lacks a W6 table. The P4a scoped accepted bearer route adds typed Organization-or-Facility XOR semantics. W6's `observation_kind='supply_capacity'` is an aggregate *result*, not the Mode; a new Mode row must not be invented from it (FR-14/FR-15).
- **Identity, responsibility, provenance and quality:** retain separate Organization/Facility tables and stable identifiers; manufacturer/import/wholesale responsibilities require contextual relators, not name matching. W6 has source-release-run and assertion-evidence tables but no operation-level evidence FK. M023's scalar confidence is a bounded projection of `MatchConfidence`, not proof of a 2.1 Quality instance (FR-01/02/03/25/26/29).
- **RM/PV/BA/DS:** four experimental small-ontology interfaces remain under #311–#314. They do not receive premature tables. The three absent 2.0 classes do not trigger a DROP.

The [migration contract](migration-contract.md) defines testable relational constraints, positive/negative/boundary rows, SQL↔SPARQL tuple parity, RDF round trip, provenance and rollback. Its example 2.1 RDF identifier export is explicitly proposed. No SQL migration was executed in this inventory.

## Sized implementation queue

| Order after relevant scientific decision | Issue | Result required |
|---|---|---|
| 1 | [#318 — versioned namespace and provenance projection](https://github.com/ArazSaieArasi3/CM-PharmE/issues/318) | Parallel 2.0/2.1 regression, identity and lineage preserved |
| 2 | [#319 — FacilityOperation projection](https://github.com/ArazSaieArasi3/CM-PharmE/issues/319) | Adjudicated cardinality, typed roles, SQL↔SPARQL and reversible migration |
| 3 | [#320 — first responsibility context](https://github.com/ArazSaieArasi3/CM-PharmE/issues/320) | Manufacturer slice with truthmaker; import/wholesale separately later |
| 4 | [#321 — SupplyCapacity bearer](https://github.com/ArazSaieArasi3/CM-PharmE/issues/321) | Distinct Mode and measurement, typed XOR, source/evidence and rollback |

Each issue is scoped to 1–3 runs, and depends on its named semantic and source gates. #307 remains the separate NHIF P1 file-contract and hosted PostgreSQL/PostGIS verification issue. Inventory completion does not certify that W6 has been deployed against the whole external source or that 2.1 is ready for publication.
