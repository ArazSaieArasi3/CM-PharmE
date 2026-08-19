# W4 OntoUML Anti-pattern and Semantic Design Review

## Review status
**Manual/static semantic review: PASS with bounded residual items.**

This W4 review was performed against the OntoUML specification and anti-pattern catalogue. It is not presented as an automated OntoUML-tool execution. Automated/model-parser validation belongs to later implementation/evaluation work when a machine-readable OntoUML model is frozen.

Reference catalogue: https://ontouml.readthedocs.io/en/latest/

## Review checklist and result
| Review concern | W4 check | Result | Refactoring / disposition |
|---|---|---|---|
| Missing identity provider for Roles | All concrete Organization roles inherit Organization; Facility roles inherit Facility. | PASS | `Ecosystem Participant` changed to RoleMixin rather than forcing one identity. |
| Free Role | Roles must be grounded in authorization, listing, operation, classification, alternative or other relational contexts. | PASS / formal mediation to encode W5 | W5 must preserve non-zero relational dependency constraints. |
| Role vs Kind confusion | Manufacturer, Importer, Distributor, 3PL, Authority and Site roles are anti-rigid. | PASS | No separate Manufacturer/Distributor Kinds created. |
| Phase vs Role confusion | Source statuses are not modeled as Phases merely because they change over time. | PASS | Status retained as controlled values unless a complete intrinsic partition is later justified. |
| Dependent Phase anti-pattern | No W4 Phase is mediated as if it were a Role. | PASS | W4 currently avoids Phase stereotypes for source-defined statuses. |
| Relator without sufficient mediations | Facility Operation, Registration, Authorization, Classification Assignment, Market Listing, Identifier Assignment, Evidence Support, Supply Dependency and Partnership patterns all require >=2 mediated participants. | PASS conceptually | Exact cardinalities deferred to W5. |
| Material relation without truth-maker | `operates`, `isAuthorizedFor`, `isRegisteredWith`, contextual classification and alternative relations have explicit Relator patterns. | PASS | W5 may expose derived material properties for query convenience. |
| Over-reification | Mapping/Match Assertions are propositions, not Relators; spatial/reference relations are not automatically reified. | PASS | Keeps evidence claims separate from domain truth-makers. |
| Organization–Facility conflation | Distinct Kinds; operation is Relator/material relation. | PASS | `componentOf` explicitly rejected here. |
| Facility–Location conflation | Facility Kind separated from Geographic Feature and position/address values. | PASS | Geospatial identifiers remain infrastructure. |
| Geography–Jurisdiction conflation | Regulatory Jurisdiction modeled as social/legal Kind with geographic scope relation. | PASS | No country=jurisdiction equivalence. |
| Product–Substance conflation | Separate Kinds. | PASS | Active-substance relation does not define Product identity. |
| Product–Presentation conflation | Separate Kinds with presentation-of relation. | PASS | Supports multiple presentations per product. |
| Identifier as identity principle | Identifier Value is Datatype; assignment is Relator. | PASS | Scheme/source/time preserved. |
| Classification as product identity | Scheme/Entry/Assignment separated. | PASS | ATC/critical/essential classifications cannot substitute Product identity. |
| Contextual classification made rigid | Essential/Critical classifications are Relator subkinds, not Product Subkinds. | PASS | Jurisdiction/list/version context required. |
| Observation vs observed phenomenon | Observation Activity and Result separated; shortage/capacity remain domain phenomena. | PASS | Dataset rows may represent results without inventing observation events. |
| Capacity vs observation | Supply Capacity Mode split from Supply Capacity Observation Result. | PASS | Avoids evidence/domain conflation. |
| Event vs situation confusion | Manufacturing/distribution/procurement/disruption are Events; shortage/stockout are Situations. | PASS | Start/resolution events may be added only if evidence requires. |
| Information object vs real-world entity | Source Record/Assertion/Dataset separated from Product/Facility/Shortage. | PASS | Provenance layer can refer to real-world assertions without identity collapse. |
| Mixin rigidity misuse | `Ecosystem Participant` and `Asset-at-Risk` are RoleMixins because their specializations can have different identity providers and are anti-rigid. | PASS | No semi-rigid Mixin needed for these patterns. |
| Quality/Mode characterization | Strength and Match Confidence are Qualities; Supply Capacity/Vulnerability/Enterprise Capability are Modes with explicit bearers. | PASS conceptually | W5 should encode characterization constraints. |
| Part-whole misuse | Organization↔Facility not modeled as componentOf; administrative geography not forced into functional mereology. | PASS | Use operation/formal containment relations. |
| Generic catch-all relation | V1 Ecosystem Relationship/Supply Chain Relationship replaced by typed relations. | PASS | Generic V1 forms remain lineage only. |
| Extension leakage | BA/Risk/Safety/Market Access/Clinical/Digital do not define Core identity. | PASS | Module dependency direction frozen at Gate D. |
| Held-out contamination | W4 uses W3 inventory/evidence only; held-out H1–H3 are not used to add Core types. | PASS | Preserves W7 generalizability design. |

