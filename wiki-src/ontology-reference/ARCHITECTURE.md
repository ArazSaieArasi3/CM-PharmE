# V2 ontology documentation architecture

**Issue:** #234  
**Authority:** `v2/research-program`  
**Authority ref checked:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
**Status:** generated-reference architecture with curated explanatory layer

## Reader architecture

```text
Home
└── V2 Ontology Reference
    ├── 17 module reference pages
    ├── 87 conceptual-element reference pages
    ├── 52 object-property reference pages
    └── 5 datatype-property reference pages
```

The existing [[Ontology and Conceptual Model Guide]] remains the explanatory cross-version entry point. `V2 Ontology Reference` is also linked directly from Home so every generated leaf remains within the two-step navigation contract.

## Documentation layers

### Curated explanatory layer
Maintained by authors:
- ontology purpose and scope;
- V1→V2 interpretation;
- architecture and module model;
- formalization strategy;
- namespace/version policy;
- reading/use guidance;
- semantic/evidential boundaries.

### Generated reference projection
Deterministically generated from V2 authority:
- module catalogs;
- concept/passport reference;
- object-property reference;
- datatype-property reference;
- formal mapping/coverage report.

Generated pages expose authority; they do not become authority.

## Authoritative inputs

1. `v2/ontouml/cm-pharme-v2.conceptual-model.json`
2. `v2/review/domains/index.md`
3. `v2/review/concepts/passports/*.md`
4. `v2/review/relations/index.md`
5. `v2/ontology/source/modules/*.ttl`
6. `v2/ontology/shapes/cm-pharme-v2.shacl.ttl`
7. `v2/ontology/baseline/formal-baseline.json`
8. V1→V2 migration/review artifacts under `v2/research/w3`, `v2/research/w4` and `v2/review/version-evolution.md`.

## Count semantics

The following counts must remain distinct:
- **87 conceptual elements** — Gate-D conceptual registry;
- **81 OWL classes** — formal class implementation;
- **6 declared conceptual/formal datatypes** — non-class conceptual elements;
- **52 object properties** — formal relation implementation/review surface;
- **5 datatype properties** — literal-valued formal properties.

Therefore 87 conceptual elements must never be restated as “87 OWL classes.”

## Review-state rule

Current concept/relation review projections are pending human/author review. A generated Wiki page:
- may report `pending`;
- may expose evidence/provenance already registered;
- may expose formal domain/range/subclass constraints;
- may not infer missing domain/range;
- may not mark a concept/property approved;
- may not change the ontology.

Semantic changes are governed through #213 / the review finding and re-review workflow.

## Navigation rule

Every generated reference page is linked from `V2 Ontology Reference`. This keeps reference leaves at depth 2 from Home without forcing the normal Ontology Guide to become a 140-link catalog.

## Regeneration rule

A V2 semantic refresh requires:
1. regenerate reference pages from a named V2 authority ref;
2. recompute coverage;
3. retain pending/review statuses truthfully;
4. rerun Wiki source/navigation/metadata/diagram QA;
5. record the synchronization in Wiki Update Register.
