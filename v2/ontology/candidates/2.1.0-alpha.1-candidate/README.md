# CM-PharmE 2.1: G1 implementation candidate

**2026-10-05 — author-approved design package implemented and tested; not a release.**

The author accepted the preceding 22-decision batch in the project conversation:
“بسیار خوب انجام بده / نتیجه را بگو بعد بگو چه کارهای دیگری باید انجام بدهیم”.
Twenty items are active refinements; S-04 and S-05 are approved deferrals.
This is author disposition, not independent expert validation or permission to
merge, release, or claim that the whole ontology has no anti-patterns.

The earlier `2.1.0-alpha.0-review` snapshot and G1 register remain historical.
This directory is the current implementation of that decision package.
Frozen 2.0 semantics, W7 measurements, source mappings and manuscript claims are
not retrospectively changed. No comprehensive diagram has been produced.

## Changes and their meaning

- Preserve Organization, Facility, Product, Substance, Presentation, record,
  assertion and observation identities. A Role uses the bearer's identity;
  it is not an additional individual.
- Add 34 Role classes and seven RoleMixin classes. The existing EvidenceItem
  RoleMixin now has SourceRecord and ObservationResult role specializations.
- Refactor the 15 registered rigid-end questions to anti-rigid participant
  patterns, including distinct authority/subject and reference/alternative
  positions. Each active Relator pattern has a two-distinct-participant minimum.
- A used IdentifierScheme and classified ClassificationEntry play contextual
  roles. Lexical identifiers remain literals, never mediated individuals.
- Contextual classification specializes the general classification assignment
  pattern. Its stereotype becomes Subkind; there are 11 identity-providing
  Relator classes and 12 tested profiles including that specialization.
- Evidence/context aliases subset their generic positions. Counting the same
  record via two property names does not create a second participant.
- Defer AssetAtRisk, its dependent Vulnerability/bearer pattern, and
  ClinicalCareParticipant outside the active ontology. Risk assessment activities
  and results remain. `deferred-not-imported.ttl` must not be imported as active.
- An OWLAPI check exposed 21 uses of undeclared `skos:altLabel` inherited from
  the review snapshot. Adding its AnnotationProperty declaration fixed this
  one root cause; both schemas now pass the executed profile check.

## Measured results

| Measure | Previous review candidate | This candidate |
|---|---:|---:|
| Conceptual classes | 81 | 119 |
| Datatypes | 6 | 6 |
| Total active concepts | 87 | 125 |
| Object properties | 57 | 57 |
| Protected distinction pairs preserved | 8 | 8 |

The 38-concept net increase is 41 new role abstractions minus three deferred
classes. It measures explicit modeling, not discovery of 38 new domain entities
and not a numerical quality score. One deferred property is balanced by the
generic `evidenceItem` property.

| Executed check | Outcome and scope |
|---|---|
| Official JSON schema | 416 elements individually validated; zero schema errors; separate ID/reference checks pass |
| Identity inheritance | All 34 new Roles retain exactly their intended Kind identity provider |
| RoleMixin identity diversity | Eight refined families span at least two Kind identities |
| Protected distinctions | All eight retained |
| SQLite admission + SHACL | 120/120 scenarios behave as expected: 36 accepted, 84 rejected |
| SQL/SPARQL agreement | 23 participant query templates across 36 valid fixtures, 828 comparisons including empty results |
| Temporal boundary | Role disappears at the exclusive end of validity; bearer identity survives |
| Rule-removal tests | All ten admission-rule removals let at least one known invalid fixture escape, so the suite detects each removal |
| HermiT | Schema and schema with 12 synthetic profile witnesses consistent; zero unsatisfiable named classes |
| Pellet 2.3.1 | Same two inputs consistent; zero unsatisfiable named classes |
| OWL 2 DL | OWLAPI 3.4.3 reports zero profile violations for both inputs |

The two engines run locally through Owlready2's bundled reasoners. Pellet is
invoked using its supported OWLAPIv3 loader because the Jena wrapper's bundled
parser requires a newer Java version. No engine binary or ontology axiom was
patched or ignored. Details and input hashes are in `reasoner-results.json`.

