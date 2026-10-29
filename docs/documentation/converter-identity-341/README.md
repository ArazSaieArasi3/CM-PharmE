# Converter identity repair — #341

The retained converter content checksum is unchanged. Exact-source rebuilds
failed because unversioned Maven default plugins resolved differently from the
successful historical build. Java and upstream source were the same.

Historical hosted run36679317918 (job109771090387, commit
`a60512cfe9a9045a583dde57dbdc02672030a986`) used resources3.4.0 and jar3.5.0.
The failed build used resources3.5.0 and jar3.5.1. Two current default builds were
entry-for-entry identical but had the wrong historical digest. A second pair
using the historical plugin versions reproduced the established
`f500951cdd4a0963fb80a96b974f463e8cfc84660f3b46ce802b14296e5e9aee`
content identity exactly. Only `META-INF/MANIFEST.MF` differs between default and
pinned builds; no class, dependency or other resource entry differs.

## Evidence and bounded implementation

[Forensic run40953972950](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40953972950)
at `6f904d9a5fd3c7d8cbccdfddaac48028b5f5f4c5`, job123729134047,
records four clean builds, per-entry digests, Maven artifact/POM checksums,
effective POM, dependency tree, Java/Maven versions and all twelve conversions.
`report.json` retains its summary. The attached artifact retains complete JARs,
entry manifests and logs. `prior-receipt.json` pins the historical comparison.
The prior frontend artifact is not misrepresented as a retained converter JAR.

`prepare_converter_build.py` checks the exact upstream Git commit and original
POM bytes, then creates a derived build-only POM adding the two explicit plugin
versions. Original POM/source files are preserved. The generated file hash
matches the forensic overlay. Both WebVOWL and full-site workflows invoke it
and keep their original content checksum assertions and delimiter convention.
No entry exclusions, new checksum, converter upgrade or published bytes change.

The four builds produce byte-identical JSON for each governed input. V1 remains
44 classes/42 properties with its historical JSON hash; full V2 remains102/110
with its historical JSON hash. The M1 projection is7/5, hash
`515b9327fd5a5ab52d3ed3d6890fbebdde9fa5624ea38e17df413bd32c55144a`.
These are converter projection counts, not domain-signature counts. M1 generated
reference/explorer flags remain disabled until #338; diagnostic conversion does
not itself satisfy entity coverage or publication/live-browser QA under #339.

Date:2026-10-30 (Asia/Tehran). This repairs documentation tooling for existing
semantic2.1.0, without a semantic release bump or broader scientific acceptance.
Original helper/diagnostic code is MIT; original explanatory content is CC BY4.0
under approved D-03, retaining project attribution and upstream terms.

## Integrated acceptance

Implementation `454317d94263efc06c8fa304cffd1b38ffdfcaa6` passes all eleven
applicable PR workflows (plus the duplicate push onboarding run). Forensic
run40954565675 also passes with the original-POM hash guard and explicit restored
identity assertions. [Full assembly run40954904319](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40954904319)
passes converter/frontend checks, closed-loop navigation, downloads, future
onboarding isolation and deployment preflight. Its synthetic PR merge tree equals
the implementation tree. `ci-evidence.json` records exact jobs/artifacts and old
subtree digests; public deploy and browser verification jobs are skipped.

The integrated proof exposed a pre-existing full-model assumption in the future
onboarding test. Reference aliases are now restored only when reference generation
is enabled, as in the common production pipeline. All prior subtree digest
assertions remain enforced, including the disabled M1 reference placeholder.
No profile feature is prematurely enabled to satisfy the test.

#341 is complete. #338 is the sole next ready packet; PR #340 remains a draft
source/tooling candidate until M1 generated content and #339 publication gates
are fulfilled. Historical #337 receipts remain observations at their own commits.
