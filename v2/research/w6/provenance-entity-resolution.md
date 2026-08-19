# W6 Provenance, Geography and Entity-Resolution Design

## Provenance
W6 treats provenance as operational data, not prose-only documentation. Each fixture/source row receives a deterministic SHA-256 fingerprint and is linked to a `DatasetRelease` and `TransformationRun`. Normalized assertions are linked back through explicit `EvidenceSupport` records.

This allows a normalized observation or assertion to answer four separate questions:
1. which dataset supplied the evidence;
2. which dataset release/file contract was used;
3. which source record supported it;
4. which transformation activity produced the canonical representation.

No provenance is invented when it is unavailable.

## Identifier policy
Source identifiers are stored through explicit identifier schemes and assignments. The current reference implementation includes hooks for NHIF product and hospital codes. The architecture also supports later FDA/openFDA/EMA/GeoNames identifiers without treating any single identifier as universal identity.

## Geography
Source geographic labels are normalized through a separate alias table containing source system, original value, normalized value, resolution method and confidence. Geographic entity identity is distinct from source labels and from regulatory jurisdiction.

PostGIS fields and indexes prepare the representation for later actor/facility geospatial evaluation. The W6 CI fixture does not claim external GeoNames resolution or geocoding accuracy.

## Entity resolution
The entity-resolution representation uses explicit assertions:
- two source-record references;
- canonical matched entity type and identifier;
- match method;
- confidence;
- status (`accepted`, `ambiguous`, `rejected`).

The architecture therefore supports reversible and auditable matching. An ambiguous match need not modify canonical entity identity.

## Current W6 fixture evidence
The schema-faithful fixture produces two accepted exact product-presentation match assertions based on compatible NHIF product-code and normalized presentation information across the outpatient and inpatient test contracts. These two matches verify execution mechanics only; they are **not** a real-world precision/recall evaluation.

## W7 hand-off
W7 may evaluate entity resolution on a defensible real overlap or gold subset if one can be built without leakage. Any reported accuracy metric must come from that future evaluated set, not from the W6 fixture.