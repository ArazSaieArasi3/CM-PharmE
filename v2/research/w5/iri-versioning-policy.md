# W5 IRI, Versioning and Provenance Policy

## Namespace
Selected V2 semantic namespace: `https://w3id.org/cm-pharme/2.0/`.

The repository currently records this as the **target persistent namespace**. A deployed w3id redirect is not claimed until external registration is actually completed and tested.

## Ontology identifiers
- Ontology IRI: `https://w3id.org/cm-pharme/2.0/ontology`
- Current formal-development version IRI: `https://w3id.org/cm-pharme/2.0/releases/2.0.0-alpha.1/ontology`
- Current formal-development version: `2.0.0-alpha.1`

## Entity stability
A semantic entity IRI is not changed merely because a source dataset changes its label or identifier. Identifier values from NDC, ATC, ChEMBL, GeoNames, regulatory systems or local datasets are represented through identifier/mapping semantics rather than used as the ontology entity IRI.

## Change categories
- Editorial annotation change: no identity change.
- Compatible formal refinement: IRI retained; change recorded.
- Material semantic redefinition: explicit design-change record required; deprecation/replacement preferred to silent reuse.
- Gate-D identity/dependence reversal: requires conceptual review before formal merge.

## Modules
Core, X-INFRA, Extension and Mapping modules share the V2 entity namespace. Module files organize formalization; they do not create competing identities for the same concept.

## Provenance
Ontology metadata records version, date, creator and formalization status. Build manifests record source modules, graph fingerprint, inventory, validation outcomes and pending persistent-namespace status.

## Release rule
A final `2.0.0` release is not created during W5. W5 establishes a tested alpha formal baseline for W6 data realization and later W7 evaluation.