## Relational experiment

`lab/schema.sql` supplies the SQLite staging schema, base identity table,
relation instances, participation, context, provenance and derived role view.
`lab/fixtures.json` contains every synthetic scenario and its expected result.
`lab/validation.sql` gives the admission queries; `lab/admission-shapes.ttl`
provides the corresponding RDF checks. `lab/example-facility-operation.sql`
is a directly loadable example including rules and witness data.

The tables deliberately admit incomplete staging records. Passing the explicit
admission gate is required before calling a row a complete asserted relation.
Missing source data is not false, and a source supporting an assertion does not
prove that assertion true. No dataset was downloaded or represented as real
clinical/pharmaceutical evidence in this experiment.

The fixture generator, SQL validator and RDF exporter share the approved
contract. Their agreement tests implementation consistency, not independent
domain correctness. Semantic confidence still requires external source mappings,
held-out data and human counterexample review. Dates in this bounded lab use
normalized UTC intervals `[valid_from, valid_to)`; an RDF snapshot does not
encode full OntoUML modal semantics or all temporal role behavior. Context
version/jurisdiction values are synthetic and do not validate actual schemes.

## Connectivity and remaining findings

The reproducible **named-class OWL graph** uses named subclass edges and named
domain/range object-property edges. It excludes datatypes, anonymous restrictions
and untyped endpoints. On this same metric, components fall **27 → 19**, the
largest component grows **34/81 → 79/119**, and isolates fall **21 → 17**.
This is a different projection from the earlier drawing's 13 components and
must not be compared directly with that number. The ontology is not yet wholly
connected. Edges must be supported semantically, not added to force one component.

`structural-audit.json` records all 20 anti-pattern catalogue entries with
scoped passes, unresolved review items or non-applicability. There is no global
all-clear. In particular:

- 36 native relation records still require stereotype and/or multiplicity
  disposition, including inherited references and subset aliases.
- Nine inherited Role definitions need complete relational-grounding decisions.
- The official OntoUML semantic validator/anti-pattern engine has not run.
  JSON-schema validity is not semantic conformance.
- The native projection has no comprehensive diagram, full datatype-attribute
  mapping, or verified round-trip through the selected modeling application.
- Phase and part-whole patterns are not invented where the model lacks evidence.
- Complete baseline SHACL/CQ, source-mapping and held-out regression is pending.

## Next gates

1. **G2 — sources and connectivity:** resolve the remaining connections in
   `v2/research/w4/connection-candidates.csv`, especially observation/aboutness,
   procurement, disruption/stockout and optional digital/service modules. C05's
   polymorphic identifier design is addressed here; real mapping is still open.
2. **G3 — native semantics:** resolve the 36 relation records and nine inherited
   roles, then run the chosen official/tool-supported semantic validation and
   catalogue review. Record exceptions with rationale, not blanket passes.
3. **G4 — full evidence regression:** rerun source mappings, held-out boundaries,
   baseline CQs/SHACL, and traceability into Wiki/Pages/manuscript. This lab is a
   scoped addition, not a replacement for that evidence.
4. **G5 — stable review candidate:** reconcile migration decisions and remaining
   findings with the author. Only after the gates should the comprehensive
   OntoUML diagram and release designation be finalized.

## Reproduce

From repository root, install `tools/v2_ontology/g1-requirements.txt`; Java 17+
with the compiler module is needed for the Java source launcher. Then run:

```bash
python tools/v2_ontology/g1_model.py
python tools/v2_ontology/g1_audit.py
python tools/v2_ontology/g1_lab.py
python tools/v2_ontology/g1_reasoners.py
```

RDF blank-node serialization/order may differ between runs. Compare graph
isomorphism and outcomes; recorded hashes identify the actual tested artifacts.

Design references: [OntoUML patterns](https://ontouml.readthedocs.io/en/latest/patterns/index.html),
[anti-patterns](https://ontouml.readthedocs.io/en/latest/anti-patterns/index.html),
[official JSON schema](https://github.com/OntoUML/ontouml-schema).
