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

## Initial methodological lineage
| Source | Role | V2 relevance |
|---|---|---|
| UFO foundational ontology literature | Methodological | Identity, rigidity, dependence, relators, events, modes, roles. |
| OntoUML methodology and tooling | Methodological | First-class conceptual modeling and anti-pattern/semantic evaluation. |
| CM-PharmE conference paper | Prior work | Formal predecessor and V1 architectural baseline. |
| CM-PharmE journal revision | Prior work | Stronger methodological/evaluation baseline and explicit limitation set. |
| CM4DI conference work | Methodological lineage only | Reusable experience in UFO/OntoUML, modularity, CQs, and repository-supported evaluation; not pharmaceutical-domain evidence. |

## W1 evidence
W1 application/methodological evidence is registered at `v2/research/w1/evidence-sources.md` and supports stakeholder-need and use-case discovery. It is not automatically empirical V2 dataset evidence.

## W2 dataset/source evidence
Detailed W2 records are maintained in:
- `v2/research/w2/dataset-landscape.md`
- `v2/research/w2/doi-dataset-registry.md`
- `v2/research/w2/operational-source-registry.md`
- `v2/research/w2/domain-source-profiles.md`
- `v2/research/w2/dataset-admission-rubric.md`
- `v2/research/w2/dataset-scorecard.md`
- `v2/research/w2/gate-c-dataset-portfolio.md`

### Proposed primary DOI anchors
- **10.5281/zenodo.19160825** — NHIF Bulgaria outpatient pharmacy reimbursement.
- **10.5281/zenodo.19160637** — NHIF Bulgaria inpatient antineoplastic/coagulopathy medicines.

### Proposed conditional DOI evidence
- **10.5281/zenodo.18851842** — operational pharmaceutical supply dataset; high semantic value but raw redistribution remains conditional because a standard open-data license was not verified.

### Proposed operational discovery/implementation families
FDA DECRS/WDD3PL, openFDA NDC/SPL, EMA critical-medicine/shortage sources, WHO essential-medicine resources and GeoNames enrichment.

### Protected held-out families
- **ClinicalTrials.gov / AACT** for organization/site/location/intervention and relational generalizability.
- **openFDA Drug Shortages** for U.S. cross-jurisdiction shortage evaluation after EU-derived shortage/criticality discovery.
- selected WHO national EMLs only after per-list audit.

## Gate discipline
No source receives its final W3/W6/W7 role until Gate C approval. Once Gate C is approved, held-out source roles are frozen before W3 concept discovery. Any later use of a held-out schema to admit Core concepts must be recorded and will invalidate clean held-out status for the affected concepts.
