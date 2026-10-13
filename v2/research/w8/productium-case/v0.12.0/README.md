# CM-PharmE Evidence Explorer — v0.12.0

This extends the earlier PR308 Product Knowledge fixture browser with a separate,
bounded pharmaceutical source-data demonstration. The earlier browser remains
unchanged. The new Explorer consumes a frozen openFDA extract already recorded in
CM-PharmE; it is not the W8 Observatory, a live service or a global ecosystem dataset.

Open `CMPharmE_Evidence_Explorer_v0_12_0.html` directly to search five product rows,
inspect seven package/listing projections and their exact source fields, and export
a selected versioned research brief. All read-model data is embedded in that file.

The mapping is `MedicinalProductPresentation → presentationOf → MedicinalProduct`,
with `MarketListing → listingPresentation → ListedPresentationRole` and
`MarketListing → listingResponsibleOrganization → ListingResponsibleOrganizationRole`.
The two listing links are native OntoUML mediations: the participant end is exactly
one and the relator end is one or more. Other unassigned native ends/stereotypes
remain unassigned in the extracted relation table rather than invented here.

Names identify row-scoped references only. A labeler is not automatically a
manufacturer or distributor. Listing, NDC presence and a marketing category do not
establish approval. Source-missing controls are separate synthetic mutations and do
not create purported real observations. The original query is five source product
rows, not seven independent product rows or representative global coverage.

## Reproduce

Install rdflib 7.6.0, pyshacl 0.30.1 and owlrl 7.1.4. Node functional tests use
linkedom 0.18.12 through `LINKEDOM_PATH`; Java/ROBOT are optional for fresh reasoning.

```
python integrate_case.py
python build_ui.py
python test_integration.py
node test_ui.mjs
ROBOT_JAR=/path/to/robot-1.9.11.jar python verify_reasoner.py
```

Python generation creates an exact 227-triple RDF export and a SQLite read model.
RDF/SQL roundtrip is isomorphic; seven listing-chain tuples agree with SPARQL.
Twenty source/SQL checks and twenty Node/DOM checks pass. The native SHACL profile
accepts the population and rejects four malformed participant controls. HermiT
accepts the 89 native logical population triples plus the pinned candidate ontology
and rejects a product/organization identity collision. The 138 document/experimental
metadata triples remain retained separately. Full-PROV and later candidate alignment
proposals are not treated as accepted native changes by this implementation.

Source and model are pinned to CM-PharmE commit
`09d60136a990d6602438be4085a4d407c9bd5c68`; source response SHA-256
`ecb97302aa8cb3148a7971045811164bef22a4d988542d8af77a0829091330de`.
The original API retrieval was 2026-10-09T20:11:56.284077+00:00; no fresh live pull is claimed.

The exact G1 candidate and current branch are not a published release or independent
semantic validation. Four of five external adapter contracts are implemented; the
broader manufacturer/distributor mapping remains partial. Actual browser visual and
filesystem download validation, independent domain/user acceptance and effectiveness
evaluation remain open. Original synthetic TC01–04 are not retrospectively marked
executed by these separate real-source tasks.

The historical folder name is a compatibility path, not a new ontology-brand decision.
No private manuscript, private industrial record or Product repository baseline is
included in this public implementation package.

Primary source semantics: https://open.fda.gov/apis/drug/ndc/.
