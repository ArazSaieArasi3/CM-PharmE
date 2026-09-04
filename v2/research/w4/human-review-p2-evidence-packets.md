# CM-PharmE 2.0 Human Review — P2 Evidence Packets

Issue: #159  
Scope: CM-PharmE 2.0 only  
Status: author-review preparation  
Semantic effect: none  
V1/main impact: none

## Purpose

This artifact prepares bounded, repository-backed review packets for the three P2 concepts frozen in `human-review-high-risk-queue.md`. P2 is the legacy/extension migration lane: these concepts are retained because they preserve useful V1 continuity or extension structure, but their presence must not be upgraded into Core necessity, semantic equivalence among predecessors, or publication validation.

The primary gap class is `G6` (V1-lineage dependence). V1 lineage is traceability evidence; it is not by itself evidence that the final V2 abstraction, stereotype, scope, or consolidation is ontologically correct.

## Source anchors

- `human-review-concept-provenance-matrix.md` — current Gate-D concept, stereotype, lineage, admitted/held-out evidence and stable IRI.
- `human-review-provenance-gap-register.md` — controlled G0–G9 gap vocabulary and claim-boundary rules.
- `human-review-high-risk-queue.md` — frozen P2 membership and review consequence.
- `../w3/v1-v2-migration-matrix.md` — authoritative V1→V2 migration decisions used below.
- `integrated-ontouml-model.md` — current V2 conceptual specification.
- `../../ontology/source/modules/30-extensions.ttl` — extension implementation surface where applicable.

No source anchor is upgraded beyond its governed role.

---

## P2-01 — Enterprise Capability (`cmpe:EnterpriseCapability`)

**Current commitment**  
An optional Business Architecture extension concept representing an enterprise capability without making Business Architecture part of the pharmaceutical ecosystem Core identity.

**Repository-backed support**
- The V1→V2 migration matrix maps V1 `C0005 Enterprise Capability` to **Move to BA Extension**.
- The same migration policy explicitly demotes Business Architecture from Core identity to an optional analytical view.
- The risk-first queue records current support as V1 + PR1/M1/M2 and marks the row `G6` / local-semantic.

**What the evidence supports now**
- Capability semantics may be preserved for an optional Business Architecture view because the concept has explicit V1 lineage.
- Keeping the concept outside Core prevents an enterprise-centric decomposition from being treated as a necessary identity condition for pharmaceutical ecosystem entities.

**What remains unproven / gap**
- V1 presence does not establish that `EnterpriseCapability` is required by the V2 pharmaceutical domain (`G6`).
- No independent V2 dataset or official-source evidence in the current matrix establishes domain necessity, completeness of capability taxonomy, or a specific capability decomposition.
- M1/M2 can support the modeling method but do not validate this domain abstraction.

**Author review question**
Does `EnterpriseCapability` provide enough analytical value to remain in the optional BA extension while being explicitly excluded from Core claims and from any assertion of V2 domain necessity?

**Safe boundary before review**
Retain only as an optional extension concept. Do not infer Core status, completeness of enterprise capabilities, or independent V2 validation from V1 lineage.

---

## P2-02 — Digital System Component (`cmpe:DigitalInformationSystemComponent`)

**Current commitment**  
A generic Digital/Application extension abstraction for information-system components, replacing technology/platform-specific V1 forms without asserting that those predecessor technologies are semantically equivalent.

**Repository-backed support**
- The migration matrix maps `C0029 Digital Health Platform Component` to **Generalize / Move** as a general Digital / Information System Component in an application extension.
- Technology-specific V1 concepts are deliberately excluded from Core: `C0030 AI-Enabled Clinical Decision Support System` is deferred, `C0031 Blockchain-Based Supply Chain Ledger` is deprecated in technology-specific Core form, and `C0033 Electronic Health Record System` / `C0035 Telemedicine Service Channel` move to Digital/Clinical extensions.
- The risk-first queue records V1 lineage + PR1/M2 as current support and assigns `G6` / local-semantic.

