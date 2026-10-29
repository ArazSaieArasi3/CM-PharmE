# Release and documentation route — planning record 0.9.0

Stable **2.1.0 — M1 Provenance Core** remains published. #337 completes the
source/content onboarding handoff on a separate main-based documentation branch,
[PR #340](https://github.com/ArazSaieArasi3/CM-PharmE/pull/340), at
`87d199da1a6afebaf58c9f238c17b1d67b55bcac`. Main, the curated release and broad
PR #305 are unmerged/unchanged by this packet. This planning update neither
publishes a new semantic version nor claims a new public documentation baseline.

## Verified preparation

The registry adds `v2-m1` as an explicit released profile, retaining the stable
V1 and evolving full V2 records. The common pipeline binds source
`77a8e854d0e3927b0687346d7f8fda6a398adda7`, profile0.1.0 and distribution2.1.0.
The 50-triple TBox has four CM-PharmE classes and two CM-PharmE object properties;
its total declarations include three object and two datatype properties.

Two independent hash-seed builds, five isomorphic serializations, nine negative
controls, production resolver with exact release checkout, unchanged old shell
subtrees, registry/build/download records and Wiki source/navigation checks pass.
The common download workflow checks all 15 serialization downloads. Wiki profile,
release index, Home and sidebar and the scoped Pages shell are prepared.
[Exact evidence and retained local/hosted reports](https://github.com/ArazSaieArasi3/CM-PharmE/blob/87d199da1a6afebaf58c9f238c17b1d67b55bcac/docs/documentation/m1-onboarding/ci-evidence.json)
distinguish verified source preparation from an unready publication candidate.

## Concrete next gate

The existing OWL2VOWL converter rebuild does not match its established content
checksum. Both complete WebVOWL and deployment-candidate workflows stop at that
guard. The root cause is unproven; a framing probe also failed and was reverted.
The expected pin is retained. PR #340 remains draft and cannot be merged/deployed
as an all-green publication candidate. #341 is a small diagnostic prerequisite
within #338; do not replace the pin merely with a newly observed digest.

| Order | Work | Issue | State |
|---|---|---|---|
| Done | Exact released-profile source/content registration | #337 | Preparation handoff verified; no public deploy |
| Next | Resolve converter identity mismatch | #341 | Sole next ready diagnostic packet |
| Then | Generate and audit M1 reference and WebVOWL | #338 | After #341; flags remain disabled |
| Then | Coordinated Wiki/Pages/WebVOWL publication | #339 | After candidate gates and live browser QA |
| Independent | WholeOver scientific dispositions | #315 | Pending; unrelated to M1 documentation eligibility |

Published 2.1.0 already supplies the stable semantic source needed for this route;
no wait for2.2.0 is required. Current public archived baselines remain
PB-2026.09.1 / WB-2026.09.1. WholeOver disposition stays pending, source-policy
acceptance1/4, historical ORSD0/83 and new expert responses0. Broader #244
editorial/excellence and full-model/native/module gates retain their own closure
rules. No fixed publication date is promised while converter/candidate/live-QA
gates remain outstanding. Older planning/evidence records remain immutable.
