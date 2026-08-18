# W1 Geospatial Intelligence, Resilience and Risk-Alignment Design

## 1. Geospatial intelligence as a cross-cutting semantic concern
Geography is not modeled as an isolated business domain. It cuts across organizations, sites/facilities, trials, authorisations, supply relationships, shortages, access observations, logistics, and risk.

### Candidate geospatial distinctions for W3/W4 discovery
- **Organization** — legal/institutional actor; not equivalent to a physical location.
- **Site / Facility** — physical operational site belonging to or used by an organization.
- **Geospatial Position** — coordinates or geometry associated with a site/place where available.
- **Administrative Region / Country** — geographic region used for aggregation.
- **Regulatory Jurisdiction** — authority/legal scope; may overlap geography but is not identical to physical location.
- **Service / Distribution Area** — area served by a provider/distributor where evidence supports it.
- **Route / Corridor** — logistics path, deferred unless usable route data are admitted.
- **Geographic Observation** — observation whose value/status is valid for a region and time.

### Evidence-grounded use cases
1. Global manufacturer/API/site map using official establishment/site records.
2. Trial-site geography and sponsor/facility network.
3. Geographic concentration of manufacturing or critical-medicine evidence.
4. Regional shortage/access variation.
5. Exposure analysis: which products/actors depend on sites in a selected region?
6. Cross-jurisdiction comparison of product/site/regulatory status.
7. Crisis analysis: disruption of a region/site and downstream dependency reach.

### Data/source signals identified in W1
- EudraGMDP exposes site name, city, country, postcode and OMS location/organization identifiers together with manufacturing/import/GMP/GDP evidence (W1-S05).
- FDA establishment registration/listing provides a U.S. establishment/product infrastructure (W1-S02).
- ClinicalTrials.gov exposes facility and location fields including city/state/ZIP/country and sponsor/collaborator structures (W1-S06).

## 2. Resilience and disruption use cases

| ID | Scenario | Main question | Required data/semantics | Candidate analysis |
|---|---|---|---|---|
| RES-01 | Manufacturing-site disruption | Which medicines/actors are exposed if a manufacturing site becomes unavailable? | Product↔Site, manufacturing role, geography, alternative site | dependency reach / alternative path |
| RES-02 | Supplier/API disruption | Which products depend on a supplier/substance source and are alternatives available? | Product, substance/API, supplier, supply relation, alternative | concentration and path analysis |
| RES-03 | Geographic shock | Which critical medicines have excessive dependency on one region/country? | Critical medicine, site/supplier geography, dependency | regional concentration / exposure |
| RES-04 | Demand surge / public-health emergency | Which medicine supply relationships are most vulnerable under increased demand? | demand/availability observations, criticality, supply actors, time | scenario-based stress query |
| RES-05 | Quality/GMP disruption | How can a site compliance/non-compliance event propagate to product availability? | Site, compliance evidence/event, product/site link, shortage/availability | event-to-dependency analysis |
| RES-06 | Logistics interruption | What product/site/region dependencies rely on a distribution route or provider? | logistics actor, shipment/route where data exist | network/path analysis; deferred if route data unavailable |
| RES-07 | Stockpile/alternative-supply planning | Which alternative sites/products/suppliers could reduce concentration? | criticality, alternatives, capacity/availability where available | counterfactual scenario ranking |

### Evidence boundary
FDA and EMA identify manufacturing/quality problems, production delays, raw-material issues, supply/demand monitoring and supply-chain vulnerabilities as real shortage/preparedness concerns (W1-S01, S03, S04). W1 therefore justifies resilience as a high-value application/evaluation family. It does not justify a complete quantitative supply-chain model until W2 confirms usable relational data.

## 3. Relationship to generic Risk Ontology research

### Verified current situation
No separate user-owned risk-ontology repository or frozen model baseline was verified during W1. Earlier CM-PharmE work identified risk/governance as future ontology-driven research. Therefore, W1 must not claim that an existing proprietary/user risk ontology has already been integrated.

### Recommended architecture
**CM-PharmE Core** models pharmaceutical facts:
- products/substances;
- organizations, roles and sites;
- activities/events;
- supply/dependency relations;
- geography/jurisdiction;
- regulatory evidence;
- provenance/evidence.

**Risk & Resilience Extension** specializes/aligned generic risk concepts to pharmaceutical ecosystem situations, such as:
- Asset/Value at Risk;
- Vulnerability;
- Hazard/Threat/Disruption Event;
- Loss/Adverse Consequence;
- Risk Subject / Assessor;
- Risk Assessment;
- Prevention / Mitigation / Treatment;
- Recovery / resilience-oriented concepts where justified.

### Reuse strategy
Do not invent generic risk semantics inside the pharmaceutical Core. W4 should evaluate alignment with UFO-grounded reference work such as **COVER** (Common Ontology of Value and Risk), the UFO-based prevention module, and **ROSE** (Reference Ontology for Security Engineering) only for concepts/patterns that are substantively applicable. The relationship is mapping/reuse first; import is decided later based on modularity, licensing, OWL/OntoUML availability, and semantic fit.

### Why this separation matters
1. Keeps the pharmaceutical Core domain-focused and stable.
2. Supports reuse of mature risk concepts across projects.
3. Avoids conflating a pharmaceutical dependency with a risk before a risk subject, value, vulnerability and adverse-event context are defined.
4. Enables a separate risk/resilience paper if the extension becomes substantial.
5. Preserves Business Architecture as an optional view rather than forcing risk semantics through BA constructs.

## W1 decision proposal
- **Geospatial semantics:** Core/cross-cutting requirement — proceed.
- **Resilience:** primary research demonstrator candidate — proceed conditionally on W2 data feasibility.
- **Generic risk ontology:** modular alignment/reuse — proceed in W4; do not duplicate into Core.
- **Dedicated Pharmaceutical Risk Ontology:** defer as a possible extension/follow-on research output until concept/data evidence demonstrates enough scope for a separate ontology.
