# W4 Geography, Facility and Regulatory-Jurisdiction Conceptualization

## Central distinction
W4 freezes four different semantic layers that were frequently conflated in source data:

1. **Organization** — social/legal/institutional entity.
2. **Facility** — physical operational functional complex.
3. **Geographic entity/value** — place/region/position/address representation.
4. **Regulatory Jurisdiction** — social/legal scope of authority and rule applicability.

A single source record may contain fields for all four, but they do not share identity.

## Organization vs Facility
`Organization <<Kind>>` provides identity for companies, authorities, hospitals or other institutional entities.

`Facility <<Kind>>` provides identity for a physical operational site. A Facility may continue to exist while its operator, license or role changes. Conversely, an Organization may operate multiple Facilities.

### Operation pattern
`Facility Operation <<Relator>>` mediates Organization and Facility. This grounds the derived material relation `operates` and avoids treating Facility as a mereological component of Organization.

## Facility roles
`Manufacturing Site Role <<Role>>` and `Distribution Site Role <<Role>>` are anti-rigid roles of Facility. A physical site can enter or leave these regulated/operational contexts without losing Facility identity.

The W4 model does not create a rigid `Manufacturing Facility` Kind unless later evidence demonstrates that manufacturing is essential to the identity of the physical entity. Current regulatory evidence instead supports role/context semantics.

## Geographic entities
`Geographic Feature <<Kind>>` is the identity provider for named geographic/place entities used in normalization.

Rigid specializations:
- `Administrative Region <<Subkind>>`
- `Country <<Subkind>>`

W4 does not assert that every Country is an Administrative Region or vice versa; both specialize Geographic Feature and can be linked by an `administrativelyWithin` formal relation.

## Geospatial values
- `Geospatial Position <<Datatype>>` — coordinate/geometry value.
- `Address <<Datatype>>` — structured postal/location descriptor.

These values can characterize Facility or Geographic Feature, but they are not identity providers.

GeoNames remains a **normalization/reference source**. A GeoNames identifier assignment can support cross-source resolution, but the presence of a GeoNames ID does not determine pharmaceutical-domain identity.

## Regulatory Jurisdiction
`Regulatory Jurisdiction <<Kind>>` represents a legal/social scope in which regulatory authority, requirements, registrations, authorizations or classification assignments apply.

It may have a formal relation such as `hasGeographicScope` to Country/Administrative Region/Geographic Feature, but it is not reducible to that geography.

Examples of why the distinction matters:
- a regulator may exercise authority over a geographic territory for a subset of products/activities;
- a medicine may be critical in one jurisdiction and not another;
- authorization validity may depend on legal scope even when facilities are physically located elsewhere;
- source-country fields are not enough to infer jurisdictional applicability.

## Core relations
- `Facility Operation` mediates Organization ↔ Facility.
- `locatedIn(Facility, GeographicFeature)` — formal/spatial relation.
- `hasPosition(Facility|GeographicFeature, GeospatialPosition)` — value relation.
- `hasAddress(Organization|Facility, Address)` — value relation.
- `administrativelyWithin(AdministrativeRegion, Country)` — formal administrative-containment relation.
- `hasGeographicScope(RegulatoryJurisdiction, GeographicFeature)` — social-to-geographic scope relation.
- `exercisesAuthorityIn(RegulatoryAuthorityRole, RegulatoryJurisdiction)` — role-context relation.
- Authorization/Registration/Classification Relators reference Jurisdiction as contextual participant/scope.

## Mereology decision
W4 intentionally avoids using `<<ComponentOf>>` for Organization↔Facility and avoids asserting that administrative geography is a functional-complex component hierarchy. OntoUML componentOf is reserved for functional complexes; the available evidence here supports operation and administrative/spatial containment, not functional mereology.

## Gate B demonstrator A support
This conceptualization directly supports the Global Actor/Facility Geospatial Integration demonstrator because it allows a record to answer separately:
- which Organization is involved?
- which physical Facility is involved?
- where is it located?
- which operational/regulatory role does it bear?
- which Jurisdiction applies?
- which source/identifier supports each assertion?

## W5 handoff
Formal OWL should keep Organization, Facility, Geographic Feature and Regulatory Jurisdiction disjoint unless a later justified abstraction explicitly generalizes them. SHACL should validate source mappings without using address/country identifiers as ontology identity axioms.
