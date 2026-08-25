# V2-078 entity/relationship browser implementation checkpoint

Issue: #147  
Parent: W8 #22  
Depends on: V2-076 #143 ✅; V2-077 #145 ✅

## Executed in this checkpoint

1. Froze the browser-facing semantic surface from the canonical W6 ontology↔RDB mapping registry in `entity-relationship-browser-mapping-freeze.csv`.
2. Added read-only T01/T03 SQL in `v2/app/observatory/sql/entity-relationship-browser.sql` for:
   - MedicinalProduct detail with bounded primary-substance and identifier/source lineage;
   - Organization↔Facility traversal only through registered `FacilityOperation`;
   - `presentationOf` traversal through M015;
   - bounded `hasActiveSubstance` traversal through M016.
3. Preserved hard boundaries:
   - Organization ≠ Facility;
   - MedicinalProduct ≠ MedicinalProductPresentation;
   - lexical/source identifiers ≠ semantic identity;
   - Facility physical location ≠ RegulatoryJurisdiction;
   - M016 is a bounded primary-substance hook, not complete composition.
4. Every browser query either exposes source-backed provenance from `IdentifierAssignment → SourceRecord → DatasetRelease → Dataset` or explicitly returns `provenance-unavailable` where W6 has no governed lineage path.

## Evidence basis

Canonical inputs are repository-governed artifacts, not UI assumptions:
- `v2/data/mappings/ontology-rdb-mapping.csv` (M009–M016, M021, M031)
- `v2/data/db/schema.sql`
- V2-076 observatory design and task traceability
- V2-077 actor/facility map implementation contract and validated read-only SQL

## Current action-dependency posture

- A0 substantive implementation/design: **materially advanced; executable SQL contract present**.
- A1 hosted reproducibility: **pending**. No browser-specific hosted PASS is claimed in this checkpoint.
- A2: **not identified** for V2-078.

## Remaining Definition-of-Done work

1. Add deterministic fixture rows/expected-result assertions for representative product, organization, facility and at least one T03 traversal.
2. Add a small deterministic validator that rejects semantic/source leakage and unregistered relation exposure.
3. Add a dedicated hosted reproducibility gate and record exact commit/run evidence.
4. Persist the V2-083 handoff only after the fixture/gate evidence exists.
5. Close #147 only when those checks reproduce successfully; do not interpret success as global ecosystem completeness, production deployment, or Gate-G PASS.
