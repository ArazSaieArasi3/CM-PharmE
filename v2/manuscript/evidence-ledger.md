# CM-PharmE 2.0 Manuscript and Evidence Ledger

## Purpose
Keep manuscript claims synchronized with repository, datasets, ontology artifacts, evaluation results and application evidence. Claims are recorded as Proposed, Evidence pending, Supported, Bounded/qualified, Rejected or Deferred.

## Candidate claims and current evidence state
| ID | Candidate claim | Current evidence state |
|---|---|---|
| C-01 | V2 provides broader pharmaceutical-ecosystem concept coverage than V1. | W3/W4 design expansion supported; comparative coverage result pending W7. |
| C-02 | V2 is data-grounded rather than scenario-grounded. | **Supported as W2–W5 research/formalization design; empirical realization pending W6.** |
| C-03 | UFO/OntoUML commitments are explicit and systematically preserved. | **Supported by Gate-D decisions and W5 machine-readable registry/formal annotations; official OntoUML-tool validation is not claimed.** |
| C-04 | Ontology, relational database and KG preserve traceable semantics. | Evidence pending — W6/W7. |
| C-05 | V2 supports cross-jurisdiction/generalizable representation. | Held-out design protected through W5; results pending W7. |
| C-06 | Selected analytics/resilience use cases can be reproducibly executed. | Evidence pending — W6/W7. |
| C-07 | Cross-source identity, Organization/Site distinction, geography/jurisdiction, time and provenance are material integration needs. | **Supported as bounded design need.** |
| C-08 | Geospatial actor/facility integration is a defensible research demonstrator. | Rationale/data/conceptual/formal model supported; W6/W7 results pending. |
| C-09 | Critical-medicine supply vulnerability/resilience is a defensible demonstrator. | Rationale/data/conceptual/formal model supported; W6/W7 results pending. |
| C-10 | AI opportunities require benchmarks and should not be novelty claims by default. | Bounded / future-dependent. |
| C-11 | V2 uses multi-source discovery rather than treating one dataset schema as the ontology specification. | **Supported as research design.** |
| C-12 | External sources were reserved before Core discovery for later generalizability evaluation. | **Design and W3–W5 contamination discipline supported; outcome pending W7.** |
| C-13 | Current public evidence does not justify complete global Product→Supplier→Buyer→Shipment reconstruction. | **Supported as limitation / negative finding.** |
| C-14 | DOI-backed empirical anchors and authoritative operational sources play complementary research roles. | Source-role design supported; ETL/mapping evidence pending W6. |
| C-15 | V2 distinguishes Organization, contextual Role and physical Facility. | **Supported conceptually and protected in W5 OWL.** |
| C-16 | V2 distinguishes Medicinal Product, Substance, Presentation, Form, Strength and Package semantics. | **Supported conceptually and represented in W5 formal ontology.** |
| C-17 | Essential/Critical medicine classifications are contextual rather than intrinsic rigid Product kinds. | **Supported by W4 pattern and W5 assignment/Relator formalization.** |
| C-18 | Shortage/availability/demand/supply evidence requires explicit context and evidence semantics. | **Supported conceptually/formally; instance evaluation pending W6/W7.** |
| C-19 | Provenance, identifier schemes and mapping assertions are first-class V2 infrastructure. | **Supported conceptually and formally; populated provenance pending W6.** |
| C-20 | Business Architecture is an optional analytical extension rather than the V2 Core decomposition. | **Supported as W3–W5 architecture decision.** |
| C-21 | Regulatory registration/authorization must be separated from source records/documents/identifiers. | **Supported by W4 Relator analysis and W5 formalization.** |
| C-22 | Observation Activity and Observation Result are distinct. | **Supported by W4 and explicit W5 protected distinction.** |
| C-23 | Supply Capacity is distinct from evidence about Supply Capacity. | **Supported by W4 Mode/Result distinction and W5 protected formalization.** |
| C-24 | Risk/Resilience remains a modular extension aligned toward UFO-grounded reference work rather than duplicated in Core. | **Supported as architecture; exact COVER/ROSE alignment remains future work.** |
| C-25 | The W5 formal ontology is reproducibly generated from controlled modular Turtle. | **Supported: two-pass canonical build PASS in GitHub Actions run 32215753957.** |
| C-26 | The W5 artifact satisfies the selected OWL 2 DL profile and is logically processable by HermiT. | **Supported for the current axiom set: ROBOT profile PASS and HermiT PASS in run 32215753957.** |
| C-27 | W5 serializations represent the same asserted RDF graph. | **Supported: TTL/RDF/XML/OWL/JSON-LD/N-Triples graph-isomorphism PASS.** |
| C-28 | W5 SHACL research-integrity shapes are executable. | **Supported: Meta-SHACL PASS and formal smoke PASS across 11 NodeShapes. Future source-data conformance is not implied.** |

