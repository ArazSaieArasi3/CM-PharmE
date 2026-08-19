# CM-PharmE 2.0 Evidence and Citation Registry

## Purpose
Provide a single traceable registry for literature, datasets, standards, operational sources, methodological references, and application evidence used in CM-PharmE 2.0.

## Admission fields
Every admitted source should record:
- stable identifier (DOI, accession, release, URL, or standard identifier);
- source type;
- publisher/maintainer;
- publication/release date;
- license or reuse terms;
- downloadability/access mode;
- schema/data dictionary availability;
- geography/jurisdiction;
- temporal coverage;
- domain coverage;
- intended research role;
- concepts/relations potentially informed;
- claims supported;
- limitations and known biases;
- discovery/admission/held-out status.

## Source roles
- **Discovery evidence** — may inform concept/relation discovery.
- **Implementation evidence** — used in ETL, instance data, mappings, or KG/RDB realization.
- **Evaluation evidence** — used for validation, held-out testing, or external comparison.
- **Held-out evidence** — deliberately excluded from Core concept admission and reserved for external/generalizability tests.
- **Enrichment evidence** — provides identifiers, terminology or geography without defining Core domain semantics.
- **Methodological evidence** — supports ontology-engineering and evaluation procedures.
- **Application evidence** — supports concrete ecosystem needs/use cases.

## Methodological lineage
| Source | Role | V2 relevance |
|---|---|---|
| UFO foundational ontology literature | Methodological | Identity, rigidity, dependence, relators, events, modes and roles. |
| OntoUML specification and methodology | Methodological | Sortal/non-sortal distinctions, Role/RoleMixin, Relator/Mediation/Material patterns, modes/qualities, part-whole semantics and anti-pattern review. |
| CM-PharmE conference paper | Prior work | Formal predecessor and V1 architectural baseline. |
| CM-PharmE journal revision | Prior work | Stronger methodological/evaluation baseline and explicit limitation set. |
| CM4DI conference work | Methodological lineage only | Reusable experience in UFO/OntoUML, modularity, CQs and repository-supported evaluation; not pharmaceutical-domain evidence. |
| Oliveira et al. 2022, ROSE, DOI `10.1007/978-3-031-17995-2_26` | Methodological / extension alignment | UFO-grounded risk-treatment reference used to define a future alignment boundary for the modular Risk & Resilience extension; W4 does not import or reproduce its axioms. |

## W1 application evidence
W1 evidence is registered at `v2/research/w1/evidence-sources.md`. It supports stakeholder-need, use-case, geospatial, resilience, risk-alignment, application and opportunity discovery. It is not automatically empirical V2 dataset evidence.

## W2 approved source portfolio — Gate C approved 2026-08-19
Detailed W2 records:
- `v2/research/w2/dataset-landscape.md`
- `v2/research/w2/doi-dataset-registry.md`
- `v2/research/w2/operational-source-registry.md`
- `v2/research/w2/domain-source-profiles.md`
- `v2/research/w2/dataset-admission-rubric.md`
- `v2/research/w2/dataset-scorecard.md`
- `v2/research/w2/gate-c-dataset-portfolio.md`

### Primary DOI empirical anchors
- **P1 — 10.5281/zenodo.19160825** — NHIF Bulgaria outpatient pharmacy reimbursement.
- **P2 — 10.5281/zenodo.19160637** — NHIF Bulgaria inpatient antineoplastic/coagulopathy medicines.

### Primary operational/reference discovery families
- **P3** — FDA DECRS + WDD/3PL.
- **P4** — openFDA NDC + FDA/openFDA SPL.
- **P5** — EMA Union List of Critical Medicines + EMA medicine-shortage JSON / reporting evidence.
- **P6** — WHO Model List/eEML.
- **P7** — GeoNames, normalization only.

### Conditional evidence
- **C1 — 10.5281/zenodo.18851842** — operational pharmaceutical supply dataset; high semantic value for inventory/procurement/lead-time/stockout discovery, but raw redistribution remains prohibited in the public research package unless reuse terms are clarified.
- **C2 — EMA EudraGMDP** — public semantic/schema evidence permitted; automated ingestion remains conditional on compliant bulk/API access verification.

