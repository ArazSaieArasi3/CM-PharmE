# W7-E13 — Reproducibility and Independent Clean Rebuild Audit

## Status
**Mandatory gate: PASS**  
**Family status: PASS WITH WARNING**

Issue: #102  
Protocol/baseline freeze: `v2/evaluation/protocol/e13-reproducibility-baseline.json`  
Final GitHub Actions run: `32566080703` — **SUCCESS**  
Evidence artifact: `9474119730`  
Artifact digest: `sha256:c5de10f0d4277d2c2b3b7bca681f75b56a658742b3c010f9bc06c71c56ebe508`

## Audit result
The W5/W6/W7 computable evidence chain was regenerated on a fresh GitHub-hosted Ubuntu runner using a pinned computational environment and a fresh PostgreSQL/PostGIS service. The final E13 audit reported **54/54 checks PASS**.

The audit intentionally does not synthesize or reconstruct W7-E9 human expert evidence. E9 remains an external empirical evidence family; only its frozen pre-collection protocol package is integrity-checked here.

## Deterministic formal-ontology rebuild
The W5 formal ontology was built twice from repository sources within the clean run.

- pass A canonical ontology SHA-256: `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`
- pass B canonical ontology SHA-256: `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`
- frozen W5 baseline: exact match
- canonical N-Triples: byte-identical across the two builds
- build manifest: byte-identical across the two builds
- inventory reproduced: 642 asserted triples; 87 conceptual elements; 81 OWL classes; 6 datatypes; 52 object properties; 5 datatype properties
- SHACL build checks and eight protected Gate-D distinctions remained intact.

## Logical rebuild
ROBOT `1.9.10` was downloaded and verified against the frozen SHA-256 before use. OWL 2 DL profile validation and both HermiT and JFact were rerun.

- OWL 2 DL gate: PASS
- named unsatisfiable CM-PharmE classes: 0 in both reasoners
- named subclass pairs: 91 in HermiT and 91 in JFact
- named subclass hierarchy agreement: exact

The previously documented JFact handling of six project-native conceptual datatypes was reproduced. It remains a bounded datatype-compatibility warning and does not invalidate the named-class logical result.

## Fresh data-infrastructure rebuild
A new PostgreSQL/PostGIS database was initialized and populated from the schema-faithful W6 fixtures.

The deterministic RDF/KG export was then executed twice:

- pass A canonical KG SHA-256: `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`
- pass B canonical KG SHA-256: `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`
- frozen W6 baseline: exact match
- graph size: 398 triples
- canonical N-Triples: byte-identical
- KG manifest: byte-identical

W6 validation and the four frozen SQL↔SPARQL benchmark pairs were regenerated successfully: **4/4 PASS**.

## W7 computable evidence regenerated
The clean run successfully regenerated the executable evidence for:

- E1 structural quality;
- E2 OWL-profile and multi-reasoner evaluation;
- E3 project-native UFO/OntoUML pattern evaluation;
- E4 positive/negative competency questions;
- E5 SHACL/data conformance and controlled mutations;
- E6 dataset-to-ontology mapping quality;
- E7 concept/relation coverage;
- E8 held-out generalizability reports from the frozen first-pass registries;
- E10 ontology↔RDB↔KG semantic consistency;
- E11 analytics/AI evidence-sufficiency gate;
- E12 controlled resilience scenarios.

The regenerated results retained the same bounded warnings and negative findings rather than normalizing them away.

## Captured environment
The workflow captured the execution environment and dependency manifest. Salient runtime values were:

- GitHub hosted runner: Ubuntu 24.04.4 LTS (`ubuntu-24.04` image)
- Python: 3.12.14
- Java: Temurin 21.0.12+8
- PostgreSQL: 16.4 in `postgis/postgis:16-3.4`
- ROBOT: 1.9.10, checksum verified
- `psycopg[binary]`: 3.2.9
- `rdflib`: 7.5.0
- `pyshacl`: 0.31.0
- `PyYAML`: 6.0.2

The Actions log also records the exact resolved SHAs for the versioned GitHub Actions used at runtime and the pulled PostGIS image digest. These records make the specific successful execution auditable even though the workflow source currently names version tags rather than immutable action/container digests.

## Artifact completeness
The E13 Actions artifact contains the clean environment capture, dependency freeze, ROBOT/version evidence, both formal builds, both KG exports, regenerated W6 reports, regenerated W7 computational evaluation reports, and the E13 machine-readable audit. The uploaded artifact is retained under ID `9474119730` with digest `sha256:c5de10f0d4277d2c2b3b7bca681f75b56a658742b3c010f9bc06c71c56ebe508`.

## Interpretation boundary
E13 supports **repository-level computational reproducibility under a fresh, captured GitHub-hosted environment**. It does not establish independent replication by a separate research team, and it does not reproduce human expert evidence. The data-infrastructure portion also remains bounded to the W6 schema-faithful reference realization rather than full external-dataset empirical replication.

The family is therefore reported as **PASS WITH WARNING**, not as unrestricted external reproducibility.
