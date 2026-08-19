# W4 Events, Situations, Observations and Temporal Participation

## Core distinction
W4 explicitly separates:
1. **events/activities** — things that occur and unfold in time;
2. **situations/states** — configurations that obtain during an interval;
3. **observations** — evidence-producing events;
4. **observation results/assertions** — information objects produced or represented by sources.

This resolves several W3 discovery candidates that combined data records with domain phenomena.

## Event types
### Manufacturing Activity — `<<Event>>`
Participants may include Organization roles, Facility roles, Product/Presentation/Substance and relevant resources. A source establishment registration is evidence of authorization/role context; it is not by itself evidence that a specific manufacturing event occurred.

### Distribution / Logistics Activity — `<<Event>>`
Represents handling/storage/distribution/logistics activity. W4 does not infer a shipment event from a distributor registration alone.

### Procurement Activity — `<<Event>>` (Supply extension)
May involve buyer, provider, Product and Facility where conditional C1 evidence supports these participants.

### Disruption Event — `<<Event>>` (Resilience extension)
A temporally bounded occurrence capable of affecting a site, activity, dependency or Product availability.

### Risk Assessment Activity / Risk Treatment Activity — `<<Event>>`
Risk extension processes. A plan and its execution are distinct.

### Provenance Activity — `<<Event>>`
Covers ingestion, extraction, normalization, transformation and mapping processes that generate research artifacts/assertions.

### Adverse Event Reporting / Post-Market Surveillance — `<<Event>>`
Safety extension activities retained from V1 lineage.

## Situation types
### Medicine Shortage Situation — `<<Situation>>`
A shortage is modeled primarily as a configuration in which supply/availability for a medicine is insufficient relative to the relevant demand/expected availability under a source/jurisdiction/context during an interval.

Key reasons for `Situation` rather than `Event`:
- shortage data commonly describe an ongoing/resolved state over time;
- source records report that the situation obtains, rather than necessarily recording a single causal occurrence;
- a shortage may be initiated/resolved by events, but the shortage itself can persist after triggering events.

A `Source Record` and `Assertion` can describe a historical or current Shortage Situation. The ontology therefore distinguishes **the shortage in the world** from **the regulatory record about the shortage**.

### Stockout Situation — `<<Situation>>` (Supply/Resilience extension)
A local operational state in which required Product inventory at a Facility is unavailable/insufficient. It may be related to but is not identical with a regulatory Medicine Shortage Situation.

## Observation pattern
### Observation Activity — `<<Event>>`
An activity that measures, counts, assesses or otherwise determines a value/state about a domain entity/context.

### Observation Result — information-object `<<Kind>>`
The persistent information result produced/represented by an Observation Activity or ingested from a source when the observation event itself is not available.

Specializations:
- Availability Observation Result
- Demand Observation Result
- Supply Capacity Observation Result
- Inventory Observation Result
- Lead-Time Observation Result
- Reimbursement / Utilisation Observation Result

This pattern is deliberately compatible with aggregated datasets: a row reporting `patients_num`, package counts or expenditure can instantiate an Observation Result without creating nonexistent individual Patient instances.

### Measure Value — `<<Datatype>>`
Represents numeric/coded values and units/currency/count semantics attached to Observation Results or Qualities. It is not a domain entity.

## Supply capacity split
W3 `Supply Capacity Observation` is split into:
- `Supply Capacity <<Mode>>` — a disposition/capability inhering in an Organization or Facility;
- `Supply Capacity Observation Result` — evidence about that disposition at a time/context.

This prevents evidence from being conflated with the capability it measures.

## Strength split
`Strength <<Quality>>` characterizes a Product Presentation. Its measured/normative value is represented through a Measure Value. This is preferable to modeling strength as a freestanding business object or identifier.

## Temporal modeling
The W4 conceptual model uses:
- `Time Interval <<Datatype>>` for validity/extent;
- `Reporting Period <<Datatype>>` for source-defined aggregation periods;
- event participation relations for who/what participates in an Event;
- validity/context relations on Relators such as Authorization, Registration, Identifier Assignment and Market Listing.

### Important constraint
A source status such as `ongoing`, `resolved`, `active` or `inactive` is **not automatically a `<<Phase>>`**. OntoUML phases require intrinsic anti-rigid classification and a disjoint/complete partition. Source vocabularies are often incomplete, jurisdiction-specific or relational, so W4 keeps status values as controlled values unless a true phase partition is demonstrated later.

## Causal boundary
W4 does not infer causality from co-occurrence. A Disruption Event may `affect` a Shortage Situation or Supply Dependency when evidence supports it, but a shortage record alone does not establish the cause of shortage.

## W5 handoff
Formalization should encode event participation, situation involvement, temporal validity and observation-result provenance without forcing every temporal source field into an OWL class. SHACL can later validate required time/source/context fields for empirical instances.
