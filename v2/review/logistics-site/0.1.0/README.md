# Logistics/site decision card and fixed boundary evidence

Date: 2026-10-30, Asia/Tehran. Preparation packet #345; technical candidate
integration is separately sequenced as #347. This packet does not promote a model.

The [decision card](decision-card.json) recommends **option B**: retain the generic
logisticsFacility association and propose three separately named optional
subproperties for documented origin, destination and storage participation.
Unspecified site function remains generic. The same site may have multiple
explicit functions, and an activity may involve multiple sites. No unsupported
global existence, uniqueness, disjointness or exactly-one constraint is added.

The minimal benefit is that a physical receiving/storage site is no longer
confused with the consignee organization, a legal designation or a guessed route.
The cost is three property/mapping declarations. A separately identified
event-site-function-time participation object is deferred until a required query
needs its identity, repeated visits or per-leg temporal structure. DistributionSiteRole
and FacilityOperation remain distinct from actual event/site participation.

The primary [European Commission 2013 GDP text](https://health.ec.europa.eu/system/files/2016-11/2013_c343_01_en_0.pdf)
was freshly inspected at sections 3.1–3.2, 5.8 and 9.2. The
[source record](sources.json) contains short paraphrases and printed/PDF locators.
Direct EUR-Lex endpoints presented a JavaScript challenge; the official EC PDF
provides the same identified 14-page text. Source wording motivates distinctions;
it does not prescribe these ontology properties, global multiplicities or a
current legal-compliance conclusion. The proposed model interpretation is explicit.

Six [candidate requirement refinements](requirements.json) are traced separately
from the unchanged 83 historical ORSD rows. All actual scientific/source-policy
dispositions remain as recorded; a successful probe is not author acceptance.

## Frozen evidence

[fixed-oracles.json](fixed-oracles.json), sources, requirements and the card were
committed at **653534b5c431ca19b53333ff40a0258bcddbd99e**, before verify.py existed.
[freeze.json](freeze.json) pins their bytes and the existing native assembly,
49-relation crosswalk and later EvidenceRecord candidate. The original model and
oracles are unchanged. Hosted CI independently checks those files at that commit
and the absence of the probe implementation there.

The 19 synthetic witnesses cover dispatch/receipt/storage, unspecified function,
organization versus facility, planned/unknown occurrence, registration/permit
without an event, missing provenance, bad function, identity/alias collapse,
multiple sites/functions and equal labels with distinct identities. They are
synthetic boundary cases, not new operational data or evidence of universal GDP
conformance. All 19 expectations pass. Five RDFS entailment/non-entailment probes
confirm specific-to-generic projection, no guessed function from the generic link,
and no event/site participation invented from registration alone.

[admission.ttl](admission.ttl) applies only to an opted-in source-claim profile.
Its exactly-one fields describe one claim, not a globally exactly-one origin,
destination or site for every activity. Projected statements stay in source-qualified
candidate graphs; the default world graph remains empty. Source support does not
become an assertion of verified world truth. The [proposed OWL properties](proposed-properties.ttl)
are isolated declarations and subproperty relations. RDFS probe success does not
claim OWL2DL/HermiT, native Event/Situation semantics or full-model validation.

Reproduce with the pinned hosted dependencies (rdflib7.5.0, pyshacl0.31.0,
owlrl7.1.4):

```bash
python v2/review/logistics-site/0.1.0/verify.py \
  --output build/logistics-site-decision --check-committed
```

[report.json](report.json) and [boundary-results.csv](boundary-results.csv) expose
each expected/observed result. Local execution versions and hosted execution
identities are recorded separately in [ci-evidence.json](ci-evidence.json); both
hosted archives were downloaded, digest-verified and compared against the local
report/CSV bytes. Push and PR-merge trees match. All 35 executions across 33
workflow families pass on implementation 2ae2f63e0fbf2109ec32ecd21ef41ee69601c048.
No identical-runtime claim is made. Source-policy acceptance remains1/4, historical ORSD author acceptance0/83,
WholeOver author disposition pending and new expert results zero.

This is the concrete decision/evidence handoff for one bounded implementation.
Actual scientific disposition, other 48 proposed relations, full native/formal
alignment and complete-model release/publication gates remain open. The separate
[Pages replacement policy](../../../release/2.2/pages-cutover/0.1.0/README.md)
implements Araz's future publication direction; no old public model is deleted
by this preparation packet.

## Completed preparation and next packet

#345 is complete as decision/evidence preparation. The recommended option B is
reviewable; actual scientific author disposition remains pending. #347 is the
sole READY technical review increment. It may implement the provisional pattern
without promoting it to an accepted whole-model ontology. The comprehensive 2.2
release and authorized Pages replacement remain blocked by their own full-model
gates.
