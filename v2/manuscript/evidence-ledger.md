# CM-PharmE 2.0 Manuscript and Evidence Ledger

## Purpose
Keep manuscript claims synchronized with repository, datasets, ontology artifacts, evaluation results and application evidence. Claims are recorded as Proposed, Evidence pending, Supported, Bounded/qualified, Rejected or Deferred.

## Candidate claims and current evidence state
| ID | Candidate claim | Current evidence state |
|---|---|---|
| C-01 | V2 provides broader pharmaceutical-ecosystem concept coverage than V1. | W3/W4 design expansion supported; comparative coverage result pending W7. |
| C-02 | V2 is data-grounded rather than scenario-grounded. | **Supported as W2–W6 research/formalization/representation design; full empirical evaluation pending W7.** |
| C-03 | UFO/OntoUML commitments are explicit and systematically preserved. | **Supported by Gate-D decisions and W5 machine-readable registry/formal annotations; W7-E3 evaluation pending. Official OntoUML-tool validation is not claimed.** |
| C-04 | Ontology, relational database and KG preserve traceable semantics. | **Supported for the registered W6 reference implementation/fixture: explicit ontology↔RDB registry, provenance checks and 4/4 paired SQL↔SPARQL benchmarks PASS. Broader empirical equivalence remains bounded; W7-E10 pending.** |
| C-05 | V2 supports cross-jurisdiction/generalizable representation. | Held-out design protected through W6; results pending W7-E8. |
| C-06 | Selected analytics/resilience use cases can be reproducibly executed. | Architecture/query mechanics supported in W6; demonstrator/effectiveness evidence pending W7/W8. |
| C-07 | Cross-source identity, Organization/Site distinction, geography/jurisdiction, time and provenance are material integration needs. | **Supported as bounded design need and represented in W6.** |
| C-08 | Geospatial actor/facility integration is a defensible research demonstrator. | Rationale/data/conceptual/formal/PostGIS-ready representation supported; empirical W7/W8 result pending. |
| C-09 | Critical-medicine supply vulnerability/resilience is a defensible demonstrator. | Rationale/data/conceptual/formal model supported; empirical W7/W8 result pending. |
| C-10 | AI opportunities require benchmarks and should not be novelty claims by default. | Bounded / future-dependent; W7-E11 eligibility rule frozen. |
| C-11 | V2 uses multi-source discovery rather than treating one dataset schema as the ontology specification. | **Supported as research design.** |
| C-12 | External sources were reserved before Core discovery for later generalizability evaluation. | **Design and W3–W6 contamination discipline supported; outcome pending W7-E8.** |
| C-13 | Current public evidence does not justify complete global Product→Supplier→Buyer→Shipment reconstruction. | **Supported as limitation / negative finding.** |
| C-14 | DOI-backed empirical anchors and authoritative operational sources play complementary research roles. | **Supported at source-role and W6 adapter-contract level; full mapping/coverage evaluation pending W7-E6/E7.** |
| C-15 | V2 distinguishes Organization, contextual Role and physical Facility. | **Supported conceptually, protected in W5 OWL and preserved in W6 relational design.** |
| C-16 | V2 distinguishes Medicinal Product, Substance, Presentation, Form, Strength and Package semantics. | **Supported conceptually/formally; Product/Substance/Presentation are separately realized in W6.** |
| C-17 | Essential/Critical medicine classifications are contextual rather than intrinsic rigid Product kinds. | **Supported by W4 pattern and W5 assignment/Relator formalization.** |
| C-18 | Shortage/availability/demand/supply evidence requires explicit context and evidence semantics. | **Supported conceptually/formally; W6 establishes reusable observation/provenance representation mechanics.** |
| C-19 | Provenance, identifier schemes and mapping assertions are first-class V2 infrastructure. | **Supported conceptually, formally and through populated W6 fixture provenance/identifier/evidence structures.** |
| C-20 | Business Architecture is an optional analytical extension rather than the V2 Core decomposition. | **Supported as W3–W5 architecture decision.** |
| C-21 | Regulatory registration/authorization must be separated from source records/documents/identifiers. | **Supported by W4 Relator analysis and W5 formalization.** |
| C-22 | Observation Activity and Observation Result are distinct. | **Supported by W4/W5; W6 deliberately avoids fabricating unobserved activity instances from aggregate administrative rows.** |
| C-23 | Supply Capacity is distinct from evidence about Supply Capacity. | **Supported by W4 Mode/Result distinction and W5 protected formalization.** |
| C-24 | Risk/Resilience remains a modular extension aligned toward UFO-grounded reference work rather than duplicated in Core. | **Supported as architecture; exact COVER/ROSE alignment remains future work.** |
| C-25 | The W5 formal ontology is reproducibly generated from controlled modular Turtle. | **Supported: deterministic canonical build PASS; independent W7-E13 audit pending.** |
| C-26 | The W5 artifact satisfies OWL 2 DL and is logically processable by multiple applicable reasoners. | **Supported with boundary by W7-E2: OWL 2 DL PASS; HermiT and JFact both exit 0; 0 unsatisfiable named classes; exact agreement on 91 materialized named-class subclass pairs. JFact emits six compatibility messages for project-native conceptual datatypes; no current reasoning-bearing uses of those datatypes were detected.** |
| C-27 | W5 serializations represent the same asserted RDF graph. | **Supported: TTL/RDF/XML/OWL/JSON-LD/N-Triples graph-isomorphism PASS.** |
| C-28 | W5 SHACL research-integrity shapes are executable. | **Supported: Meta-SHACL PASS and formal smoke PASS across 11 NodeShapes. Future source-data conformance is not implied; W7-E5 pending.** |
| C-29 | A PostgreSQL/PostGIS reference representation can preserve selected ontology distinctions and provenance. | **Supported for the W6 schema-faithful fixture through explicit mappings and relational invariants.** |
| C-30 | The W6 relational fixture can be deterministically projected to an ontology-aligned RDF ABox. | **Supported: 398-triple ABox generated deterministically with canonical SHA-256 `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`.** |
| C-31 | Selected RDB and KG queries can return equivalent answers for registered questions. | **Supported for 4/4 registered W6 SQL↔SPARQL fixture benchmarks only; universal equivalence is not claimed.** |
| C-32 | Cross-source entity matches can be represented as auditable assertions with evidence/confidence. | **Supported as W6 implementation mechanics; two exact fixture matches executed. Real-world accuracy is not yet evaluated.** |

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

