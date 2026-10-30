# Scoped 2.1 progress — planning record 0.3.0

**Target 2.1.0; GA not yet ready.** The approved D-01 / SC-REL / D-03 strategy
continues from [record 0.2.0](../0.2.0/README.md); no repeated owner decision is
needed for the bounded implementation and copied-fixture integration.

**#331 is verified; #332 is next ready.** The exact implementation commit is
`42708dc83599a84d161631ccf6d4960189a54581`. The direct push
[hosted run 40734338360](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40734338360)
passed. Its downloaded artifact ZIP SHA-256 was verified, and all sixteen
normalized evidence fields match the local result. The 26 head-referenced workflow
families also passed, each within its own pinned scope. PR checks used a separately
identified merge commit with the same Git tree; primary profile evidence uses the
direct implementation commit. See the profile's exact CI/execution records.

The [M1 support profile](../../../ontology/profiles/2.1/m1-provenance/0.1.0/README.md)
implements #331 with an isolated 50-triple vocabulary, 143-triple opt-in shape
graph, four direct targetClass shapes and the unchanged query/key contract.
It uses exactly the six selected CM-PharmE terms and imports no whole experimental
ontology. The four-file standalone CLI test needs no copied repository, DB or Java.

The contract, 24 fixture/oracle cases and incoming-axiom dispositions were frozen
at `699bd799c0c0234e9ded1422de83885c9bde24bb` before implementation. Local results:
24/24 admission expectations (8 accepted, 16 expected refusals), five HermiT
expectations, two OWLAPI profile views, two isolation/target guards and four-format
roundtrips passed. A present run is checked; an absent run remains allowed. Extra
metadata remains allowed and local admission does not become universal OWL
cardinality or disjointness.

The raw RDF row payload/query remains unchanged. The strict OWL view explicitly
excludes only rdf:value serialization triples, with counted loss; no lossless
full-RDF-to-OWL or raw-export OWL 2 DL claim is made. See the profile's explanation
and exact formal/query witnesses. The next copied-W6 packet must preserve this
boundary while testing actual exported rows.

| Packet | Issue | Release point |
|---|---|---|
| Exact hosted verification of the isolated profile — done | #331 | Scoped core ready for integration |
| One isolated copied-W6 integration and preservation audit | #332 | Selected 2.1 mapping path verified |
| Minimum support docs/notices/manifest and new bundle/cold replay | #306 child just in time | Reviewed 2.1 GA candidate |
| Exact tested publication and downloaded-byte verification | #306 | Stable 2.1.0 |
| Next completed compatible extension | Retained native/source/domain backlog | Incremental 2.2.0 |

[release-plan.json](release-plan.json) records the current local/hosted state;
[next-steps.csv](next-steps.csv) records bounded sequencing. This implementation
does not change the old M1 verifier/database, full modern native model, scientific
card/oracles, source-profile acceptance (1/4), historical ORSD review (0/83),
expert evidence or published RC. No full-candidate merge or GA follows from this
profile alone. Continue with one active packet and small justified release cuts.

The three-packet release-cut review (#329/#330/#331) is HOLD for #332's copied-W6
integration and the subsequent minimum docs/notices/new-bundle/release checks.
This is an eligibility decision, not a guarantee of three more executions.
