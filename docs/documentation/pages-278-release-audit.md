# PB-2026.09.1 — accepted Pages documentation baseline

Decision: **PASS / DECLARED**, 2026-09-30. Tracks #278; completes Epic #267.

This is a Pages/documentation baseline. V2 remains evolving and no V2 semantic
release or research-completion claim is created.

- Published build commit: `f41da9a633c69196676306fddd79e4408a3ac07d`.
- Pages build/deploy/public browser verification: run `36679626350`, SUCCESS.
- Published Wiki commit: `9d6cbcb2fb53a61009062834422d02097080c00b`; all 266 ready Wiki URLs verified.
- Cross-surface reader journeys: 16 surfaces, zero broken links, correct exact refs.
- Local links/assets: 3,406 checked, zero broken; WebVOWL application hash routes are explicitly recorded.
- WIDOCO coverage: all 42 V1 input classes / 41 object properties represented (including infrastructure; 39 canonical concepts / 40 canonical relations); all 81 V2 classes / 52 object properties / 5 datatype properties represented. Zero missing entities.
- Ten advertised serializations are checksum/provenance/graph-equivalence bound.
- Wiki disposition: 171 pages assessed; unique content and inbound routes retained.
- Synthetic future-version onboarding: schema/selector/flags/negative guards PASS;
  V1/V2 prior subtrees byte-identical. No fictional V3 published.
- Public exposure review and mandatory deployment preflight: PASS.
- Deterministic archive: 180 files, rebuilt twice with identical bytes and read-back verified.
- Archive SHA-256: `b01b3cf3b22e1a2c6297f04309252c3e5eb321c829c9b86c67d801bea23788a7`.

## Durable evidence

- [Full release/audit record](baselines/PB-2026.09.1.json)
- [Exact published site and evidence archive](baselines/PB-2026.09.1.zip)

The record separates the published build ref, exact semantic V1/V2 refs, published
Wiki ref and the later recording commit. It includes generator/tool metadata,
registry hash, route inventory, entity coverage, download checksums, workflow/artifact
IDs and digests, exposure audit, isolation proof and known limitations.

## Archive reproduction

The ZIP stores `site/`, `evidence/`, `source/`, `RELEASE-INPUT.json` and
`BASELINE-MANIFEST.json`. Extract it; restore `source/` as the source repository
working tree with the archived `site/` and `evidence/` as inputs. Run the bundled
`tools/pages/archive_pages_baseline.py` under Python 3.12 with rdflib 7.5.0 against
those frozen inputs. Fixed ZIP timestamps/order/permissions and SHA-256 inventories
make the archived bytes reproducible and independently checkable. Browser screenshots
are frozen evidence; fresh interactive-layout screenshots are not claimed deterministic.

No open portal child issues remain after recording and closing #278. Broader ontology
review, expert evaluation and manuscript tasks continue in their own research issues.
