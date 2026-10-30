# Release and documentation route — planning record0.10.0

Stable semantic **2.1.0 — M1 Provenance Core** remains published and unchanged.
#337 completed released-profile source/content onboarding. #341 restores the
established converter checksum through explicit historical Maven plugin pins;
no checksum replacement, new converter version or semantic change is made.

Four clean converter builds show that current unpinned default plugins change
only META-INF/MANIFEST.MF. With resources3.4.0 and jar3.5.0 (successful historical
run36679317918), two clean builds reproduce the original f500951c... content
identity exactly. All four builds produce byte-identical V1, fullV2 and M1 VOWL
JSON. Actual M1 projection counts are7classes/5properties, distinct from its
four domain classes/two domain object properties. Those diagnostic projections
alone do not complete #338 entity coverage or #339 public browser verification.

Implementation: docs/m1-release-337@9650f91cfcd52abaca4cab40007b9e29a4b70aba,
draft PR #340. Verified integrated implementation is
454317d94263efc06c8fa304cffd1b38ffdfcaa6; recording head is
165796e80c57b6cbc7dba27b46d380587828c17e. Converter forensic run40953972950 retains complete JARs, per-entry
hashes, dependency/POM hashes and twelve conversions. Full integration evidence
is retained in docs/documentation/converter-identity-341/ci-evidence.json on the
documentation branch. Main and release2.1.0 are not changed or merged here.

| Order | Issue | State | Outcome |
|---|---|---|---|
| Done | #337 | Source preparation complete | Explicit released M1 entry, Wiki/Pages source and five downloads |
| Done | #341 | Converter identity repaired | Original checksum and old projections retained |
| Next | #338 | Sole next ready packet | Enable/audit M1 formal reference and static explorer |
| Then | #339 | After #338 | Publish Wiki/Pages/WebVOWL, verify actual browser routes, record baseline |
| Independent | #315 | Pending | Actual WholeOver and other scientific dispositions |

The M1 reference/explorer flags remain false. No public M1 route, new public
baseline or rendered-QA result is claimed. This documentation route needs no
semantic2.2.0 release. Existing public archives PB-2026.09.1/WB-2026.09.1 and
older roadmap bytes remain retained. Source-policy acceptance1/4, historical
ORSD0/83, WholeOver author disposition pending and zero new expert responses
remain unchanged. Full-model/native/module and #244 editorial/excellence gates
retain their own closure rules. Date:2026-10-30, Asia/Tehran.
