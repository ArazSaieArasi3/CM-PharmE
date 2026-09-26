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

## Remaining #273 work

This first slice does not close #273. Remaining bounded work:
- generated evolution/changelog link and boundary;
- shell/download-page integration;
- V1/V2 isolation and overwrite negative tests;
- future V3 manifest-pattern dry run;
- sample download verification from assembled Pages candidate;
- final URL/path inventory and closure audit.
