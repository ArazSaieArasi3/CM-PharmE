# V2 Dataset Landscape and Provenance

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** V2 W2/W3 source manifests, mappings and evidence registry  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** W2/W3 program and E6–E8 evaluation lineage  
> **Evidence status:** Data-grounding/evidence discipline established; full external ingestion is not claimed  
> **Future refresh:** #213/#214 where semantic/evidence decisions change  
> **Wiki baseline:** WB-2026.09.1

## Data strategy

V2 distinguishes:
- DOI-backed primary research datasets;
- complementary secondary datasets;
- authoritative operational/public sources where DOI is not expected;
- held-out datasets reserved from core discovery for generalizability evaluation.

## Why this matters

The V2 research claim is not merely that “more data” exist. The contribution is the explicit use of heterogeneous evidence to:
- admit or reject concepts/relations;
- record source-field mappings;
- distinguish direct, derived, bounded and ambiguous mappings;
- preserve provenance across transformations;
- evaluate coverage and held-out reuse without silently adapting the ontology after observation.

## Provenance model

V2 keeps first-class concepts/structures for:
- Data Source;
- Dataset;
- Dataset Release;
- Source Record;
- Assertion;
- Evidence Item / Evidence Support;
- Mapping Assertion;
- Provenance Activity;
- data-quality findings;
- identifier assignment;
- entity-match assertion and confidence.

Evidence records are not treated as the domain entities they describe.

## Mapping evidence

E6 records 39/39 mapping decisions explicitly, with:
- 36/38 in-scope fields direct/derived/bounded;
- 2 ambiguous;
- 0 unmapped.

This supports traceability for the evaluated contracts, not global source-schema coverage.

## Source-semantic coverage

E7 evaluates 97 requirements:
- 74 exact;
- 88 exact-or-partial.

Retained gaps are evidence, not defects to hide.

## Held-out evidence

E8 evaluates 51 frozen held-out requirements:
- 23 exact;
- 38 exact-or-partial;
- 0 first-pass Core identity conflicts.

This is bounded cross-source/cross-jurisdiction evidence, not proof of universal generalizability.

## W6 fixture boundary

The reference data pipeline uses deterministic schema-faithful fixtures for reproducibility. It does not claim full external dataset ingestion or real-world data completeness.

## Evidence

- [Source manifest](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/sources/source-manifest.json)
- [Source-field ontology mapping](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/mappings/source-field-ontology-mapping.csv)
- [Mapping documentation](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/mappings/README.md)
- [Evidence registry](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/evidence-registry.md)
- [Held-out source manifest](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/evaluation/heldout/e8-heldout-source-manifest.json)
