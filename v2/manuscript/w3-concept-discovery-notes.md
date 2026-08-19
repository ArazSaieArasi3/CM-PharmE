# W3 Manuscript Notes — Evidence-Driven Concept and Relation Discovery

Status: working manuscript material; candidate concepts are pre-UFO and not final ontology results.

## Research-design narrative supported after W3
CM-PharmE 2.0 uses a staged concept-discovery protocol in which the frozen CM-PharmE 1.x inventory is treated as prior conceptual evidence rather than as a mandatory ontology skeleton. The discovery corpus is defined prospectively through Gate C source roles and combines DOI-backed empirical datasets with authoritative regulatory/reference sources. Protected held-out source families are excluded from Core concept admission before external/generalizability evaluation.

The discovery procedure distinguishes source fields from domain semantics. Columns, API fields and record types are first interpreted as candidate entities, roles, events/situations, observations, classifications, identifiers, measures or relationship structures. Synonymous/source-specific labels are then normalized before any UFO/OntoUML stereotype is assigned.

## Principal W3 discovery result
The strongest evidence-backed V2 semantic backbone differs materially from the V1 business-architecture-centered organization:

**Organization and contextual roles → physical Site/Facility → Regulatory/Jurisdiction context → Medicinal Product/Substance/Presentation → Geography/Time → Shortage/Availability/Demand/Supply observations → Evidence/Provenance/Identifier infrastructure.**

This structure is supported by the admitted W2 discovery sources and by the needs/use cases established in W1. It does not depend on protected held-out schemas.

## Pre-UFO inventory
W3 normalizes **80 candidate concepts** and **80 candidate relationship semantics**. The current admission distribution is:
- 29 Core candidates;
- 23 cross-cutting infrastructure candidates;
- 26 modular extension candidates;
- 2 deferred candidates.

These numbers must be described as a **discovery inventory**, not the final ontology class/property count. W4 may merge, split, reclassify or reject candidates after foundational analysis.

## Material V1→V2 changes that may support later novelty claims
Subject to W4–W7 evidence, the following changes are already traceable as design evolution rather than rhetorical repositioning:
1. Business Architecture becomes an optional analytical extension rather than the Core decomposition principle.
2. Pharmaceutical Enterprise is generalized to Organization plus contextual pharmaceutical roles.
3. Organization and physical Site/Facility are explicitly distinguished.
4. A product/material layer distinguishes Medicinal Product, Pharmaceutical Substance, Presentation, Dosage Form, Strength and Package.
5. Essential/Critical medicine semantics are contextual list/jurisdiction/version classifications rather than intrinsic permanent kinds.
6. Shortage, availability, demand and supply are modeled through time/source/context-sensitive cases/observations instead of generic static signals.
7. Provenance, identifiers, mapping assertions and entity-match evidence become first-class cross-representation infrastructure.
8. Generic ecosystem/supply-chain relationships are replaced by typed candidate relations.
9. Detailed risk, safety, market access, clinical care, digital-health and BA concepts are modular rather than forced into Core.

These are **candidate novelty components**, not final contribution claims until W4–W7 implementation/evaluation is complete.

## Methodological anti-circularity statement
The protected held-out source families are known to exist and were screened for feasibility in W2, but W3 did not mine their schemas to admit Core concepts/relations:
- ClinicalTrials.gov/AACT;
- openFDA Drug Shortages;
- selected national Essential Medicines List schemas.

Later W7 evaluation can therefore test whether the independently derived Core accommodates those structures without claiming a fully blind test.

## Important negative findings to preserve
- Current public data do not support a completeness claim for a global transaction-level Product→Supplier→Buyer→Shipment graph.
- Financing/counterparty concepts remain outside Core because W2/W3 evidence is insufficient.
- Detailed procurement, lead-time, inventory and stockout semantics rely heavily on conditional C1 and therefore remain extension-level.
- Aggregate NHIF patient counts are measures, not evidence for individual Patient instances.
- Technology-specific V1 concepts (e.g., blockchain ledger, AI-CDSS) are application options, not durable Core ontology classes.

## W4 handoff language
The W3 inventory answers **what semantic distinctions require modeling and what evidence supports them**. W4 will answer **how those distinctions should be ontologically characterized under UFO/OntoUML**, including identity, rigidity, dependence, role/relator structure, event/situation distinctions, part-whole relations and cardinality rationale.

## Manuscript sections that may now be drafted incrementally
- Research Design: source-role separation, held-out boundary, concept-admission protocol.
- Concept Discovery: source-schema interpretation, normalization, migration and traceability procedure.
- V1→V2 Evolution: explicit migration categories and evidence-backed changes.

Do not yet write final results for OntoUML stereotypes, OWL 2 DL, RDB/KG mappings, held-out coverage, expert validation or application performance.
