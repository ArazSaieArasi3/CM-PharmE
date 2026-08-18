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

## Dataset registry status
No dataset is admitted at W0. W2 will score and admit DOI-backed and authoritative sources using explicit criteria. Candidate names discussed before W2 remain candidates only until license, accessibility, schema, provenance, and research fit are verified.
