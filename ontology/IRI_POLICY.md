# CM-PharmE IRI Policy

## Purpose

CM-PharmE uses persistent, identifier-based IRIs so that labels, definitions, domains, and ontology commitments can evolve without changing the identity of released semantic entities.

## Planned persistent namespace

The project reserves the namespace:

`https://w3id.org/cm-pharme/`

The `w3id.org` redirect configuration is **not yet registered by this B3 branch**. Until the redirect is deployed, these IRIs are persistent identifiers used by the ontology source but should not be described as dereferenceable public URLs. Redirect registration and publication deployment belong to the release/automation cycle.

## IRI patterns

| Entity | Pattern | Example |
|---|---|---|
| Ontology | `https://w3id.org/cm-pharme/ontology` | — |
| Development version IRI | `https://w3id.org/cm-pharme/ontology/dev/b3` | — |
| Released version IRI | `https://w3id.org/cm-pharme/ontology/{semver}` | `.../ontology/1.1.0` |
| Concept | `https://w3id.org/cm-pharme/concept/{stable-id}` | `.../concept/CMPE-C0001` |
| Relation | `https://w3id.org/cm-pharme/relation/{stable-id}` | `.../relation/CMPE-R0001` |
| Domain | `https://w3id.org/cm-pharme/domain/{stable-id}` | `.../domain/CMPE-D0001` |
| Metamodel term | `https://w3id.org/cm-pharme/meta/{term}` | `.../meta/Relator` |
| SHACL shape | `https://w3id.org/cm-pharme/shape/{shape-id}` | `.../shape/CMPE-R0001-forward` |

## Stability rules

1. Stable IDs are identity-bearing; English labels are not.
2. Renaming a concept or relation does not change its IRI.
3. A deprecated entity retains its IRI and is marked as deprecated rather than deleted.
4. A superseding entity uses a different stable ID only when the semantic identity changes.
5. Released version IRIs are immutable.
6. Development IRIs must not be cited as stable release IRIs.
7. Historical v1.0.0 Draw.io/XML/OWL artifacts keep their original identifiers and are not rewritten to conform to this policy.

## Namespace separation

CM-PharmE keeps concept, relation, domain, and metamodel IRIs in separate paths. This prevents accidental collisions and makes the role of an identifier apparent without relying on lexical naming conventions.

## Labels and definitions

Every canonical concept and relation in the formal ontology has:

- `dcterms:identifier`
- `skos:prefLabel`
- `skos:definition`
- lifecycle/status metadata
- ontology stereotype metadata

Labels may evolve through controlled semantic changes; the stable identifier remains unchanged.
