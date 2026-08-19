# W3 → W4 Conceptual Transformation Ledger

## Purpose
Make every material change between evidence discovery (W3) and foundational conceptualization (W4) auditable. W4 is allowed to split/merge/reclassify candidates; this ledger prevents those changes from appearing arbitrary.

## Summary
- W3 normalized candidates: **80**.
- W4 named conceptual types/pattern elements: **87**.
- W3 deferred and still excluded from Gate D: **2**.
- Net increase results from required semantic splits/truth-makers, not uncontrolled scope expansion.

## Major transformations
| W3 candidate | W4 transformation | Reason |
|---|---|---|
| Ecosystem Participant Role | → Ecosystem Participant `<<RoleMixin>>` | Bearers include Organization and Facility with different identity providers. |
| Site / Facility | → Facility `<<Kind>>`; `Site` retained as source synonym | Prevent physical site/location/organization ambiguity. |
| Establishment Registration | → Registration `<<Relator>>` + source record evidence | Separate real regulatory relation from record/document. |
| Regulatory Authorization / License | → Authorization `<<Relator>>` + identifier/document evidence | License document/number is not the authorization's identity. |
| Product Classification | → Classification Scheme + Classification Entry + Assignment Relator | Separate classification vocabulary from contextual assignment. |
| Product Listing / Marketing Status | → Market Listing Relator + status value | Listing is jurisdiction/source/time dependent, not intrinsic Product phase. |
| Strength / Concentration Specification | → Strength `<<Quality>>` + Measure Value | Ground quantitative characteristic in its Product Presentation bearer. |
| Medicine Shortage Case | → Medicine Shortage Situation + Source Record/Assertion | Separate domain situation from regulatory record about it. |
| Shortage Status | → controlled status value | Avoid unjustified complete/disjoint Phase partition. |
| Observation | → Observation Activity `<<Event>>` + Observation Result information object | Separate evidence-production occurrence from persistent result. |
| Availability Observation | → Availability Observation Result | Dataset/regulatory evidence predominantly represents result. |
| Demand Observation | → Demand Observation Result | Same rationale; aggregate data do not imply individual demand events. |
| Supply Capacity Observation | → Supply Capacity `<<Mode>>` + Supply Capacity Observation Result | Distinguish capability/disposition from evidence about it. |
| Data Source | → Data Source Resource | Remove conflation of publisher organization, system and resource identity. |
| Evidence Item | → Evidence Item `<<RoleMixin>>` + Evidence Support `<<Relator>>` | Many information objects can contextually serve as evidence. |
| Identifier | → Identifier Value `<<Datatype>>` | Identifier string is not entity identity. |
| Identifier Assignment | retained as `<<Relator>>` | Makes scheme/source/time context explicit. |
| Mapping Assertion | → Assertion Subkind | Mapping is a proposition, not the relation's truth-maker. |
| Entity Match Assertion | → Assertion Subkind + Match Confidence Quality | Separate proposition, evidence and confidence. |
| Essential Medicine Classification | → Relator Subkind | Essentiality is list/context/jurisdiction dependent. |
| Critical Medicine Classification | → Relator Subkind | Criticality is context dependent. |
| Alternative Medicinal Product Role | → Product Role + Alternative Assignment Relator | Alternative status is anti-rigid and relational. |
| Supply Dependency | → `<<Relator>>` | Objectifies domain dependency relation without claiming complete network data. |
| Stockout Event / Situation | → Stockout Situation | Available evidence primarily supports state/configuration; transition event optional. |
| Risk Assessment | → Risk Assessment Activity | Assessment occurrence is an Event; results are Assertions. |
| Risk Treatment / Mitigation | → Risk Treatment Plan + Risk Treatment Activity | Intent/planning and execution are distinct entities. |
| Business Architecture View | retained as information object | Explicit analytical layer, not domain identity. |
| Enterprise Capability | → `<<Mode>>` | Organizational capability is an intrinsic disposition. |
| Clinical Care Participant Role | → `<<RoleMixin>>` | Future clinical bearers may follow different identity principles. |

## New W4 truth-makers/helpers
| New element | Justification |
|---|---|
| Facility Operation `<<Relator>>` | Grounds Organization↔Facility operation without false mereology. |
| Classification Entry | Needed so a Scheme and its entries are not conflated. |
| Contextual Medicine Classification Assignment | Common parent for Essential/Critical assignment semantics. |
| Alternative Medicine Assignment `<<Relator>>` | Grounds Alternative Product Role. |
| Evidence Support `<<Relator>>` | Grounds evidence role/support relation. |
| Observation Result | Parent for all persistent evidence results. |
| Asset-at-Risk `<<RoleMixin>>` | Minimal adapter to external risk-reference semantics. |

## W3 items intentionally not promoted
- Clinical Care Pathway / Activity Pattern — deferred.
- Public–Private Partnership Arrangement — deferred.
- generic Ecosystem Relationship — replaced by typed patterns.
- generic Supply Chain Relationship — replaced by typed participation/dependency/procurement patterns.
- Blockchain-Based Supply Chain Ledger — implementation option, not domain semantics.
- AI-CDSS, EHR, Telemedicine and RWE platform — application specializations, not Core.

## Continuity vs novelty
Retained concepts such as Organization/roles, regulatory concern, supply/demand concern and activity modeling are predecessor lineage and must not be presented as new by themselves. V2 novelty is carried by the evidence-grounded restructuring, product/site/jurisdiction layers, contextual classifications, situation/observation separation, provenance/identifier infrastructure, modular BA/risk design and later empirical/formal evaluation.

## Gate D rule
After Gate D, changes to these identity/stereotype decisions require a recorded design change. Source-specific mappings may adapt without reopening the conceptual model as long as they do not contradict the frozen identity/dependence commitments.
