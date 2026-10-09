# G3-3-D — bounded real-source migration

Source: **NHIF Bulgaria Outpatient Pharmacy**, the project's W6 P1 primary DOI anchor, [Zenodo record 19160825](https://zenodo.org/records/19160825), DOI [10.5281/zenodo.19160825](https://doi.org/10.5281/zenodo.19160825). The official record metadata identifies `pharmacy_data_20260322_131416.csv` (1,704,038,344 bytes, MD5 `b43fb62d3d44525de74f930f472d2f03`) with CC BY 4.0 metadata. Credit: Kostadin Kostadinov and coauthors/editors named in the Zenodo record; underlying data are attributed to Bulgaria's NHIF. This project downloaded **five small HTTP byte ranges**, not the full file, so the published full-file MD5 was not locally verified. The project's W6 [source manifest](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/sources/source-manifest.json) expects a different file name; [source-contract-delta.json](source-contract-delta.json) records the fix and acceptance boundary.

## Observed sample and validation

| Measure | Result | Scope |
| --- | ---: | --- |
| Real source records selected | 768 | Five deterministic byte-range prefixes: first 256 and 128 each at four other offsets. Five region codes and five reporting dates spanning 2020–2025; not representative. |
| Required fields | 19/19 observed; 0 empty cells in these rows | Three fields (`costs`, `part`, `currency`) remain in the raw source/provenance layer; package/strength/unit values are descriptive, not formalized domain structures. |
| Preflight admission | 768 accepted, 0 rejected | Required typed values and date/decimal parsing on this sampled slice. |
| Mapped graph | 39,272 triples | 768 SourceRecords, 3,072 separate aggregate metric observations, 264 source-scoped product and 264 presentation nodes. |
| Full candidate pySHACL | 768 rows admitted; 0 graph violations | All G3-C SHACL shapes on the complete mapped sample with `inference='none'`. |
| Controlled negative probes | 5/5 rejected | Missing identifier scheme, missing classification entry, wrong observation product type, geographic self containment, Product-only substance property on a presentation. These were injected into real-row data and are **not actual source defects**. |
| HermiT OWL DL | Full ABox consistent; disjointness counterexample inconsistent | Aligned G3-C OWL TBox plus all 39,272 real-source triples. |

The [sample manifest](source-slice-manifest.json) pins the Zenodo record, requested byte ranges, SHA-256 of every downloaded range and every committed selected slice, and exact selection rule. The five CSV slices are verbatim UTF-8 lines from the official published file. The 39,272-triple full graph is stored as sorted N-Triples encoded in [gzip/Base64](real-source-abox.nt.gz.b64), with hashes in [migration-results.json](migration-results.json); [one real row witness](one-real-row-witness.ttl) is directly readable. Decode with `base64 -d real-source-abox.nt.gz.b64 | gzip -dc > real-source-abox.nt`, then verify its SHA-256 against the result file.

ATC code is represented as classification evidence and `atc_name` as its source label. **No** PharmaceuticalSubstance or `productHasActiveSubstance` fact is inferred from an ATC label alone. `patients_num` remains an aggregate observation, with no patient individuals. NHIF codes are scheme-scoped identifier assignments, and product/presentation URIs are explicitly source-scoped provisional identities. The [W6 field-mapping register](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/mappings/source-field-ontology-mapping.csv) is the interpretation boundary. The sample cannot establish full-dataset completeness, cross-source identity accuracy, or generalization to other regions and periods.

## Reproduction

Python 3.12 dependencies: `rdflib==7.6.0`, `pyshacl==0.30.1`, `owlready2==0.49`, `owlrl==7.6.2`; Java 17 for HermiT. From this directory:

```bash
python migrate_g3d.py source-slice-manifest.json ../2.1.0-alpha.1-g3-3-c-integrated-validation/constraints.ttl .
python validate_g3d_abox.py ../2.1.0-alpha.1-g3-3-c-integrated-validation/active.ttl real-source-abox.nt abox-reasoner-results.json
python build_g3d_report.py . ../2.1.0-alpha.1-g3-3-c-integrated-validation/g3-closure-plan.json
```

To re-fetch the exact ranges from the official URL, use `curl --range START-END` for each range listed in `source-slice-manifest.json`, verify HTTP 206 and the pinned SHA-256 before running `build_g3d_slices.py <range-dir> .`. The script expects the downloaded range files under its documented `cmpe-p1-*` names. A changed remote response is a new snapshot and must not silently overwrite these results.

## Gate and next turn

This completes the **bounded D turn**, not G3-P6 or the ontology release. Full-source ingestion, source contract repair, `SupplyCapacity` bearer, 29 relation decisions, 14 isolate connectors, 10 ImpAbs endpoint questions, 19 RepRel policies and the official full 20-pattern detector remain open. PR #305 stays draft and issue #306 open. G1/G2 closed = **2/5 major stages (40%)**; G3 closed named packages = **2/7 (28.6%)**. Of the five bounded B3–F turns, **3/5 (60%)** are done; E and F remain, plus scientific/detector gates.

**Exact next step G3-3-E:** recompute native and OWL connectivity, compare all 14 isolate proposals with actual source witnesses and OntoUML constraints, and report component/isolate and domain-coverage changes without adding an unsupported edge. G3-3-F then prepares the traceability and human-review handoff.
