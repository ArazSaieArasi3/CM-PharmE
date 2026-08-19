# CM-PharmE 2.0 — W7 Prospective Evaluation Protocol

**Protocol status:** FROZEN BEFORE W7 RESULT INTERPRETATION  
**Baseline:** Gate-E-approved merge `59417e352c68585effc3056440fd1a815f6b92bc`  
**Protocol issue:** #89  
**Gate:** Gate F (#104)

## 1. Purpose
Evaluate CM-PharmE 2.0 prospectively across independent evidence families. The protocol separates formal correctness, conceptual quality, data fit, generalizability, expert judgment, cross-representation fidelity, application evidence and reproducibility. No single aggregate quality score is used because success in one family cannot substitute for failure in another.

## 2. Research-integrity rules
1. Metrics and interpretation rules are defined before W7 results are interpreted.
2. W5/W6 frozen artifacts are the evaluation target unless an explicitly logged post-test adaptation is being studied.
3. Fixture, admitted real-data and held-out results are reported separately.
4. H1–H3 remain protected until W7-E8 (V2-070). Their use must be logged before inspection of their evaluation results.
5. Any ontology change prompted by held-out evidence is recorded as post-test adaptation and is not counted as initial held-out performance.
6. Negative or null findings are retained.
7. A PASS is scoped only to the metric and dataset/run that produced it.
8. Formal consistency does not imply semantic truth, domain completeness, standards conformance, empirical effectiveness or adoption.
9. Expert results are prospective only; missing participant variables are not retrospectively inferred.
10. Application/AI/resilience results are claims only where a predefined task, dataset, baseline and metric exist.

## 3. Evaluation families

### W7-E1 — Syntactic, structural and ontology quality — issue #90
**Target:** authoritative ontology source, generated serializations, conceptual registry and traceability artifacts.  
**Measures:** parse success; graph-isomorphism/regression status; duplicate/undefined internal terms; namespace hygiene; structural counts; annotation completeness descriptors; registered traceability resolution; protected-distinction integrity.  
**Mandatory gate conditions:** all authoritative/generated serializations parse; deterministic graph fingerprint matches the frozen baseline where no intended ontology change exists; zero unresolved internal CM-PharmE terms in registered artifacts; all protected distinctions remain present.  
**Interpretation:** annotation/structural indicators are descriptive; they are not a completeness score.

### W7-E2 — Logical and profile evaluation — issue #91
**Target:** asserted OWL and reasoned views.  
**Measures:** OWL 2 DL profile; consistency; unsatisfiable named classes; inferred hierarchy sanity; agreement between at least two applicable reasoner engines where technically feasible; reasoner versions and runtime/exit status.  
**Mandatory gate conditions:** selected OWL profile passes; no inconsistency; no unintended unsatisfiable named class. Reasoner disagreement is a WARN/FAIL requiring investigation, not majority voting.  
**Reasoner target:** HermiT plus a second applicable OWL reasoner available in the pinned toolchain (target JFact; substitute must be documented).

### W7-E3 — UFO/OntoUML pattern and anti-pattern evaluation — issue #92
**Target:** Gate-D conceptual model and W5 formal projection.  
**Measures:** stereotype/pattern consistency; Relator mediation; Kind/Role/Phase discipline; event/result distinction; Mode/Quality distinction; Organization/Facility; Geography/RegulatoryJurisdiction; Product/Substance/Presentation; ObservationActivity/ObservationResult; SupplyCapacity/evidence separation; documented exceptions.  
**Mandatory gate conditions:** no unresolved critical anti-pattern affecting a principal claim; all eight protected Gate-D distinctions remain explicit.  
**Boundary:** official OntoUML-tool conformance is claimed only if such a tool is actually executed and evidenced.

### W7-E4 — Positive and negative competency questions — issue #93
**Target:** ontology and evaluation KG(s).  
**Measures:** predefined positive-CQ expected-result agreement; predefined negative-CQ expected rejection/absence/constraint outcome; ontology-term traceability; query reproducibility.  
**Mandatory gate conditions:** all mandatory CQs must match their frozen expected outcomes. Exploratory CQs are reported separately and do not silently become mandatory after execution.

### W7-E5 — SHACL and data conformance — issue #94
**Target:** W6 fixture plus admitted real and held-out instance graphs when available.  
**Measures:** conforms flag; violation/warning counts by shape and severity; provenance completeness; identifier/geography/observation constraint coverage; sampled review of violations.  
**Mandatory gate conditions:** controlled regression fixture must conform. Real/held-out datasets are not required to have zero violations; violations are empirical findings. Principal claims requiring a constrained field fail or are qualified if critical unresolved violations affect that field.

### W7-E6 — Dataset-to-ontology mapping quality — issue #95
**Target:** admitted source contracts, mapping registries and populated data.  
**Measures:** every in-scope field classified as direct, bounded/derived, ambiguous, unmapped or out-of-scope; mapped-field proportion; critical-field coverage; semantic-loss cases; provenance-link completeness; manual audit sample.  
**Mandatory gate conditions:** 100% of in-scope fields receive an explicit mapping-status classification; no critical field used by a principal claim remains silently unmapped. Numeric coverage is reported descriptively per source; no universal arbitrary threshold is used.

### W7-E7 — Concept and relation coverage — issue #96
**Target:** admitted evaluation source families and V1/V2 comparison sets.  
**Measures:** represented/partial/not-represented concept coverage; relation coverage; Core/X-INFRA/Extension coverage; incremental coverage by source; unsupported ontology terms; source concepts without representation; V1→V2 comparative delta where evidence is comparable.  
**Mandatory gate conditions:** denominators and extraction basis are explicit; critical gaps are enumerated. Coverage percentages are evidence, not proof of global domain completeness.

### W7-E8 — Held-out and cross-jurisdiction generalizability — issue #97
**Protected targets:** H1 ClinicalTrials.gov/AACT; H2 openFDA Drug Shortages; H3 reserved national essential-medicines sample, subject to W2 access/licensing registry.  
**Measures:** first-pass mapping success; unseen-concept rate; unseen-relation rate; required-extension count; held-out CQ success; jurisdiction-specific mismatch taxonomy; post-test adaptation delta.  
**Mandatory gate conditions:** initial results are captured before any model adaptation; held-out contamination log remains clean; adaptations are reported separately. Generalizability claims are bounded to evaluated held-out sources.

### W7-E9 — Prospective structured expert evaluation — issue #98
**Target:** CM-PharmE 2.0 conceptual/formal artifacts and selected representative tasks.  
**Instrument dimensions:** clarity; semantic adequacy; domain relevance; missing concepts/relations; inappropriate distinctions; task usefulness; confidence/uncertainty; open comments.  
**Participant target:** minimum evidence target 5 qualified participants spanning at least two relevant expertise profiles; preferred target 8–12 if feasible. Smaller or less diverse participation is reported as a limitation rather than compensated statistically.  
**Analysis:** primarily descriptive/ordinal; item distributions, medians/IQR where appropriate, disagreement and qualitative themes.  
**Mandatory gate conditions:** instrument, eligibility, collection procedure, anonymization/consent and aggregation rules are fixed before responses are collected. No participant background variable is reconstructed if it was not collected.

### W7-E10 — Ontology↔RDB↔KG semantic consistency — issue #99
**Target:** W5 ontology, W6 PostgreSQL/PostGIS schema, mapping registry, generated ABox and query benchmarks.  
**Measures:** registered mapping resolution; key identity/cardinality/distinction preservation; unknown ontology-term count; one-to-many metric projection correctness; SQL↔SPARQL result equivalence; round-trip spot checks; semantic-loss exceptions.  
**Mandatory gate conditions:** zero unknown CM-PharmE terms; all registered mandatory mappings resolve; all mandatory paired SQL↔SPARQL benchmarks agree after canonical normalization. Claims remain bounded to registered mappings/benchmarks.

### W7-E11 — Selected analytics/AI demonstrators — issue #100
**Eligibility rule:** a task is evaluable only if it has a predefined hypothesis, dataset, baseline, metric and reproducible implementation.  
**Measures:** task-specific baseline delta; error analysis; provenance visibility; ontology-dependent contribution; computational cost where relevant.  
**Mandatory gate conditions:** no benchmark means no AI/analytics novelty claim. A non-improving result is retained and may support a negative finding or deferral.

### W7-E12 — Pharmaceutical resilience scenarios — issue #101
**Target:** critical-medicine vulnerability/resilience representation scenarios.  
**Measures:** scenario representability; required concepts/relations; CQ/query outcome; provenance coverage; evidence-gap taxonomy; sensitivity to missing supply/procurement evidence.  
**Mandatory gate conditions:** assumptions and evidence sources are explicit. Scenario representability does not become a predictive-effectiveness claim without outcome validation.

### W7-E13 — Reproducibility and independent rebuild audit — issue #102
**Target:** W5/W6/W7 code, data fixtures/contracts and generated evidence.  
**Measures:** clean environment bootstrap; pinned dependency capture; ontology rebuild; database bootstrap; KG regeneration; evaluation-report regeneration; deterministic fingerprints/checksums; CI/local or independent-run agreement.  
**Mandatory gate conditions:** all artifacts declared deterministic reproduce byte-identically or with an explicitly justified canonical equivalence; any non-determinism is documented.

## 4. Evidence classes
Each result is tagged with one of:
- `fixture-regression`
- `admitted-real-data`
- `held-out`
- `expert`
- `formal/computational`
- `application-demonstrator`

These tags must not be collapsed in reporting.

## 5. Result states
Each registered check receives one of:
- `PASS` — predefined criterion satisfied within scope;
- `WARN` — result usable but limitation materially affects interpretation;
- `FAIL` — predefined criterion not satisfied;
- `DEFERRED` — evidence/task prerequisites unavailable or intentionally future-facing;
- `NOT_APPLICABLE` — metric does not apply to that artifact/source.

## 6. Claim sufficiency rule for Gate F
Gate F is claim-based, not wave-score-based. A principal claim can be:
- `SUPPORTED` — all mandatory evidence families for that claim pass and limitations do not contradict it;
- `SUPPORTED_WITH_BOUNDARY` — evidence passes but the claim must be narrowed to evaluated scope;
- `DEFERRED` — evidence is insufficient but no contradiction is established;
- `REJECTED/REFORMULATE` — evidence contradicts or fails the proposed claim.

A failed exploratory AI task, for example, does not automatically fail the ontology paper if AI is not a principal claim. Conversely, formal consistency cannot rescue a failed generalizability claim.

## 7. Held-out contamination log rule
Before W7-E8 starts, the evidence register must record:
- exact held-out source identifier/version/access date;
- confirmation that its evaluation payload was not used to alter the frozen baseline before first-pass scoring;
- first-pass artifact hash;
- any subsequent adaptation as a separate phase.

## 8. Data and licensing rule
Only data that satisfy the W2 admission/access/licensing rules may be downloaded, redistributed or committed. Where redistribution is restricted, scripts/manifests/checksums and derived aggregate evidence are preferred over raw redistribution.

## 9. Expert-evaluation ethics boundary
The expert study must collect only what the approved instrument requires, keep identifiers out of the public repository unless explicitly consented, and record whether institutional ethics review/waiver is required under the applicable institutional policy before recruitment. W7 does not invent or infer participant attributes.

## 10. Protocol amendments and implementation corrections
Any change to scientific evaluation criteria after the first W7 result is produced must be logged as a protocol amendment with date, reason, affected metrics and whether the change was made before or after seeing the affected result. Original criteria remain available for audit.

**Implementation correction log — W7-E2:** the first E2 harness execution expected ROBOT to emit an unsatisfiable-class dump file even when the unsatisfiable set was empty. Both reasoners completed, but the comparison harness failed on the absent empty dump. The harness was corrected to interpret absent/empty dump files as empty sets and to retain reasoner log findings. No protocol criterion, threshold or interpretation rule was changed.

## 11. Gate F minimum decision package
Gate F should receive:
1. this frozen protocol and amendments/correction log;
2. evaluation matrix with status/artifact links;
3. claim-evidence gate table;
4. per-family machine-readable reports;
5. held-out contamination/adaptation log;
6. expert-evaluation report if completed;
7. reproducibility audit;
8. explicit list of supported, bounded, deferred and rejected manuscript claims.