## Formal W5 evidence
Frozen formal-development baseline:
- version `2.0.0-alpha.1`;
- 642 asserted triples;
- SHA-256 `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`;
- 87 Gate-D conceptual elements represented by 81 OWL classes + 6 declared datatypes;
- 52 object properties and 5 datatype properties;
- eight protected Gate-D distinctions explicitly checked;
- 11 SHACL NodeShapes;
- HermiT reasoned artifact generated from the current axiom set.

Final mandatory run: GitHub Actions `32215753957` — **SUCCESS**. Formal evidence artifact ID: `9352276802`.

## Evidence artifacts by wave
### W1
`v2/research/w1/` — needs, use cases, analytics/AI, geospatial/resilience, application and opportunity evidence.

### W2
`v2/research/w2/` — dataset landscape, DOI registry, operational sources, admission rubric/scorecard and Gate-C portfolio.

### W3
`v2/research/w3/` — schema interpretation, candidate concepts/relations, provenance/identifiers, V1→V2 migration, traceability and admission protocol.

### W4
`v2/research/w4/` — architecture, UFO stereotype decisions, relator/event/geography patterns, Risk/BA extensions, integrated conceptual model, anti-pattern review and Gate-D freeze.

### W5
- `v2/ontology/source/modules/` — authoritative formal source;
- `v2/ontouml/cm-pharme-v2.conceptual-model.json` — project-native conceptual registry;
- `v2/ontology/shapes/cm-pharme-v2.shacl.ttl` — SHACL profiles;
- `v2/ontology/tests/formal-smoke.ttl` — formal smoke fixture;
- `v2/ontology/baseline/formal-baseline.json` — frozen regression baseline;
- `tools/v2_ontology/build_validate.py` — deterministic build/validation;
- `.github/workflows/v2-ontology-ci.yml` — profile/reasoning CI;
- `v2/research/w5/` — IRI/version, formalization, mapping and validation documentation;
- `v2/manuscript/w5-formalization-notes.md` — manuscript method/claim boundaries.

## Manuscript skeleton
1. Introduction
2. Background and prior CM-PharmE lineage
3. Research design and dataset admission protocol
4. Concept discovery and evidence traceability
5. UFO/OntoUML conceptualization
6. Formal ontology and constraints
7. Relational/KG realization and data integration
8. Evaluation
9. Application demonstrator(s)
10. Discussion
11. Limitations
12. Conclusion

## Writing guidance after W5
The manuscript may report the W5 formal architecture and exact formal metrics only as **current formalization results**. It may state that the asserted 642-triple graph passed the selected OWL 2 DL profile, deterministic serialization/regression checks, SHACL smoke validation and HermiT reasoning in the recorded GitHub run.

Do not infer from these results that the ontology is domain-complete, externally standardized, empirically validated or generalizable. Do not describe the project-native JSON as official OntoUML JSON. Do not describe the w3id redirect as deployed. Mapping accuracy, SQL↔SPARQL equivalence, data coverage, held-out generalizability, AI performance, expert validation and demonstrator effectiveness remain W6/W7 results.

## Persistent limitations
- No complete global transaction-level pharmaceutical supply graph claim.
- Detailed supply/procurement population relies materially on conditional evidence and future W6 data.
- Finance/counterparty remains outside Core.
- H1/H2/H3 remain protected until W7.
- Exact external-standard/risk-ontology conformance remains unclaimed without dedicated evaluation.

## Writing rule
No result is written as completed until its corresponding repository/data evidence exists and passes the applicable gate.
