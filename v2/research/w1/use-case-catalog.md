# W1 Pharmaceutical Ecosystem Use-Case Catalog

Classification at W1 is provisional. Final dataset feasibility is a W2 decision.

| UC | Use case | Primary actor / decision | Required semantics | Candidate output / metric | W1 classification |
|---|---|---|---|---|---|
| UC-01 | Global pharmaceutical actor/facility map | Regulator, researcher, public-health analyst: where are relevant organisations and sites located and what roles/statuses do they have? | Organization, Role, Site/Facility, Location, Jurisdiction, Authorisation, Identifier, Provenance | Map coverage, geocoding/identity accuracy, cross-jurisdiction coverage | **Research Demonstrator candidate** |
| UC-02 | Critical-medicine supply vulnerability | Regulator/public-health authority: which critical medicines depend on concentrated sites/suppliers/geographies? | Critical Medicine, Product/Substance, Site, Supplier/Dependency, Jurisdiction, Geography, Alternative | concentration/centrality, alternate-site coverage, vulnerability queries | **Research Demonstrator candidate** |
| UC-03 | Shortage/resilience scenario analysis | Regulator/MAH: what downstream entities may be affected by a disruption or demand shock? | Disruption Event, Shortage, Dependency, Product, Site, Supplier, Region, Recovery/Alternative | affected-node reach, path/dependency analysis, scenario query correctness | **Research Demonstrator candidate** |
| UC-04 | Cross-source entity resolution and identity ledger | Data steward: which records refer to the same organisation, site, product or substance? | Identifier, Entity, Mapping, Evidence, Provenance, confidence/status | precision/recall on gold subset, unresolved/ambiguous rate | **Cross-cutting evaluation candidate** |
| UC-05 | Regulatory/site compliance browser | Manufacturer/regulator: what authorisation/compliance evidence exists for a site and jurisdiction? | Site, Organization, GMP/GDP/MIA/WDA status, Authority, Inspection/Certificate, Time | coverage and provenance completeness | Application candidate |
| UC-06 | Clinical-trial sponsor/site/product network | Sponsor/researcher: how are sponsors, collaborators, trial facilities, interventions/products and countries connected? | Study, Sponsor, Collaborator, Site, Location, Intervention/Product | network coverage, cross-jurisdiction query set | Application / held-out evaluation candidate |
| UC-07 | Pharmacovigilance evidence integration | PV analyst: what safety evidence/signals relate to a product/substance and what is the provenance? | Product, Substance, Adverse Event, Report, Signal, Evidence, Source | evidence retrieval precision, provenance completeness | Application candidate |
| UC-08 | Essential-medicine access and availability analytics | Public-health/payer: where are important medicines available/affordable and how does status vary? | Essential/Critical Medicine, Availability, Price/Affordability, Facility, Region, Time | access indicator reproduction where data allow | Application candidate |
| UC-09 | Reimbursement/market-access comparison | Payer/researcher: how do reimbursement/access observations differ across regions/time/products? | Payer, Reimbursement Record/Decision, Product, Amount, Region, Time | coverage, trend/comparison queries | Application candidate |
| UC-10 | Provenance-aware semantic search | Researcher/regulator: answer ecosystem questions while showing source/evidence for each result. | Ontology entities/relations + Evidence/Provenance | answer correctness, citation/provenance coverage | Application candidate |
| UC-11 | Knowledge-graph-assisted demand forecasting | Supply/planning analyst: improve pharmaceutical demand prediction with relational context. | Product, Demand Observation, Time, substitution/condition context, KG relations | MAE/RMSE/MAPE vs non-KG baseline | Future research / AI candidate |
| UC-12 | Shortage prediction/classification | Regulator/MAH: predict shortage occurrence/duration/cause from integrated evidence. | Product, shortage history, MAH/site, availability, alternatives, time | AUROC/F1/MAE depending task | Future research / AI candidate |
| UC-13 | Safety-signal / ADR prediction | PV analyst: prioritize potential adverse relationships using integrated KG evidence. | Drug/Product/Substance, Target/Indication where used, Event/ADR, Evidence | AUROC/AUPRC, calibration, expert validation | Future research / AI candidate |
| UC-14 | Ecosystem anomaly detection | Data steward/regulator: detect unusual or inconsistent organization–site–product–authorisation patterns. | Typed entities/relations, temporal/provenance constraints | precision/recall on injected/known anomalies | Future research / AI candidate |
| UC-15 | Ontology↔RDB↔KG query equivalence | Researcher/developer: do equivalent semantic questions yield consistent results across representations? | Formal mappings, relational schema, RDF graph, identifiers | agreement rate across benchmark query suite | **Research evaluation demonstrator** |
| UC-16 | Regulatory-data compliance assistance | MAH/software provider: map reporting requirements to data entities and detect missing/invalid fields. | Requirement, Data Element, Product/Site/Org, Validation rule, Evidence | rule coverage, validation precision | Future application candidate |
| UC-17 | Crisis stockpile/alternative-supply planning | Preparedness authority: where should critical items or API capacity be diversified/stockpiled? | Critical Medicine, API/Substance, Site, Capacity, Geography, Dependency, Stockpile | scenario-based reduction in concentration/exposure | Future research / resilience candidate |
| UC-18 | Pharmaceutical ecosystem observatory | Multi-stakeholder: browse actors, products, sites, relationships, geography and provenance in one research interface. | Cross-domain Core + extensions | task completion, query correctness, provenance visibility | Application demonstrator candidate |

## Portfolio rule
A use case enters the principal V2 manuscript only when later waves establish:
1. admitted data sufficient for the task;
2. ontology dependence (not merely a generic database/dashboard task);
3. explicit evaluation metrics/baselines;
4. reproducibility and provenance;
5. a clear contribution to one or more V2 RQs.
