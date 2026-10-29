# Released M1 generated documentation candidate — #338

This packet generates the formal reference and static explorer for released M1
profile0.1.0 in distribution2.1.0. The exact 50-triple TBox is pinned at
77a8e854d0e3927b0687346d7f8fda6a398adda7; raw ABox exports and the evolving full
V2 model do not substitute for it. The common pipeline handles all three entries.

## Coverage and reproducibility

WIDOCO1.4.25 renders four CM-PharmE classes and two CM-PharmE object properties.
Its namespace-scoped main sections omit three external declarations: PROV
wasGeneratedBy, DC identifier and PROV value. The adapter generates a separate
introduction table from their exact local input triples. It explicitly describes
profile declarations, not complete upstream vocabulary definitions. No imported
axioms or source changes are introduced. The full coverage gate still requires
all4classes/3object-properties/2datatype-properties, without exclusions.

WIDOCO provenance is configured with the exact owl:versionIRI already in the
released TBox. Otherwise its fallback inserts the output folder into provenance
HTML; the diagnostic diff exposed only that path difference. Two independent
complete reference trees must compare byte-for-byte. This semantic IRI is kept
distinct from the Pages documentation route.

OWL2VOWL0.3.7 retains its original content checksum; WebVOWL1.1.7 retains its
exact frontend checksum. M1 projects7classes/5properties, JSON SHA256
515b9327fd5a5ab52d3ed3d6890fbebdde9fa5624ea38e17df413bd32c55144a. All formal
class/property IRIs must appear; helper class IRIs are recorded separately.
These projection totals do not redefine the domain signature. The selector is
locked to one dataset and bundled samples are removed. WebVOWL is neither the
complete logical specification nor an OntoUML diagram. Raw RDF, opt-in admission
and the strict logical view retain their distinct purposes.

## Verification and publication boundary

Full assembly checks exact input hashes, common configuration guards, formal
coverage, links/assets, citation/download navigation, independent regeneration,
projection hashes and unchanged prior V1/full-V2 subtree receipts. The existing
WebVOWL workflow now uses common stages for every enabled registry entry.
Pinned Playwright/Chromium serves the assembled site over local HTTP and checks
actual graph load, search, zoom, browser/console/network errors and screenshots
for all three explorers. ci-evidence.json retains actual results and identities.
Local candidate QA does not claim public availability or Wiki synchronization.

#339 owns coordinated public publication, actual public-browser QA and a new
documentation baseline. Main, stable semantic2.1.0 payloads and historical public
baseline bytes remain unchanged. No semantic bump, native/full-model acceptance
or expert evidence is implied. Source-policy acceptance stays1/4, historical
ORSD0/83 and WholeOver author disposition pending. Original code is MIT and
original explanation CC BY4.0 under D-03; project/upstream attribution is retained.
Date:2026-10-30, Asia/Tehran.

## Preserving prior V2 download bytes

A strict comparison against the prior assembled artifact exposed six differing
paths, confined to RDF/XML and JSON-LD serializations and their checksum/manifest
and rendered download list. The old pinned V2 builder serializes unsorted graphs
for these formats. Canonical NT/TTL and all reference/explorer files are unchanged.
The guard retrieves immutable artifact12934165079 from run40954904319, verifies
its whole V2 subtree hash against the retained receipt, checks unchanged source
ref/fingerprint/metadata, verifies every old/new checksum and reparses all ten
serializations against the freshly rebuilt governed TBox. Rendered HTML may
differ only in those verified checksum strings. Only the observed six paths can
be retained from the archive; unexpected differences fail. The final complete
V1/V2 subtree hashes must equal the prior receipt. No scientific/source change or
arbitrary file difference is hidden by this preservation step. Original public
baseline archives remain untouched; actual public publication QA belongs to #339.

## Executed acceptance

Implementation75574a84d498b071d42c9eda4a3c3575df95335c passes all twelve distinct
PR workflows plus the duplicate push onboarding run. Integrated run40961606116,
job123755580644, passes all assembly and preflight checks. The PR execution merge
tree equals the implementation tree. Both22-file M1 reference regenerations are
byte-identical. All four classes and five formal object/datatype properties are
covered. V1 and fullV2 final subtree hashes equal the prior retained receipt.
Local Chromium renders all three explorers, with successful search/zoom and zero
browser/console/network errors; M1 renders7nodes. Screenshot names retain the
existing verifier's public-* prefix, but their actual URLs and scope are local.
Public deployment and public-browser jobs are skipped. ci-evidence.json binds
exact reports/artifacts and the tested implementation, separately from this
receipt-recording commit. #338 is complete; #339 is the sole next ready packet.