**What the evidence supports now**
- V2 should avoid hard-coding a particular implementation technology into ecosystem Core semantics.
- A generic extension-level system-component abstraction can preserve migration traceability while technology-specific implementations remain downstream/application specializations or deferred concepts.

**What remains unproven / gap**
- The migration does not prove that all deprecated/deferred V1 technology concepts share one ontology identity (`G6`).
- No claim is established that the generic component abstraction is exhaustive for digital-health/pharmaceutical software architecture.
- V1 labels do not justify `owl:equivalentClass`, subsumption, or one-to-one semantic replacement without separate modeling evidence.

**Author review question**
Does the generic `DigitalInformationSystemComponent` abstraction preserve the useful common denominator of the V1 digital concepts while keeping technology-specific semantics as optional specializations rather than implying equivalence?

**Safe boundary before review**
Keep the concept in the Digital/Application extension. Treat predecessor mapping as migration/traceability only; do not claim equivalence, architectural completeness, or Core status.

---

## P2-03 — Clinical Care Participant (`cmpe:ClinicalCareParticipant`)

**Current commitment**  
A contextual Clinical extension role used to consolidate V1 care-delivery participant concepts while preserving the possibility of more specific downstream roles.

**Repository-backed support**
- The migration matrix moves `C0007 Clinical Workforce` to the Clinical extension and explicitly consolidates it under a Clinical Care Participant role.
- `C0019 Prescribing Physician` moves to the Clinical extension as a specialization of that role; `C0021 Healthcare Provider` also moves to a contextual healthcare-provider role, while `C0020 Healthcare Provider Organization` is generalized to Organization with provider status treated contextually when the extension is activated.
- The risk-first queue records V1-only admission support, H1 extension pressure, PR1/M1/M2 support and `G6` / local-semantic.

**What the evidence supports now**
- Clinical-care participation should be contextual rather than forcing physician/provider/workforce identities into the principal pharmaceutical ecosystem Core.
- Consolidation can reduce V1 duplication while allowing more specific participant roles to be modeled when the Clinical extension is activated.
- H1 may motivate extension coverage, but it remains held-out pressure/evidence lead rather than author/expert approval.

**What remains unproven / gap**
- V1 consolidation does not prove that all predecessor role distinctions can be safely collapsed into one undifferentiated participant role (`G6`).
- The current packet does not establish a complete clinical workforce/provider taxonomy or universal role hierarchy.
- H1 does not validate the final stereotype, role conditions, cardinalities, or downstream specialization design.

**Author review question**
Does `ClinicalCareParticipant` preserve the shared contextual participation semantics while leaving clinically material distinctions—such as prescribing physician, provider organization, provider role, and workforce role—available as explicit downstream specializations when needed?

**Safe boundary before review**
Retain the common role only as an extension abstraction. Do not erase predecessor distinctions by equivalence, and do not treat H1 pressure as semantic validation.

---

## Cross-packet review checklist

Before recording any P2 disposition, verify:

1. `G6`: V1 lineage is traceability, not independent V2 necessity or semantic correctness.
2. Optional BA/Digital/Clinical extension concepts are not promoted into Core claims by historical continuity.
3. Generalization/consolidation does not imply semantic equivalence among technology-, organization-, provider-, workforce-, or role-specific predecessors.
4. Methodological support (M1/M2) does not substitute for pharmaceutical-domain evidence.
5. Held-out extension pressure is not author/expert approval or empirical validation.
6. Any post-Gate-D semantic change is routed to a separate V2 design-decision issue before OWL/SHACL modification.
7. E9 expert evidence remains separate and cannot be inferred from these packets.

## Packet completion state

- P2 packet inventory: **3/3 prepared**.
- Risk-first packet inventory across P0/P1/P2: **19/19 prepared**.
- Human/author dispositions across the 19-row queue: **0/19 recorded**.
- Semantic changes caused by this artifact: **0**.
- External expert evidence added: **0**.
- Hosted CI/Actions required: **no**.

Completing packet preparation means only that the frozen risk-first queue now has bounded review packets. It does not mean the 19 rows passed human review, the remaining 68 matrix concepts were reviewed, #159 is complete, or CM-PharmE V2 is publication-ready.