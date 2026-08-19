# W3 Geospatial, Temporal and Jurisdiction Concept Discovery

## Design problem
Pharmaceutical sources routinely mix legal actors, physical facilities, postal locations, administrative regions and regulatory scopes. CM-PharmE 2.0 must keep these semantics separate so that geospatial analysis does not silently convert an organization into a place or a jurisdiction into a coordinate.

## 1. Required distinctions

### Organization vs Site/Facility
- **Organization**: institutional/legal/social bearer of roles.
- **Site/Facility**: physical operational location at which activities may occur or registrations/licenses may apply.
- A single organization may operate multiple sites.
- A site may bear multiple contextual roles/licenses.
- FDA WDD/3PL evidence that one facility may have multiple licenses is direct support for keeping `Facility`, `License`, and `Role` distinct.

### Geographic Feature vs Administrative Region vs Country
- **Geographic Feature** provides place identity.
- **Administrative Region** provides a hierarchical reporting/administrative unit.
- **Country** provides country-level geographic/political reference.
- GeoNames identifiers/coordinates are normalization evidence, not pharmaceutical identity.

### Regulatory Jurisdiction vs Geography
`Regulatory Jurisdiction` is a social/legal scope. It can correspond to a country, supranational area, or other legal scope, but it is **not identical** to a physical geographic feature. For example, an EU-level critical-medicine classification has a jurisdiction/policy context different from the coordinates of any site.

### Address vs Geospatial Position
- **Address** is a structured information description.
- **Geospatial Position** is a coordinate/geometry representation.
- Both may describe the same Site/Facility but have different identity/quality semantics.

## 2. Core geospatial candidates
| Candidate | Evidence | Main relations | Admission |
|---|---|---|---|
| Site / Facility | P2, P3, C2 | operatedBy Organization; locatedIn Geographic Feature; bearsRole | CORE |
| Geographic Feature | P7/native source locations | contains/isContainedIn; hasPosition; hasIdentifier | X-INFRA |
| Administrative Region | P1, P2, P7 | within Country; scopeOf Observation | X-INFRA |
| Country | P3/P5/P7 | contains Region; may ground Jurisdiction mapping | X-INFRA |
| Geospatial Position | P7 | describes Feature/Site | X-INFRA |
| Address | P3/C2 | describes Site/Organization | X-INFRA |
| Regulatory Jurisdiction | P3/P5/P6/C2 | appliesTo Authorization/Classification/Requirement; covers scope | CORE |

## 3. Temporal candidates
| Candidate | Source signal | Why needed |
|---|---|---|
| Time Interval | shortage start/resolution; registration/license validity; observation spans | Avoid treating changing statuses as permanent qualities. |
| Reporting Period | P1/P2 monthly/part reporting; ESMP reporting | Connect aggregate observations to their period. |
| Publication/Update Time | EMA shortage first-published/last-updated; dataset release dates | Provenance and change tracking. |
| Validity Interval | license/registration/classification/list validity | Distinguish validity from record publication time. |
| Event Time | manufacturing/procurement/disruption/stockout activities | Event semantics. |

`Time Instant` is not separately admitted in the candidate class inventory because W4/W5 may reuse a standard temporal pattern/OWL-Time rather than create project-specific time classes. W3 records the semantic requirement without over-populating the domain Core.

## 4. Jurisdiction-sensitive semantics
The following candidates **must carry jurisdiction/list/source context** where applicable:
- Regulatory Authorization / License.
- Regulatory Requirement.
- Product Listing / Marketing Status.
- Critical Medicine Classification.
- Essential Medicine Classification.
- Medicine Shortage Case/Status.
- Reimbursement/Access Observation.
- Organization/Site regulatory role where licensing is jurisdiction-specific.

## 5. Geospatial demonstrator A requirements
The approved geospatial demonstrator should eventually be able to answer reproducible questions such as:
1. Which pharmaceutical organizations and facilities are represented in a selected country/region?
2. Which roles does a facility bear under which license/registration evidence?
3. Which regulatory source supports each facility/role assertion?
4. Which medicinal-product observations or activities are linked to a facility or region?
5. Which records from different sources plausibly refer to the same facility/organization?
6. What geographic concentration is observed for a selected actor/product/context?
7. Does the model represent held-out trial facilities without having mined the ClinicalTrials.gov/AACT schema during W3?

## 6. PostGIS alignment requirements for W6
The ontology should permit an RDB/PostGIS realization that keeps at minimum:
- canonical entity identifier;
- organization table/object;
- site/facility table/object;
- address and normalized place relation;
- geometry/coordinates where legally and technically available;
- jurisdiction relation;
- source/record provenance;
- validity interval;
- entity-resolution/mapping status.

The relational design must preserve ontology distinctions rather than flatten `Organization`, `Site`, `Address`, `Place` and `Jurisdiction` into one “location” column.

## 7. Held-out boundary
ClinicalTrials.gov/AACT is known to contain global facility/location structures from W2 feasibility work, but W3 does not inspect its tables/fields to invent additional Core geospatial concepts. W7 will test whether the independently derived Organization–Site–Location–Jurisdiction framework can accommodate that family.

## Conclusion
W3 admits geography and time as **cross-cutting semantic infrastructure**, while `Regulatory Jurisdiction` belongs in the pharmaceutical Core because regulatory roles, authorizations, criticality and shortage interpretations depend on it. This separation is essential for global mapping, cross-jurisdiction evaluation and resilience analysis.
