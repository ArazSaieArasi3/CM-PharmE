# W2 Domain Source Profiles

## 1. Geospatial actors and facilities
### Strong sources
- **FDA DECRS** — drug establishments; public ZIP; appropriate for U.S. manufacturer/establishment/site identity.
- **FDA WDD/3PL reporting** — facility-level wholesale distributor and third-party logistics roles; useful to distinguish logistics/trading facilities from registered manufacturing establishments.
- **EMA EudraGMDP** — manufacturing/import/GMP/GDP/wholesale/active-substance role and site evidence; strong semantic source, but automated bulk ingestion remains conditional.
- **NHIF inpatient dataset D02** — hospitals/facilities plus product/region/time; directly ingestible DOI-backed empirical data.
- **GeoNames G01** — geographic normalization with stable geoname IDs and WGS84 coordinates where matching succeeds.

### Held-out
- **ClinicalTrials.gov/AACT** — global trial facilities, sponsor/collaborator and location relations; reserved for W7 generalizability.

### W3 discovery implications
Candidate distinctions to test include Organization, Establishment/Site/Facility, Facility Role, Location, Administrative Region, Regulatory Jurisdiction, Registration/Authorisation Status and provenance-bearing identifiers. Do not pre-admit them solely from this profile.

## 2. Medicinal product and substance
### Strong sources
- **NHIF D01/D02** — marketed product, ATC/INN, packaging/concentration and reimbursement codes.
- **openFDA NDC O03** — marketed drug/product/package identifier structure, ingredients, form/route and harmonized identifiers.
- **FDA SPL O04** — product labeling and product/facility information.
- **WHO essential medicines O10** — essentiality, formulations and medicine-selection context.
- **ChEMBL O15** — substance/compound identity enrichment.

### W3 discovery implications
Explicitly distinguish Substance/Active Ingredient, Medicinal Product, Marketed/Branded Product, Dosage/Formulation, Strength/Concentration, Package and Identifier. Exact ontological treatment is deferred to UFO/OntoUML analysis.

## 3. Manufacturing, supplier and logistics
### Strong sources
- **FDA DECRS O01** — manufacturing/processing establishments.
- **FDA WDD/3PL O02** — wholesale/3PL facility roles.
- **EudraGMDP O08** — MIA/GMP/GDP/wholesale/active-substance roles.
- **D04 conditional supply dataset** — actual consumption, procurement, lead-time, arrivals, stock/inventory and operational-event relationships.

### Data gap identified
Public regulatory registries are strong for actor/site/authorization semantics but often do **not** expose complete product-level supplier→buyer→shipment networks. D04 is much richer operationally but licensing is conditional. Therefore, V2 should not claim complete global supply-network reconstruction unless W6 later obtains legally reusable relationship data.

## 4. Shortage, criticality and resilience
### Discovery sources
- **EMA Union List of Critical Medicines O06** — criticality and alternatives context.
- **EMA shortages JSON O07** — shortage status, product/substance/form/strength, alternatives and dates.
- **EMA vulnerability methodology** — methodological evidence for supply-chain vulnerability concepts; not an empirical dataset.
- **D04 conditional supply dataset** — operational inventory/lead-time/stockout evidence.

### Held-out
- **openFDA Drug Shortages O05** — reserve U.S. shortage data for external/cross-jurisdiction evaluation.

### W3/W7 implication
The ontology should represent observed shortage/availability/criticality situations and dependencies without assuming that every regulatory definition is universally identical. Held-out U.S. data can test whether EU-derived semantics generalize.

## 5. Clinical trial and pharmacovigilance
### Held-out / extension sources
- **ClinicalTrials.gov/AACT O12/O13** — sponsor, collaborator, trial facility, intervention/product and geography.
- **openFDA FAERS O14** — safety-report extension data, not causal evidence.

### Rationale
These sources are intentionally not primary Core-discovery sources. They test whether a pharmaceutical-ecosystem Core can accommodate additional stakeholder, role, facility and evidence structures without having been built around the trial/safety schemas.

## 6. Market access, reimbursement and finance
### Strong sources
- **D01 outpatient NHIF** — region/product/diagnosis/patient/package/reimbursement/time.
- **D02 inpatient NHIF** — hospital/product/diagnosis/patient/expenditure/time.
- **D03 individually approved medicines** — exception-based access/funding process.
- **WHO essential medicines/national lists** — policy/essentiality/access context rather than transactional reimbursement.

### Finance boundary
D04 contains procurement-cost and finance-related operational files, but this does not establish a complete pharmaceutical-financing domain. Financing actors/arrangements remain extension candidates until broader evidence is found.

## 7. Cross-source identity and entity-resolution opportunity
Potential overlap exists through:
- ATC/INN/product names across NHIF, WHO and other medicine sources;
- NDC/SPL/harmonized identifiers across openFDA sources;
- organization/site names and addresses across FDA facility sources;
- sponsor/facility names in held-out ClinicalTrials.gov/AACT;
- EMA OMS identifiers within EudraGMDP where accessible.

W2 does not yet guarantee a gold standard. W6/W7 may promote entity resolution to a measured AI component only after an explicit overlapping-record sample can be curated with defensible same-entity judgments.

## Overall profile conclusion
The candidate portfolio is sufficiently diverse for broad concept/relation discovery without forcing the V2 Core to mirror one operational schema. The key limitation remains public, product-level supply-chain relationship data: this area needs cautious claims and may rely on conditional research data plus regulatory vulnerability/shortage evidence rather than a complete global transaction network.
