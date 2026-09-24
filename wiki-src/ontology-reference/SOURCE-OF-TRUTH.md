# V2 ontology documentation source-of-truth rules

**Issue:** #234

## Authority hierarchy

1. **Approved conceptual decisions** — V2 W4 conceptual/review artifacts and conceptual registry.
2. **Formal ontology authority** — `v2/ontology/source/modules/*.ttl`.
3. **Formal regression baseline** — `v2/ontology/baseline/formal-baseline.json` and validation evidence.
4. **Review/evidence projection** — `v2/review/` Concept Evidence Passports, relation catalog and review packages.
5. **Wiki curated explanation** — human-readable interpretation/navigation.
6. **Wiki generated reference** — deterministic lookup projection of the above.

Lower layers must not override higher semantic authority.

## Conflict rule

If a generated Wiki page disagrees with the authoritative V2 source:
- treat the Wiki as stale/defective;
- do not “repair” authority from the generated page;
- regenerate or correct the generator;
- open/route semantic discrepancies through the governed review process if the authority itself may be wrong.

## Missing formal constraints

An absent OWL domain/range is reported as **unspecified**. The generator must not infer a missing endpoint from names, examples, data mappings or common sense.

## Conceptual/formal distinction

A conceptual element may formalize as an OWL class or declared datatype. Formal helper entities may exist outside the conceptual count. Coverage reports must state mapping/exclusion rules explicitly.

## Review status

Repository presence is not author approval. Current review statuses such as `pending` remain pending until a governed disposition exists.

## Namespace boundary

The selected target namespace is `https://w3id.org/cm-pharme/2.0/`. External redirect deployment/registration must not be implied merely because the namespace is used in formal source.

## Generated-page labeling

Every generated reference page states:
- that it is generated;
- authority ref;
- source artifacts;
- review state;
- that semantic changes do not occur through Wiki editing.
