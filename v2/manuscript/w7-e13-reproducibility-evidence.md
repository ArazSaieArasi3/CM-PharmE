# W7-E13 Manuscript Evidence Note — Reproducibility

## Evidence available
A clean GitHub-hosted CI environment rebuilt the CM-PharmE 2.0 computational evidence chain from repository sources. The final E13 run (`32566080703`) completed successfully and the audit reported **54/54 checks PASS**. Evidence artifact: `9474119730`, digest `sha256:c5de10f0d4277d2c2b3b7bca681f75b56a658742b3c010f9bc06c71c56ebe508`.

The formal ontology was rebuilt twice and reproduced the frozen W5 canonical SHA-256 `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`; the canonical N-Triples and manifests were byte-identical. A fresh PostgreSQL/PostGIS realization was then bootstrapped, and two independent KG exports reproduced the frozen W6 canonical SHA-256 `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825` with byte-identical canonical N-Triples and manifests.

The run also regenerated W6 validation/SQL↔SPARQL evidence and the executable W7 E1–E8 and E10–E12 evidence families. E9 expert evidence was deliberately excluded from automated regeneration; only the integrity of the prospectively frozen expert protocol is within the E13 reproducibility boundary.

## Safe manuscript claim
A defensible formulation is:

> The repository's computational ontology, data-infrastructure, and evaluation evidence was regenerated successfully in a fresh, version-captured CI environment. Repeated ontology and reference-KG builds reproduced their frozen canonical fingerprints, while the executable W7 evaluation families reproduced their registered outcomes.

## Required qualification
Do not describe E13 as independent external replication. The evidence demonstrates **repository-level computational reproducibility on a fresh GitHub-hosted environment**, not replication by an unaffiliated research team. Human expert evidence is not computationally reproducible and remains a separate prospective empirical evaluation family. The W6 data rebuild uses the schema-faithful reference realization and therefore does not constitute a full re-ingestion of every external source.

## Environment note
The successful run captured Ubuntu/Python/Java/PostgreSQL/PostGIS/package versions, verified ROBOT 1.9.10 by SHA-256, and retained runtime-resolved action SHAs and the PostGIS image digest in the Actions log. The workflow source still uses versioned tags for some infrastructure references; this is an explicitly bounded reproducibility dependency rather than an unstated guarantee of immutable infrastructure.
