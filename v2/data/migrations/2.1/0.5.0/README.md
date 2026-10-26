# RDB-M4 SupplyCapacity bearer projection — 0.5.0

Issue #321; ORSD FR-14 / FR-15. The scoped #309 bearer design is reused without
changing the native/OWL/SHACL candidate. The independent oracles, fixture
specification and six implementation decisions were frozen before implementation
at `e750774db38c9946c9d3abdb4c801c88df271301`.

## Contract and scope

The [semantic contract](semantic-contract.md) fixes the finite implementation
slice. A SupplyCapacity Mode uses its own public identity in a separately versioned
table. A SQL XOR constraint admits exactly one Organization or Facility foreign
key. Each Mode has one bearer; a bearer is not globally required to have a capacity.
The two primary Characterizations are exported bearer-to-Mode; inverse/common query
properties remain derived through the existing OWL axioms.

The observation remains a separate row and RDF individual. A new Mode cannot reuse
an existing observation public ID. Selecting an observation with kind
`supply_capacity` never causes the capacity exporter to instantiate a Mode. There
is no inferred Mode for the observation-only fixture facility.

All new records are **synthetic fixtures**: two capacity Modes (one per bearer
route), one complete synthetic capacity provenance chain, one capacity with
explicitly unknown provenance, and one separate capacity measurement. There are
**zero real capacity witnesses**. The version is the projection version, not an
empirical change in intrinsic Mode identity.

Where asserted, capacity provenance must have mutually aligned source, assertion
and evidence identities. Optional unknown provenance stays absent. Generic links
preserve SQL EvidenceSupport identity without asserting unresolved M025 role types.
The local [admission profile](admission.ttl) is a closed-world input contract, not
additional universal OWL axioms.

## Checks

| Check | Bounded expectation |
|---|---|
| Q21-04 capacity identity/bearer/provenance | Two complete normalized 11-field SQL/SPARQL tuples; one sourced and one unknown-source route |
| Q21-05 capacity observation | One separate normalized nine-field SQL/SPARQL tuple, with quantity, period, facility and source/assertion/evidence/run lineage |
| SQL | Nine expected rejections: missing/double bearer, swapped FK types, duplicate capacity ID, partial/invalid/misaligned provenance and observation public-ID reuse |
| SHACL | Fourteen fixed positive/negative expectations, including missing/multiple/wrong bearers, broad/inverse-only bypasses, observation/Mode collision and source misalignment |
| HermiT | Nine fixed expectations: positives, open-world missing bearer, co-referring IRIs, explicit inequality, disjoint bearer types, observation/Mode separation and capacity-free bearers |
| OWL RL | Exactly two derived common bearer pairs; no asserted common edge and no Mode inferred from the measurement |
| Native | Intrinsic Mode restriction, two primary typed Characterizations, 0..1 / 0..* ends and the existing combined-XOR note |
| W6 compatibility | Four legacy query pairs before/during/after, W6 validation while the addition is present, old observation query restored and identical pre-existing rows/schema/sequences/canonical KG after cleanup |

Two organization IRIs need not be different under OWL. The corresponding closed
graph still fails SHACL when it provides two bearer nodes; the explicit
`owl:differentFrom` witness makes the exact-one OWL restriction inconsistent.
A missing asserted bearer similarly fails admission while remaining possible
under OWL's open-world semantics.

## Reproduce

Use a disposable copied PostgreSQL 16 / PostGIS 3.4 database, Python 3.12, Java 21
and the dependency versions pinned in `.github/workflows/v2-21-rdb-m4.yml`.

```sh
python tools/v2_data/bootstrap_ingest.py --reset --report build/v2-21-rdb-m4/ingest.json
python v2/data/migrations/2.1/0.5.0/verify_m4.py
```

An RDF-only local subset is available:

```sh
python v2/data/migrations/2.1/0.5.0/verify_m4.py --offline --output-dir build/v2-21-rdb-m4-offline
```

The offline report explicitly excludes PostgreSQL, SQL constraints, paired SQL
queries and rollback. The full hosted run is required for issue closure.

The additive table/function are removed in a finally block after a successful seed
transaction. Existing tables use collision-checked explicit negative test IDs;
their sequences never advance. Pre-existing row/schema, sequence and graph hashes
must match after cleanup. This prototype does not modify the stable W6 schema,
views, defaults, mapping registry or generic exporter.

## Measurement boundary

The fixture quantity is 120 synthetic packages per reporting period. It is not
a measured production rate. Reporting-period dates use the existing midnight-UTC
normalization convention in the RDF view; they are not observed event instants.
The 2.1 view explicitly types the selected observation_kind as
SupplyCapacityObservationResult. The unchanged historical generic W6 exporter has
its existing reimbursement metric representation; this run does not reclassify
that frozen baseline or claim broader measurement semantics were resolved.

## Release boundary

This is a typed-bearer database prototype. Completing all four M1–M4 slices does
not mean all 36 ontology/database mappings, real-source coverage, ORSD content,
full anti-patterns, four-module semantics, human/expert review or publication are
complete. #306 remains open and PR #305 remains draft until those gates pass.
