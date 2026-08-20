# W7-E6 — Dataset-to-Ontology Mapping Quality

## Status
**Mandatory gate: PASS**  
**Evidence-family interpretation: PASS WITH WARNING**  
**Issue:** #95 / V2-068  
**Final GitHub Actions run:** `32337590134` — SUCCESS  
**Evidence artifact:** `cm-pharme-v2-w7-e6-mapping-evidence` / ID `9395173816`  
**Artifact digest:** `sha256:a8991c240a6a12cde98f3c6aa600b6446778894660ef5ddf2c449b4f95fd0d41`

## 1. Evaluation target
W7-E6 evaluates the field-level mapping quality of the two source contracts whose schemas were already frozen and implemented by the Gate-E reference adapters:

- `P1-NHIF-OUTPATIENT` — 19 required fields;
- `P2-NHIF-INPATIENT` — 20 required fields.

The evaluation is performed against:

- `v2/data/sources/source-manifest.json`;
- `v2/data/mappings/source-field-ontology-mapping.csv`;
- `v2/data/mappings/ontology-rdb-mapping.csv`;
- `v2/data/mappings/source-mapping-coverage.csv`;
- the frozen W5 asserted ontology rebuilt in CI;
- the frozen W7-E6 rule set in `v2/evaluation/protocol/e6-mapping-quality-rules.json`.

No held-out source is used in E6.

## 2. Mapping documentation architecture
The repository now maintains mapping evidence as a layered traceability architecture rather than a single ad-hoc crosswalk:

1. **Source contract layer** — source role, DOI/access/licensing boundary, unit of observation, required columns, adapter status.
2. **Source-field semantic layer** — exact source field, semantic interpretation, ontology target, mapping status, transformation rule, provenance rule, semantic-loss classification and rationale.
3. **Ontology↔RDB realization layer** — formal ontology element to relational table/field/join realization.
4. **RDB↔KG projection layer** — explicit RDF projection or an explicit `RDB-only`/bounded statement where the current ABox does not yet materialize the semantics.

The mapping-directory `README.md` is the human-readable governance specification for these artifacts and defines the controlled mapping-status vocabulary and change-control process.

## 3. Mandatory results

### Overall
- field decisions evaluated: **39**;
- in-scope fields: **38**;
- direct/derived/bounded mapped: **36/38 = 94.74%**;
- explicitly ambiguous: **2**;
- explicitly unmapped: **0**;
- out-of-scope source fields retained explicitly: **1**;
- critical fields: **28**;
- critical unmapped: **0**;
- critical ambiguous: **0**;
- provenance rule documented: **39/39**;
- frozen author-side semantic audit sample: **12/12 PASS**;
- held-out H1–H3 used: **false**.

### Mapping-status distribution
Across the 39 evaluated field decisions:

| Status | Count |
|---|---:|
| Direct | 6 |
| Derived | 14 |
| Bounded | 16 |
| Ambiguous | 2 |
| Unmapped | 0 |
| Out of scope | 1 |

The 28 principal-claim-critical fields comprise **6 direct + 14 derived + 8 bounded** decisions. None is ambiguous or unmapped.

### Semantic-loss descriptors
The registry records semantic loss/coarsening explicitly rather than hiding it:

- `none`: **13** decisions;
- `low`: **8** decisions;
- `medium`: **18** decisions;
- `high`: **0** decisions.

These descriptors are not a score; they document where the current representation is exact, normalized, or intentionally coarser.

## 4. Per-source results

### P1 — NHIF Outpatient
- frozen required fields classified: **19/19**;
- in-scope fields: **18**;
- direct/derived/bounded mapped: **17/18 = 94.44%**;
- ambiguous: **1 (`atc_name`)**;
- unmapped: **0**;
- status distribution: 2 direct, 7 derived, 8 bounded, 1 ambiguous, 1 out-of-scope.

### P2 — NHIF Inpatient
- frozen required fields classified: **20/20**;
- in-scope fields: **20**;
- direct/derived/bounded mapped: **19/20 = 95.00%**;
- ambiguous: **1 (`atc_name`)**;
- unmapped: **0**;
- status distribution: 4 direct, 7 derived, 8 bounded, 1 ambiguous.