## Refactorings introduced by the review
1. `Ecosystem Participant Role` → **RoleMixin** because Organization and Facility roles inherit different identities.
2. `Site / Facility` normalized to **Facility Kind**; `Site` becomes a source synonym/context label, not a second Core identity.
3. `Product Classification` split into **Scheme + Entry + Assignment Relator**.
4. `Product Listing / Marketing Status` split into **Market Listing Relator + status value**.
5. `Medicine Shortage Case` normalized to **Medicine Shortage Situation**; source case/record remains provenance information.
6. `Observation` split into **Observation Activity Event + Observation Result information object**.
7. `Supply Capacity Observation` split into **Supply Capacity Mode + Observation Result**.
8. `Identifier` normalized to **Identifier Value + Identifier Scheme + Identifier Assignment Relator**.
9. `Match Evidence / Confidence` split into **Evidence support + Match Confidence Quality**.
10. `Risk Treatment / Mitigation` split into **Risk Treatment Plan + Risk Treatment Activity**.
11. Organization↔Facility `componentOf` interpretation rejected; **Facility Operation Relator** introduced.
12. Essential/Critical medicine concepts retained as **contextual assignment Relators**, not rigid Product types.

## Residual semantic risks — non-blocking for Gate D
### R1. Medicinal Product vs Product Presentation identity boundary — Medium
W4 intentionally models them as separate Kinds. W5/W6 source mapping may reveal that some source identifiers collapse the distinction. Mapping must adapt to source granularity rather than collapse the conceptual distinction.

### R2. Dosage Form / Package as specification objects — Low–Medium
Current treatment as stable specification/reference entities is defensible for integration. Formalization should avoid asserting stronger physical-part semantics without batch/package-instance data.

### R3. Supply Dependency completeness — Medium
Conceptual pattern is sound, but public data are incomplete. This affects empirical population/evaluation, not the Core identity analysis.

### R4. Regulatory Requirement social-object alignment — Low–Medium
W4 treats requirements as normative information/social objects in an extension. A deeper UFO-C normative-description alignment can be added without changing Core.

### R5. COVER/ROSE mapping details — Medium, extension-only
Risk adapter is conceptually aligned but not formally imported. Exact class/property alignments must be verified in W5 or a dedicated risk-extension wave.

### R6. Machine-readable OntoUML serialization — Deferred implementation
The W4 integrated model is specified textually and in PlantUML. A native machine-readable OntoUML serialization/tool validation is recommended before or during W5, but absence of that serialization does not invalidate the conceptual Gate D review.

## Gate D recommendation
**PASS / APPROVE with the current conceptual architecture.**

No critical/high semantic defect remains that requires another W3 discovery cycle. The remaining risks are formalization, source-mapping or extension-alignment issues and can be addressed in W5–W7 without reopening the W4 Core identity decisions unless new evidence contradicts them.
