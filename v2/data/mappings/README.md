# CM-PharmE 2.0 Mapping Architecture

## Purpose
This directory is the authoritative mapping documentation layer between admitted source schemas, the CM-PharmE 2.0 ontology, the PostgreSQL/PostGIS reference representation, and the RDF knowledge-graph projection.

The mapping layer is intentionally explicit. A source column is never treated as an ontology class or property merely because it exists in a dataset. Each field is interpreted semantically, assigned a mapping status, linked to implementation targets, and given a provenance and semantic-loss note.

## Mapping artifacts

| Artifact | Role |
|---|---|
| `source-field-ontology-mapping.csv` | Field-level Source → Ontology → RDB → KG registry for source contracts with frozen field schemas. |
| `ontology-rdb-mapping.csv` | Ontology → relational representation registry for classes, properties, Relators, qualities, and deferred elements. |
| `source-mapping-coverage.csv` | Source-by-source inventory showing which source contracts have field-level mappings and which remain contract-only/deferred. |
| `../sources/source-manifest.json` | Authoritative source-role, DOI/licensing, unit-of-observation, required-column, adapter, and execution-boundary manifest. |

These artifacts are complementary. `source-field-ontology-mapping.csv` answers *what does a source field mean and how is it represented?*; `ontology-rdb-mapping.csv` answers *how is a CM-PharmE semantic element realized relationally?*

## Field-level mapping schema

Each row in `source-field-ontology-mapping.csv` records:

- `mapping_id` — stable mapping decision identifier;
- `source_id` and `source_role` — source contract and research role;
- `source_field` — exact field name from the frozen source contract;
- `in_scope` — whether the field contributes to ontology/data claims;
- `mapping_status` — semantic mapping classification defined below;
- `critical_for_principal_claim` — whether an unresolved mapping could affect a principal manuscript claim;
- `semantic_interpretation` — source-grounded meaning used by CM-PharmE;
- `ontology_targets` — CM-PharmE/external semantic targets;
- `rdb_targets` — canonical relational realization;
- `kg_projection` — current RDF/ABox realization or an explicit statement that the value remains relational only;
- `transformation_rule` — deterministic derivation/normalization rule;
- `provenance_rule` — how the mapped value remains traceable to Dataset/Release/SourceRecord/transformation evidence;
- `semantic_loss` — `none`, `low`, `medium`, or `high` descriptive risk of information loss/coarsening;
- `rationale` — why the mapping was chosen and what must not be inferred;
- `manual_audit` — status of the author-side semantic review of that mapping decision.

## Mapping-status taxonomy

The registry uses a controlled vocabulary:

- **`direct`** — the source field has an explicit, semantically compatible ontology representation without substantive reinterpretation.
- **`derived`** — the ontology representation is produced by a documented deterministic transform, normalization, grouping, or metric projection.
- **`bounded`** — the source meaning is retained only at a coarser or partial semantic granularity, or is represented relationally while the RDF/Ontology projection remains incomplete.
- **`ambiguous`** — the source field can support more than one plausible semantic interpretation and evidence is insufficient to make a stronger commitment.
- **`unmapped`** — the field is in scope but no current semantic mapping exists. Such rows must remain visible and cannot be silently dropped.
- **`out_of_scope`** — the field is retained for source fidelity/reproducibility but is intentionally excluded from ontology-domain claims.

No percentage threshold converts an ambiguous or unmapped field into a pass. The research-integrity rule is that every in-scope field receives an explicit status and no field used by a principal claim remains silently unmapped.

## Current evaluated field-level scope

W7-E6 quantitatively evaluates the two frozen NHIF schemas already implemented by the Gate-E adapters:

- `P1-NHIF-OUTPATIENT` — 19 required fields;
- `P2-NHIF-INPATIENT` — 20 required fields.

The authoritative FDA/openFDA/EMA contracts remain explicitly **contract-only** at this point because a versioned field-level schema snapshot has not yet been frozen in the repository. They are listed in `source-mapping-coverage.csv` as deferred rather than being assigned invented coverage percentages.

GeoNames is treated as a normalization source, not as pharmaceutical-domain evidence, and therefore is not mixed into the pharmaceutical field-mapping denominator.

## Important semantic decisions captured by the registry

### Aggregate counts are not persons
`patients_num` maps to an aggregate `ReimbursementUtilisationObservationResult` with a numeric measure. No `Patient` individual is fabricated.

### Identifiers are assignments, not identities
`nhif_code` and `hospital_code` are represented under explicit identifier schemes and attached to presentation/facility entities through `IdentifierAssignment`.

### Geography and jurisdiction are distinct
NHIF region codes/names resolve to `AdministrativeRegion`; they are not treated as `RegulatoryJurisdiction`.

### Product, substance, and presentation remain distinct
`market_name`, `nhif_code`, packaging, concentration, and pack-size fields participate in different identity/representation layers. They are not collapsed into a single Drug entity.

### ATC labels have a bounded substance interpretation
`atc_code` directly supports product classification. `atc_name` is retained as a classification label, while its current use as a provisional source label for substance normalization is explicitly classified as **ambiguous**. It must not be reported as independently validated active-substance identity.

### RDB-only representation is visible
Several values—such as detailed packaging/strength/package count structure, diagnosis-reference links, original cost/currency fields—are retained in PostgreSQL but are not yet fully projected into the W6 RDF ABox. The registry marks these as `bounded` rather than hiding the semantic-loss boundary.

## Provenance and auditability

Every evaluated source row is represented as a `SourceRecord` with a deterministic content fingerprint. Mapping decisions document whether the derived canonical entity/observation/identifier/assertion remains traceable through:

`Dataset → DatasetRelease → SourceRecord → Transformation/Assertion/EvidenceSupport → canonical representation`.

The field registry complements, rather than replaces, execution-level provenance checks in W6/W7.

## Quality evaluation

W7-E6 validates the mapping registry mechanically and reports:

1. source-contract coverage;
2. explicit status coverage for every required field;
3. direct/derived/bounded/ambiguous/unmapped/out-of-scope counts;
4. mapped-field proportion by source, with denominators stated;
5. critical-field status;
6. semantic-loss distribution;
7. ontology-target syntax/resolution checks where applicable;
8. RDB target documentation completeness;
9. provenance-rule documentation completeness;
10. a frozen author-side manual audit sample spanning direct, derived, bounded, ambiguous, and out-of-scope decisions.

The result is evidence about **mapping quality for the evaluated source contracts**, not proof of global ontology completeness.

## Change-control rule

A mapping decision that changes after W7 result inspection must be logged as a post-test mapping amendment. The original row must remain recoverable in version history, and manuscript claims must use the evidence state that corresponds to the reported ontology/data release.

When a new source is admitted, the expected workflow is:

1. freeze source version/schema and licensing/access metadata;
2. add/update the source in `source-manifest.json`;
3. add the source to `source-mapping-coverage.csv`;
4. classify every in-scope field in `source-field-ontology-mapping.csv`;
5. document ontology, RDB, KG, transform, provenance, and semantic-loss decisions;
6. run the mapping-quality evaluator/CI;
7. only then use the source for manuscript coverage or generalizability claims.

## Claim boundary

A high field-mapping percentage does **not** prove domain completeness, standards conformance, or empirical correctness. Conversely, an explicit ambiguous/bounded mapping is not automatically a defect: it is an auditable statement that the source semantics do not justify a stronger ontological commitment.
