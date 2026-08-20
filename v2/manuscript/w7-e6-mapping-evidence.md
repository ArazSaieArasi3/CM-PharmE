# W7-E6 Mapping Evidence for the Manuscript

Final status: **PASS WITH WARNING**. Final CI run `32337590134`; evidence artifact `9395173816`.

Supported result for the two frozen NHIF field-level source contracts:
- 39/39 source fields have explicit mapping decisions;
- 38 fields are in scope;
- 36/38 in-scope fields are direct, derived, or bounded mappings (94.74%);
- two `atc_name` decisions remain explicitly ambiguous for substance-level interpretation;
- zero in-scope fields are unmapped;
- 28 fields are critical to principal claims, with zero ambiguous or unmapped;
- provenance rules are documented for 39/39 field decisions;
- the frozen author-side semantic audit sample passed 12/12.

Per source, P1 NHIF outpatient has 19/19 fields classified and 17/18 in-scope mapped (94.44%); P2 NHIF inpatient has 20/20 fields classified and 19/20 in-scope mapped (95.00%).

This evidence is source-specific. It is not an ontology-completeness score and does not establish field-level coverage of contract-only FDA, openFDA, or EMA sources. H1-H3 remain unused.

The manuscript must preserve the distinction between `direct`, `derived`, `bounded`, `ambiguous`, `unmapped`, and `out_of_scope` mappings. In particular, `atc_name` must not be reported as independently validated active-substance identity, and RDB-only presentation/diagnosis/currency semantics must not be described as fully projected RDF semantics.
