"""Build G3-3-D checkpoint from frozen source and executed validation results."""
import json
import sys
from pathlib import Path

out, prior = map(Path,sys.argv[1:3])
source=json.loads((out/'source-slice-manifest.json').read_text())
m=json.loads((out/'migration-results.json').read_text())
r=json.loads((out/'abox-reasoner-results.json').read_text())
plan=json.loads(prior.read_text())
assert source['selected_rows_total']==768
assert m['input']['schema_accepted']==768 and m['input']['preflight_rejected']==0
assert m['full_candidate_pyshacl']['conforms'] and m['full_candidate_pyshacl']['validation_results']==0
assert m['negative_sensitivity']['passed']==5
assert m['mapped']['rdf_triples']==39272 and m['mapped']['reimbursement_metric_observations']==3072
assert r['positive']['pass'] and r['negative']['pass']
assert r['input']['abox_sha256']==m['abox']['sha256']

delta={"source_id":"P1-NHIF-OUTPATIENT",
       "source_manifest_branch":"v2/research-program",
       "zenodo_record":"https://zenodo.org/records/19160825",
       "manifest_file_contract":"nhif_outpatient_pharmacy_combined.csv",
       "published_file_at_pinned_record":"pharmacy_data_20260322_131416.csv",
       "published_size_bytes":source['published_size_bytes'],
       "published_md5_metadata_only_not_downloaded":source['published_md5_from_Zenodo_metadata_unverified_locally'],
       "required_header_matches_19_columns_in_five_real_slices":True,
       "impact":"The source contract's literal filename will not locate the published v3 file even though its sampled schema matches; fixture-only CI did not exercise remote file discovery.",
       "recommended_fix":"Pin record ID and file checksum; update the expected published filename (or explicit alias) in the W6 source adapter and manifest, then test discovery against official Zenodo metadata and the parsed header. Preserve the fixture filename only as a documented local fixture alias.",
       "negative_acceptance":"Do not mark the whole 1.7 GB file ingested, equate schema match with full-data quality, or silently rename the real source to pass a fixture contract.",
       "state":"OPEN_RECONCILIATION"}
(out/'source-contract-delta.json').write_text(json.dumps(delta,indent=2,ensure_ascii=False)+'\n')
plan['as_of']='2026-10-09 Asia/Tehran'
plan['G3_3_D_status']='completed bounded five-stratum real-source sample migration and full graph SHACL/HermiT checks; full dataset and identity review remain open'
plan['next_exact_turn']='G3-3-E: recompute native/OWL class and relation connectivity after B2/C/D; review all 14 isolate proposals against actual source witness and ontology pattern constraints; keep unsupported links absent; report component/isolate deltas and domain coverage.'
plan['remaining_bounded_turns']=['G3-3-E connectivity and isolate evidence','G3-3-F traceability and human review handoff']
plan['G3_package_status']['P6_formal_empirical_validation']='in progress; 768 actual NHIF source rows from five nonrepresentative byte-range strata admitted by full SHACL, 39,272 mapped ABox triples HermiT consistent; full dataset and external validity pending'
(out/'g3-closure-plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
summary={"as_of":"2026-10-09 Asia/Tehran","step":"G3-3-D",
         "source":{"doi":"10.5281/zenodo.19160825","published_filename":source['published_filename'],
                   "sampled_rows":768,"strata":5,"region_codes":[x['selected_region_codes'][0] for x in source['strata']],
                   "periods":[x['selected_periods'][0] for x in source['strata']],
                   "filename_contract_mismatch":True},
         "results":{"required_columns":19,"observed_missing_cells_in_sample":sum(m['input']['missing_cells'].values()),
                    "schema_accepted_rows":768,"preflight_rejected_rows":0,"full_SHACL_admitted_rows":768,
                    "full_SHACL_violations":0,"controlled_negative_rejections":5,
                    "ABox_triples":39272,"aggregate_observation_nodes":3072,
                    "HermiT_full_ABox_consistent":True,"HermiT_injected_disjointness_rejected":True,
                    "product_nodes_source_scoped":264,"presentation_nodes_source_scoped":264,
                    "asserted_patient_individuals":0,"asserted_substance_nodes_from_ambiguous_ATC":0},
         "limits":["Five contiguous byte-range strata, each one region/period; no random or representative sampling claim.",
                   "The full 1.7 GB dataset and its published MD5 were not downloaded or independently verified.",
                   "Three fields remain raw-only; packaging, concentration and units are descriptive strings, not first-class domain structures.",
                   "Source-scoped product and presentation nodes are provisional, not authoritative cross-source identity.",
                   "Official full anti-pattern engine, scientific decisions and SupplyCapacity bearer route remain open."],
         "progress":{"closed_major_stages":2,"total_major_stages":5,"closed_major_stage_percent":40.0,
                     "closed_G3_packages":2,"total_G3_packages":7,"closed_G3_package_percent":28.6,
                     "bounded_B3_to_F_turns_completed":3,"bounded_B3_to_F_turns_total":5,
                     "bounded_B3_to_F_turns_percent":60.0,"remaining_turns":["G3-3-E","G3-3-F"]},
         "release_state":"REVIEW_CANDIDATE_ONLY"}
(out/'g3d-summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
readme="""# G3-3-D — bounded real-source migration

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
"""
(out/'README.md').write_text(readme)
print(json.dumps(summary['results']))
