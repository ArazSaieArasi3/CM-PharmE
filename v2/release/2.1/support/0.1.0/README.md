# CM-PharmE 2.1.0 — M1 Provenance Core support contract

This is the minimum support contract for #333. **Stable 2.1.0 has not yet been
published.** Archive construction, cold replay and exact publication verification
are separate subsequent packets. The release is a small provenance core, not a
replacement for the entire pharmaceutical ecosystem model.

| Version | Meaning |
|---|---|
| 2.1.0 | Target distribution version |
| 0.1.0 | Frozen standalone M1 profile version |
| 1.0.0 | Historical main/root citation baseline, unchanged |

## Supported entrypoints

- `v2/ontology/profiles/2.1/m1-provenance/0.1.0/profile.py admit export.ttl`: opt-in SHACL, nonempty focus and local
  public/composite-key admission against profile.ttl and shapes.ttl.
- `v2/ontology/profiles/2.1/m1-provenance/0.1.0/query.rq`: unchanged Q21-01 over the complete raw RDF payload.
- `v2/ontology/profiles/2.1/m1-provenance/0.1.0/verify_profile.py`: 24 frozen synthetic admission expectations,
  five HermiT cases, bounded OWLAPI/Pellet views and serialization/portability checks.
- `v2/data/integrations/2.1/m1-core/0.1.0/verify_integration.py`: the declared M001–M004 path on the explicit
  disposable copied-W6 database only. The guarded preflight precedes fixture reset.

The vocabulary has four classes (Dataset, DatasetRelease, SourceRecord,
ProvenanceActivity) and two object properties (hasDatasetRelease,
containsSourceRecord). There is no whole-model import or equivalence bridge.
SHACL/key completeness is an opt-in export profile, not universal OWL cardinality.
Generating activity is optional. Extra metadata is allowed. Row numbers are
integers and hashes are opaque nonempty strings; no invented global semantics.

## Exact scope and evidence

[manifest.json](manifest.json) enumerates included files, SHA-256, role and rights.
[claims.json](claims.json) links supported behavior to its bounded evidence.
[dependency-review.json](dependency-review.json) records the 60-file computational
closure and dynamic/subprocess dependencies. [excluded-files.csv](excluded-files.csv)
lists the other files in source snapshot `b9c1c26edb756fdc741cba8bb56f5c0e88feb45d`: no implicit inclusion or support.
New files outside this manifest also remain excluded by default.

Full P3 active.ttl is a six-definition derivation input only. P3 constraints.ttl,
old scope.json and core inventory.json are pinned reference inputs. They are
included for reproducibility and never admitted as the supported whole TBox.
Historical verify_m1.py is imported for pure helpers; its main is unsupported.
Frozen W5 modules are compatibility references only, with no 2.0/2.1 equivalence.
Original reference documents describe their own historical scope and next steps;
this contract supplies the current support boundary.

Raw RDF retains rdf:value row triples for queries and admission. The strict OWL
view explicitly omits only those triples and counts the loss; it is not a lossless
conversion or proof that the full raw export is OWL 2 DL.

The integration evidence covers seven synthetic records, two independently
bootstrapped databases, baseline and optional-run cases, seven golden Q21-01
tuples, four legacy query pairs, 24 preserved base tables and 22 unchanged default
2.0 IRIs. It does not cover real-source ingestion or the other 32 mappings.
Historical source-policy acceptance is 1/4; historical ORSD acceptance is 0/83;
no new external expert responses exist. Full native detector, domain, research,
expert, application and broader ORSD obligations remain open.

Read [REPRODUCE.md](REPRODUCE.md), [NOTICE.md](NOTICE.md),
[CHANGELOG.md](CHANGELOG.md), [MIGRATION.md](MIGRATION.md), and
[CITATION.cff](CITATION.cff). The historical root CITATION.cff remains unchanged.