### Secondary/enrichment
- **S1** ChEMBL 37 — substance/identifier enrichment.
- **S2** NHIF Individually Approved Medicines — DOI `10.5281/zenodo.15680002`.
- **S3** openFDA FAERS — optional Safety/Pharmacovigilance extension only.

### Protected held-out
- **H1 ClinicalTrials.gov / AACT** — organization/site/location/intervention and relational generalizability.
- **H2 openFDA Drug Shortages** — U.S. shortage cross-jurisdiction test.
- **H3 selected WHO national EMLs** — later jurisdiction-sensitive essentiality test after per-list audit.

## W3 concept/relation evidence artifacts
- `v2/research/w3/source-schema-concept-extraction.md`
- `v2/research/w3/candidate-concept-inventory.md`
- `v2/research/w3/candidate-relations-events.md`
- `v2/research/w3/geospatial-temporal-jurisdiction.md`
- `v2/research/w3/provenance-evidence-observation.md`
- `v2/research/w3/identifiers-entity-resolution.md`
- `v2/research/w3/v1-v2-migration-matrix.md`
- `v2/research/w3/evidence-traceability.md`
- `v2/research/w3/concept-admission-protocol.md`
- `v2/research/w3/gate-concept-inventory.md`

## W3 evidence result
W3 normalized **80 pre-UFO concept candidates** and **80 candidate relationship semantics** from approved discovery sources and V1 lineage:
- 29 CORE candidates;
- 23 cross-cutting infrastructure candidates;
- 26 extension candidates;
- 2 deferred candidates.

The evidence-backed semantic backbone was Organization/Role → Site/Facility → Regulatory/Jurisdiction context → Medicinal Product/Substance/Presentation → Geography/Time → Shortage/Availability/Demand/Supply observations → Evidence/Provenance/Identifier infrastructure.

## W4 methodological and conceptual evidence
W4 applies the approved W3 inventory to a UFO/OntoUML conceptualization before OWL formalization. Its methodological basis is recorded in `v2/research/w4/README.md` and the detailed design artifacts below:
- `v2/research/w4/architecture.md`
- `v2/research/w4/stereotype-decision-matrix.md`
- `v2/research/w4/relator-material-patterns.md`
- `v2/research/w4/events-situations-observations.md`
- `v2/research/w4/geography-jurisdiction.md`
- `v2/research/w4/risk-resilience-extension.md`
- `v2/research/w4/business-architecture-view.md`
- `v2/research/w4/integrated-ontouml-model.md`
- `v2/research/w4/integrated-ontouml-overview.puml`
- `v2/research/w4/anti-pattern-review.md`
- `v2/research/w4/w3-w4-transformation-ledger.md`
- `v2/research/w4/gate-d-conceptual-freeze.md`
- `v2/research/w4/W4-CLOSURE.md`

### W4 conceptual result — Gate D candidate
The integrated W4 specification contains **87 named conceptual types/pattern elements**:
- **32 Core**;
- **25 X-INFRA**;
- **30 modular extensions**.

The increase from W3's 80 candidates comes from documented foundational splits and truth-makers rather than new uncontrolled source discovery. Examples include Observation Activity vs Observation Result; Classification Scheme/Entry/Assignment; Facility Operation; Evidence Support; Supply Capacity vs its observation result; and Risk Treatment Plan vs Risk Treatment Activity.

### W4 review result
The manual/static semantic review against OntoUML rules and anti-pattern categories is **PASS with bounded residual issues**. It is explicitly not an automated OntoUML-tool execution. Machine-readable OntoUML serialization, OWL/SHACL encoding and computational validation remain subsequent implementation/evaluation work.

## Held-out integrity after W4
H1/H2/H3 were not used to add or redesign Core concepts in W4. W4 operates on the Gate-approved W3 inventory and methodological sources. If a later wave mines a held-out schema before W7, held-out status must be revised explicitly.

## Persistent boundaries
- No complete global product-level supplier→buyer→shipment network claim is supported by the current source landscape.
- Finance/counterparty semantics remain outside Core.
- C1 detailed supply semantics remain conditional.
- EudraGMDP automated ingestion remains conditional.
- W4 conceptual commitments are **Gate-D candidates** until user approval.
- W5 formal OWL/SHACL implementation and later W7 computational/generalizability evaluation remain pending.
