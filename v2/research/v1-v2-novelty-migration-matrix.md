# CM-PharmE 1.x → 2.0 Novelty and Migration Matrix

## Purpose
Maintain an explicit audit trail between the reviewer-facing CM-PharmE 1.x baseline and CM-PharmE 2.0 so that novelty, retained foundations, refinements, deprecations, and new evidence can be demonstrated rather than asserted.

## Migration statuses
- **Retained** — concept or relation preserved without semantic change.
- **Refined** — meaning retained but definition, stereotype, relation semantics, or constraints improved.
- **Renamed** — same intended concept with clearer terminology.
- **Split** — one v1 construct separated into multiple semantically distinct constructs.
- **Merged** — multiple v1 constructs unified under one better-supported concept.
- **Moved to extension** — no longer part of the Core but retained in an optional module/view.
- **Deprecated** — removed from the active model with rationale.
- **New** — introduced from new literature, datasets, standards, use cases, or expert evidence.
- **Deferred** — candidate retained in backlog pending stronger evidence.

## Initial architectural migration decisions
| V1 element | V2 treatment | Rationale |
|---|---|---|
| Five-domain architecture | Refined / not automatically preserved as the V2 Core decomposition | V2 domains/modules must emerge from evidence and UFO/OntoUML analysis rather than remain fixed by inheritance. |
| Business-architecture-informed identity | Moved to extension/view | Business Architecture remains useful for analytical mapping but no longer defines the Core ontology identity. |
| UFO grounding | Retained and strengthened | UFO becomes first-class in the prospective conceptualization protocol. |
| OntoUML model | Retained and strengthened | OntoUML becomes a first-class artifact with explicit decision records and semantic review. |
| OWL implementation | Retained and strengthened | V2 targets OWL 2 DL as a hard formal gate. |
| Scenario-only data evidence | Replaced by data-grounded evidence | V2 requires real DOI-backed and authoritative datasets, with held-out evaluation. |
| Repository-supported evaluation | Retained and expanded | V2 predefines evaluation families prospectively and adds data, cross-representation, generalizability, expert, and application evaluation. |
| Risk Management Activity | Candidate for Risk/Resilience Extension | Reusable risk semantics should be aligned with the separate risk-ontology research rather than duplicated in the Core. |
| Reference-architecture applications | Retained as optional analytical/application view | Application value remains important but is separated from Core ontological commitments. |

## Concept-level matrix
This section is intentionally empty at W0. It will be populated during W3 after dataset/schema discovery. Every v1 concept and relation will receive one migration status and supporting evidence.
