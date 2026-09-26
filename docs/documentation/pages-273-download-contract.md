# PAGES-06 Download Bundle Contract

Issue: #273  
Parent: #267

## Slice 1 scope

This slice packages already-governed semantic build outputs. It does **not** author new ontology content and it does not treat copied/generated files as semantic authority.

Per supported version the bundle contains:
- Turtle;
- RDF/XML as `.owl`;
- RDF/XML as `.rdf`;
- JSON-LD;
- canonical N-Triples;
- `download-manifest.json`;
- `provenance.json`;
- `SHA256SUMS.txt`.

## Governing checks

Before a file is advertised:
1. version registry, build contract and download contract must agree on the exact source ref;
2. the upstream semantic build must already have passed;
3. each RDF-compatible serialization is reparsed and checked graph-isomorphic to the governed Turtle documentation input;
4. every advertised file receives a SHA-256;
5. the emitted checksum manifest is immediately reverified;
6. generated artifacts are labeled derived/publication artifacts, never authoring authority.

## Version isolation

- V1 bundle target: `/ontology/v1.0.0/downloads/`
- V2 bundle target: `/ontology/v2/current/downloads/`

There is no generic mutable `latest` download route.

V1 inherits immutable stable-path policy from the registry. V2 retains its explicit **Stable-to-date / Evolving** status and must not be represented as a final semantic release.

## Machine-readable traceability

The manifest/provenance pair exposes:
- version/lifecycle;
- exact semantic source ref and commit SHA;
- canonical graph fingerprint;
- upstream build tool and build-manifest checksum;
- governed documentation-input checksum;
- per-download checksums and sizes;
- repository/source/Wiki/citation paths;
- authority boundary.

## Evolution/changelog boundary

Each generated download manifest links to:
- the repository-level `CHANGELOG.md` as a technical/generated evolution aid;
- the curated Wiki research-evolution page.

The manifest and rendered download page explicitly state that the repository changelog does **not** replace the curated research-evolution narrative.

## Slice 2 integration contract

When verified bundles already exist in a Pages candidate, the shell reads their machine-readable manifests and renders:
- direct links to all five verified serializations;
- per-file SHA-256 values;
- manifest/provenance/checksum links;
- lifecycle/source boundaries;
- evolution/changelog links and boundary.

When bundles are absent, the independent shell build retains its placeholder page, so #270 remains independently testable.

Negative guards include:
- a second write to a non-empty bundle path MUST fail;
- a synthetic V3 contract must resolve to its own `/ontology/v3/current/downloads/` route through the same pattern;
- a colliding V3/V2 route MUST be rejected by contract validation.

## Remaining #273 work

After this slice only final closure QA remains:
- final assembled Pages URL/path inventory;
- sample-download checksum/reparse verification from the assembled candidate;
- final closure disposition against every #273 AC.
