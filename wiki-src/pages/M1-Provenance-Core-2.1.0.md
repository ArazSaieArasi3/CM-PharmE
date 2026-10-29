# M1 Provenance Core — release 2.1.0

> **Version scope:** Released 2.1.0 M1 profile 0.1.0  
> **Status:** Stable source release; documentation candidate  
> **Updated:** 2026-10-29

## Purpose and supported use

This profile keeps the origin of a record visible as information moves from a
dataset release into a knowledge graph. A record remains tied to its owning
release and public identity; the activity that generated it may also be recorded.
The resulting chain helps a reader trace a query answer back to its declared
source without inferring that the source has been independently verified.

The released vocabulary contains Dataset, DatasetRelease, SourceRecord and
ProvenanceActivity, linked by hasDatasetRelease and containsSourceRecord. The
TBox has 50 triples. It also declares the external vocabulary needed by the
export, including PROV and identifier/value properties. Its four CM-PharmE
classes and two CM-PharmE object properties should be distinguished from the
total property counts used by reference and visualization tools.

## Use the release

- [Published package, checksums and provenance](https://github.com/ArazSaieArasi3/CM-PharmE/releases/tag/2.1.0)
- [Canonical profile at the exact release commit](https://github.com/ArazSaieArasi3/CM-PharmE/blob/77a8e854d0e3927b0687346d7f8fda6a398adda7/source/v2/ontology/profiles/2.1/m1-provenance/0.1.0/profile.ttl)
- [Release-specific citation](https://github.com/ArazSaieArasi3/CM-PharmE/blob/77a8e854d0e3927b0687346d7f8fda6a398adda7/CITATION.cff)
- [Exact supported files, hashes and rights](https://github.com/ArazSaieArasi3/CM-PharmE/blob/77a8e854d0e3927b0687346d7f8fda6a398adda7/source/v2/release/2.1/support/0.1.0/manifest.json)

The complete package includes admission code, shapes, synthetic witnesses and
reproduction instructions. The planned Pages route is `ontology/2.1.0/m1/`;
this documentation candidate does not yet assert that its new public route is live.
Formal reference and WebVOWL generation follow in #338, with coordinated public
verification in #339. WebVOWL is an exploration projection of the TBox, not an
OntoUML diagram or a complete statement of the logical semantics.

Candidate routes for that publication (not yet verified as live):

- [Formal reference — preparation pending #338](https://arazsaiearasi3.github.io/CM-PharmE/ontology/2.1.0/m1/reference/)
- [WebVOWL — preparation pending #338](https://arazsaiearasi3.github.io/CM-PharmE/ontology/2.1.0/m1/explore/)

## Admission, identity and logical view

Admission is opt-in for this export contract. SHACL and local key checks verify
explicit fields, nonempty scope and record identities; they do not impose
universal completeness or cardinalities on every dataset in the world. Extra
metadata is allowed and a generating activity is optional.

The unchanged Q21-01 query operates on raw RDF. Raw exports retain row-number
`rdf:value` assertions. The strict OWL view excludes only those serialization
assertions and reports the loss, so it cannot substitute for raw query data
without losing row-number information. Local admission and OWL consistency
answer different questions.

## Evidence and limits

The released profile has 24 frozen admission expectations and five bounded
HermiT cases, with separate OWLAPI/Pellet checks and serialization/portability
checks. The selected M001–M004 path was replayed on seven synthetic copied-W6
records in independent hosted databases. Those checks preserve the seven golden
Q21-01 tuples, four legacy query pairs, 24 base tables and 22 old default IRIs.
These are scoped reproducibility results, not evidence of real-source ingestion,
complete market coverage or product effectiveness.

The full V2 ontology remains evolving. This small stable profile does not
replace it, accept all 36 mappings or close the native model, domain modules,
ORSD or expert evaluation. Source-policy acceptance remains 1/4, historical
ORSD acceptance 0/83, and no new external expert responses are recorded.

## Version and citation

The distribution is 2.1.0 and the profile is 0.1.0. Cite the release-specific
CITATION.cff linked above and identify the exact profile used. The historical
source citation retains its own 1.0.0 identity. Research authors are Araz Saie
Arasi, Hassan Haghighi and Hossein Azgomi; their ORCIDs remain in the release citation.
Project-owned ontology/documentation and original code follow the precise
CC BY 4.0/MIT dispositions, while source fixtures and external runtimes retain
upstream terms. The support manifest provides the file-level scope.

## Related reading

[[Version and Release Index]] · [[V2 Formal Ontology and SHACL]] · [[Citation and Reuse]]

---

<details>
<summary>Documentation record</summary>

- **Page scope:** Released M1 provenance profile only
- **Documentation maturity:** Source-complete candidate; live public QA pending
- **Authoritative sources:** release/2.1.0@77a8e854d0e3927b0687346d7f8fda6a398adda7
- **Last synchronized:** 2026-10-29
- **Last synchronized ref:** main@d185ba2751a77658db9e282f13367362068d07d0; release/2.1.0@77a8e854d0e3927b0687346d7f8fda6a398adda7
- **Wiki baseline:** Existing WB-2026.09.1 retained; M1 increment awaits #339 public QA
- **Related issues:** #337, #338, #339
- **Evidence status:** Stable source release verified; this documentation increment is not yet published
- **Future refresh:** #338 generated reference/explorer; #339 public publication and QA

</details>
