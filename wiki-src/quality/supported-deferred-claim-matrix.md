# WIKI-27 — Frozen Supported / Bounded / Deferred Claim Matrix

Issue: #238  
Status: **FROZEN BEFORE READER-FACING REFACTOR**  
Date: 2026-09-25  
Authority: `v2/evaluation/results/w7-claim-evidence-traceability.csv` on `v2/research-program`

## Interpretation

This is a documentation control matrix, not a new scientific evaluation. It preserves the current claim disposition and safe wording boundary so editorial work cannot inflate evidence.

| Claim | Short description | Frozen disposition | Reader-safe boundary |
|---|---|---|---|
| C-01 | Broader ecosystem coverage than V1 | **NARROW / BOUNDED** | Qualitative/design expansion and source-semantic coverage only; no like-for-like percentage improvement over V1. |
| C-02 | Data-grounded ontology evolution | **SUPPORTED WITH BOUNDARY** | Grounded in admitted real-source schemas/evidence; W6 reference execution uses schema-faithful fixtures rather than full-source ingestion. |
| C-03 | Explicit UFO/OntoUML commitments | **SUPPORTED WITH WARNING** | Project-native commitment checks supported; no official OntoUML-tool certification claim. |
| C-04 | Ontology–RDB–KG semantic traceability | **SUPPORTED WITH BOUNDARY** | Registered mappings/reference realization/frozen benchmarks only; not universal lossless bidirectional equivalence. |
| C-05 | Cross-jurisdiction generalizability | **SUPPORTED WITH BOUNDARY** | Limited to evaluated H1–H3 held-out families; not global completeness. |
| C-06 | Reproducible analytics/resilience tasks | **SELECTED ONLY** | AN-08 and frozen resilience scenarios only; unsupported AI/predictive tasks remain deferred. |
| C-07 | Identity/geography/time/provenance are material integration needs | **SUPPORTED** | Observed across evaluated source families; not asserted as universal requirements for every pharmaceutical dataset. |
| C-08 | Actor/facility geospatial demonstrator | **DESIGN SUPPORTED / EFFECTIVENESS DEFERRED** | Representability, provenance, query mechanics supported; usability/effectiveness remains a later application claim. |
| C-09 | Supply vulnerability/resilience demonstrator | **SUPPORTED WITH BOUNDARY** | Controlled scenario-level representational adequacy only; no predictive, causal, or operational-effectiveness claim. |
| C-10 | AI claims require benchmark evidence | **SUPPORTED** | No AI novelty/performance claim without task/data/baseline/metric evidence; current AI candidates remain deferred. |
| C-11 | Multi-source discovery rather than one-schema specification | **SUPPORTED** | Supported as a research-design discipline; not a completeness claim. |
| C-12 | Reserved held-out sources for generalizability | **SUPPORTED** | First-pass held-out evaluation occurred before adaptation; contamination discipline preserved. |
| C-13 | No complete global product→supplier→buyer→shipment reconstruction claim | **SUPPORTED LIMITATION** | Current public evidence is insufficient; this is an evidence boundary, not proof of impossibility. |
| C-14 | DOI anchors and operational sources have complementary roles | **SUPPORTED** | Source-role/provenance differences explicit; quantitative field mapping strongest for frozen P1/P2 contracts. |
| C-15 | Organization/Role/Facility distinction | **SUPPORTED** | Preserved conceptually, formally, and across evaluated representations. |
| C-16 | Product/Substance/Presentation/Form/Strength/Package distinctions | **SUPPORTED** | Principal distinctions preserved and source-grounded where corresponding fields exist. |
| C-17 | Essential/Critical medicine as contextual classification | **SUPPORTED** | Contextual-assignment pattern preserved and compatible with held-out essential-medicine evidence. |
| C-18 | Shortage/availability/demand/supply require context/evidence semantics | **SUPPORTED WITH BOUNDARY** | Context/provenance preserved; not all source-specific shortage semantics are fully modeled. |
| C-19 | Provenance/identifier/mapping assertions as first-class infrastructure | **SUPPORTED** | Supported by traceability and reproducibility evidence. |
| C-20 | Business Architecture as optional extension | **SUPPORTED** | BA remains outside Core; extension warnings do not invalidate Core. |
| C-21 | Regulatory authorization/registration distinct from records/identifiers | **SUPPORTED** | Distinction preserved; mappings avoid semantic collapse. |
| C-22 | Observation Activity distinct from Observation Result | **SUPPORTED** | No fabricated activity instances from aggregate results; distinction preserved across evaluated layers. |
| C-23 | Supply Capacity distinct from evidence about capacity | **SUPPORTED WITH WARNING** | Mode/result distinction preserved; bearer/dependence semantics remain bounded. |
| C-24 | Risk/Resilience remains modular extension | **SUPPORTED WITH WARNING** | Module boundary defensible; explicit extension gaps remain. |
| C-25 | Deterministic formal ontology generation | **SUPPORTED** | Two clean rebuilds reproduce frozen ontology fingerprint and byte-identical canonical artifacts. |
| C-26 | OWL 2 DL and multi-reasoner processability | **SUPPORTED WITH WARNING** | Named-class results pass; six datatype-compatibility warnings bound datatype-level claims. |
| C-27 | Equivalent asserted RDF graph across serializations | **SUPPORTED** | Graph equivalence and clean rebuild evidence support asserted-graph claim. |
| C-28 | Executable SHACL research-integrity shapes | **SUPPORTED WITH BOUNDARY** | Shapes execute and detect predefined mutations; universal external-source conformance is not implied. |
| C-29 | PostgreSQL/PostGIS preserves selected distinctions/provenance | **SUPPORTED WITH BOUNDARY** | Registered reference schema/fixture and mapped semantics only. |
| C-30 | Deterministic RDB→RDF ABox projection | **SUPPORTED** | 398-triple reference ABox and frozen KG fingerprint are deterministically reproduced. |
| C-31 | Selected SQL/SPARQL query equivalence | **SUPPORTED WITH BOUNDARY** | 4/4 frozen paired benchmarks agree; no universal SQL/SPARQL-equivalence claim. |
| C-32 | Auditable entity-match assertions | **MECHANICS SUPPORTED / ACCURACY DEFERRED** | Representation of match evidence/confidence supported; real-world precision/recall not evaluated. |

## Cross-cutting deferred / pending evidence

- **E9 prospective expert evaluation:** readiness package exists, but **0 real responses** and therefore **0 admissible expert-result claims**.
- **AI/ML performance and novelty:** deferred where benchmark evidence does not exist.
- **Real-world entity-resolution accuracy:** deferred.
- **Geospatial demonstrator effectiveness/usability:** design/representation supported; effectiveness remains deferred.
- **Representative-task completion:** current governed record is **6 PASS / 3 NOT_EXECUTED**; incomplete.
- **Demonstrator evaluation:** pending.
- **Research release readiness:** pending.
- **Independent scientific replication:** not established by repository-level reproducibility.

## Frozen editorial rule

No #238 prose edit may upgrade:
- `SUPPORTED_WITH_BOUNDARY` → unqualified supported;
- `SUPPORTED_WITH_WARNING` → warning-free;
- `DESIGN_SUPPORTED` or `MECHANICS_SUPPORTED` → effectiveness/accuracy;
- readiness → observed human result;
- reproducibility → independent replication;
- NOT_EXECUTED/pending → PASS/complete.

Any change to those states requires new authoritative research evidence, not editorial revision.