Formal Gate: **APPROVED**. W5 was merged only into `v2/research-program`.

## W6 representation evidence
Successful W6 fixture baseline:
- 7 source records;
- 7 relational aggregate observations;
- 2 products, 2 presentations, 2 substances, 2 facilities and 2 normalized geographies;
- 7 assertions and 7 evidence-support records;
- 2 accepted exact cross-source presentation-match assertions;
- 36 registered ontology↔RDB mappings resolve to W5 terms;
- 398 RDF ABox triples;
- canonical KG SHA-256 `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`;
- zero unknown CM-PharmE terms in the generated KG;
- SHACL conformance PASS;
- relational/provenance invariants PASS;
- SQL↔SPARQL equivalence 4/4 registered benchmarks PASS;
- OpenAPI syntax PASS;
- held-out H1–H3 unused.

**Boundary:** this evidence comes from deterministic schema-faithful synthetic fixtures implementing the admitted NHIF source contracts. It is not evidence that the full external datasets were ingested or that real-world entity resolution, geocoding, generalizability or application effectiveness has been evaluated.

## W7 evidence to date
### W7 protocol
Frozen before result interpretation at commit `7419f37796835522667fb36a60a4c9bbd5f0e09a`.

### W7-E1 — structural quality
Mandatory structural gate PASS with non-blocking WARN. Actions run `32231194172`; evidence artifact `9357280400`.

### W7-E2 — logical and multi-reasoner
Mandatory logical gate PASS; family status WARN due a documented JFact compatibility limitation. Final Actions run `32234016236`; evidence artifact `9358275161`.
- OWL 2 DL profile: PASS;
- HermiT: exit 0; 0 unsatisfiable named classes;
- JFact: exit 0; 0 unsatisfiable named classes;
- named internal classes: 81;
- named subclass pairs: 91 vs 91, exact agreement;
- project-native datatypes: 6; no current reasoning-bearing semantic uses detected;
- JFact's six datatype-factory messages are retained rather than suppressed.

Repository report: `v2/research/w7/e2-logical-multireasoner.md`.

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
- `v2/ontology/baseline/formal-baseline.json` — frozen regression baseline;
- `tools/v2_ontology/build_validate.py` — deterministic build/validation;
- `.github/workflows/v2-ontology-ci.yml` — profile/reasoning CI;
- `v2/research/w5/` and `v2/manuscript/w5-formalization-notes.md`.

### W6
- `v2/data/db/` — PostgreSQL/PostGIS schema and views;
- `v2/data/mappings/ontology-rdb-mapping.csv` — semantic traceability;
- `v2/data/sources/source-manifest.json` — source contracts and boundaries;
- `v2/data/fixtures/` — schema-faithful deterministic fixtures;
- `v2/data/queries/sql-sparql-benchmarks.json` — paired benchmarks;
- `v2/data/api/openapi.yaml` — bounded access contract;
- `tools/v2_data/` — ingestion, KG export, validation and equivalence tooling;
- `.github/workflows/v2-data-ci.yml` — W6 representation gates;
- `v2/research/w6/` and `v2/manuscript/w6-data-infrastructure-notes.md`.

### W7
- `v2/research/w7/evaluation-protocol.md` — frozen prospective protocol;
- `v2/evaluation/protocol/` — metric/claim-evidence registries;
- `v2/evaluation/results/w7-evidence-status.csv` — family status register;
- `v2/research/w7/e1-structural-quality.md` — W7-E1 report;
- `v2/research/w7/e2-logical-multireasoner.md` — W7-E2 report;
- `tools/v2_evaluation/` — W7 evaluator code;
- dedicated W7 GitHub Actions workflows.

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

## Writing guidance after W7-E2
The manuscript may state that the frozen asserted ontology passed OWL 2 DL profile validation and that HermiT and JFact both completed on the current axiom set with no unsatisfiable named CM-PharmE classes and exact agreement on 91 materialized named-class subclass pairs. This statement must retain the boundary that JFact logged six compatibility messages for project-native conceptual datatypes; these datatypes are not currently used in reasoning-bearing positions, so no datatype-reasoning equivalence claim is made.

Do not infer domain completeness, semantic truth, empirical validity, standards conformance or complete cross-reasoner equivalence from W7-E2.

## Persistent limitations
- No complete global transaction-level pharmaceutical supply graph claim.
- Detailed supply/procurement population remains conditional/future data work.
- Finance/counterparty remains outside Core.
- H1/H2/H3 remain protected until W7-E8.
- Exact external-standard/risk-ontology conformance remains unclaimed without dedicated evaluation.
- W6 CI validates mechanics on synthetic schema-faithful fixtures rather than full real datasets.
- Project-native conceptual datatypes require future definition/refinement before datatype-dependent multi-reasoner claims.

## Writing rule
No result is written as completed until its corresponding repository/data evidence exists and passes the applicable gate.
