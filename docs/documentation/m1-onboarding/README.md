# Released M1 documentation onboarding — #337

This is a documentation-only candidate from main control plane
`d185ba2751a77658db9e282f13367362068d07d0`. The separately released profile is
registered as **v2-m1**, under family v2, without replacing the full evolving V2
entry. Registry schema1.1 adds the explicit released_profile type and vN-profile
identifier; previous1.0 model records remain valid and unchanged.

The source is the curated release commit
`77a8e854d0e3927b0687346d7f8fda6a398adda7`, not a mutable research branch.
`m1-profile-release.json` pins seven exact source files, profile0.1.0,
distribution2.1.0 and canonical graph fingerprint
`7b7cff97eedc071a6c1f15d71f58eadb2a9a1d3bcdfc7f38b14a920b70707186`.

## Build and reader handoff

The existing common pipeline can check out this source and execute
`build_released_profile.py` from the publication control plane. The builder
requires the exact Git commit and all source-file hashes, retains the 50-triple
TBox and signature, checks two original admission witnesses and emits five
graph-isomorphic serializations. It does not invoke a full source model or
claim a new formal reasoner run. Local materialized-input mode is explicitly
test-only and is refused by the production documentation-input resolver.

The signature has four CM-PharmE classes and two CM-PharmE object properties.
Total declarations include three object properties and two datatype properties
because external vocabulary is retained. These totals are not WebVOWL projection
counts. Canonical bytes, serialization bytes and release-archive bytes have
different fingerprints and are kept distinct.

Wiki source adds a profile explanation and updates the release index/navigation.
Pages uses `ontology/2.1.0/m1/`, the pinned citation, release package, support map,
source TTL and corrected profile-specific evolution links. Formal-reference and
WebVOWL flags remain false until #338 supplies validated adapters and coverage.
Their candidate shell pages state that preparation is in progress. No production
route or new documentation baseline is claimed by this packet; publication and
rendered cross-surface checks remain #339.

## Verification and preservation

The real-profile onboarding test checks both schemas/common plan, unchanged
V1/V2 registry/build/download records, previous shell subtrees, five equivalent
serializations, independent builds under different Python hash seeds, source
identity, reader links and nine negative controls. The source-only local test
does not claim a Git checkout; the hosted test requires the actual release
checkout and the production resolver to pass. `baseline/` retains exact pre-change
contracts for regression, not a new semantic authority or a public archive.

The previous synthetic V3 tests now select their explicit V2 model fixture
instead of assuming the last registry entry is a full model. They remain
temporary architecture tests and publish no fictional scientific version.

Original new helper/test/workflow code is MIT and original explanatory changes
are CC BY 4.0 under approved D-03. Preserve Araz Saie Arasi and CM-PharmE contributor
attribution and existing upstream notices. No repository-wide grant or historical
release modification is made. Existing full-model/native/source/ORSD/expert
obligations remain outside the released M1 documentation cut.