## 5. Principal findings

### 5.1 ATC code and ATC name require different claims
`atc_code` has a direct classification interpretation through `ProductClassificationScheme`, `ClassificationEntry`, and `ProductClassificationAssignment`.

`atc_name`, however, is explicitly **ambiguous** beyond its classification-label role. The current adapter also uses it as a provisional source-label input for substance normalization, but the mapping registry prohibits treating this as independently validated active-substance identity. This ambiguity is retained as evidence rather than being normalized away to improve the coverage percentage.

### 5.2 Product-presentation details are represented but partly RDB-only
`packaging`, `concentration`, and `num_in_pack` contribute to deterministic presentation identity and are retained in PostgreSQL. The current W6 RDF ABox does not yet project their full formal semantics as explicit packaging/Strength/PackageConfiguration structures; therefore these mappings are correctly classified as **bounded**.

### 5.3 Diagnosis semantics are not silently discarded
ICD code/label fields are retained through `DiagnosisClassificationReference` and the relational observation link, but the current ABox does not yet materialize that relation. The mapping registry therefore exposes this as a bounded projection rather than reporting false semantic equivalence.

### 5.4 Aggregate measures remain aggregate
`patients_num`, `pack_num`, and normalized monetary measures are deterministically projected into metric-specific `ReimbursementUtilisationObservationResult` nodes. `patients_num` never creates Patient individuals.

### 5.5 Original monetary evidence remains auditable
Original `costs` and `currency` values remain in the relational evidence layer, while normalized BGN/EUR values are projected as explicit metric observations. This is documented as bounded rather than claiming that all monetary semantics are currently represented by a dedicated currency model.

### 5.6 Source-only partition semantics are explicit
The outpatient `part` field is classified `out_of_scope` for ontology-domain claims but retained in the source fingerprint/raw-key and relational record. This is an intentional reproducibility decision, not a dropped column.

## 6. Professional mapping-quality controls
The CI evaluator verified:

- exact equality between the two frozen source contracts and their field-level mapping decisions;
- no duplicate mapping decision for a source field;
- controlled mapping-status vocabulary;
- no critical field silently unmapped;
- required semantic interpretation, RDB target, provenance rule and rationale;
- resolution of every referenced `cmpe:` ontology term against the rebuilt frozen ontology;
- source-coverage-index consistency;
- the frozen 12-decision author-side manual semantic audit sample.

The final job completed successfully with no mandatory failure.

## 7. Sources not quantified in E6
The following authoritative sources remain visible in `source-mapping-coverage.csv` but are **not assigned invented field-level percentages**:

- `P3-FDA-ACTORS` — contract-only;
- `P4-OPENFDA-PRODUCT` — contract-only;
- `P5-EMA-CRITICAL-SHORTAGE` — contract-only.

Their field schemas must first be version-frozen before a professional quantitative mapping audit is valid.

`P7-GEONAMES` is recorded separately as a geography-normalization source and is not included in the pharmaceutical field-mapping denominator.

## 8. Interpretation
The mandatory E6 gate passes because every field in the two evaluated frozen source contracts has an explicit mapping decision, no critical field is unmapped/ambiguous, ontology targets resolve, provenance is documented, and the audit sample passes.

The family remains **PASS WITH WARNING** because:

1. two `atc_name` decisions remain explicitly ambiguous for substance interpretation;
2. 16 in-scope field decisions are bounded/partial by design;
3. field-level quantitative mapping has not yet been performed for the contract-only FDA/openFDA/EMA sources.

These warnings are evidence-quality boundaries, not reasons to rewrite the source semantics or inflate coverage.

## 9. Manuscript-safe claim
The manuscript may state that **all 39 fields across the two frozen NHIF source contracts were explicitly classified, with 36/38 in-scope fields having direct, derived, or bounded ontology mappings (94.74%), zero in-scope fields left unmapped, and no critical field left ambiguous or unmapped; all mapping decisions included provenance documentation and a frozen 12-case author-side semantic audit passed.**

The manuscript must also state that this result is limited to the two evaluated field-level source contracts and does not establish global pharmaceutical-domain completeness or field-level coverage of the contract-only authoritative sources.
