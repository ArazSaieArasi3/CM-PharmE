# V1 Research Design and Evidence Review

> **Version scope:** V1  
> **Status:** Stable  
> **Updated:** 2026-09-23

## Visual research process

![CM-PharmE 1.x research process](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/process/DGM-PRC-002--v1-research-process.svg)

**DGM-PRC-002** summarizes the V1 research-to-model pathway. Detailed evidence and method remain authoritative in the linked V1 artifacts.

## Method overview

V1 uses a traceable research-to-model sequence:

**Problem framing → PRISMA-guided evidence review → thematic synthesis → evidence-to-domain mapping → business-architecture concern identification → UFO/OntoUML concept classification → relation selection → cardinality assignment → integrated model → demonstration/evaluation → versioned repository evidence**

## Evidence review

The journal-oriented review reports:
- 380 records identified;
- 49 duplicates removed;
- 331 records screened;
- 89 full texts assessed;
- 17 studies retained for qualitative synthesis.

The review focuses on ontology engineering, business/enterprise architecture, conceptual modeling and organizational/ecosystem-level pharmaceutical or healthcare concerns.

These counts are provenance for the V1 model-development lineage; they are not automatically updated unless a new evidence-review cycle is explicitly performed.

## Thematic synthesis

The repository documents a three-stage synthesis logic:
1. line-by-line coding;
2. consolidation into descriptive categories;
3. abstraction into higher-order analytical themes.

Representative concerns include organization structure, capability, strategy, stakeholder collaboration, partnership, governance, compliance, clinical/business process, data integration, platform concerns, traceability and semantic interoperability.

The synthesis is interpretive, not a simple frequency ranking.

## Evidence-to-domain decomposition

Themes organize the literature; domains organize modeling responsibilities. They are deliberately not treated as one-to-one categories.

The five V1 domains are:
- Organizational / Structural;
- Ecosystem / Collaborative;
- Operational / Process;
- Governance / Regulatory;
- Digital Transformation.

## Business architecture role

Business architecture is used as an analytical lens to identify what kinds of concerns require representation: organization design, participation, capability, strategy, value delivery, operating activity, governance and digital enablement.

This does **not** establish full BACM conformance and does not itself determine OntoUML stereotypes.

## UFO/OntoUML modeling logic

Candidate concepts are classified by ontological status:
- **Kind** — rigid identity-supplying entity type;
- **Role** — contingent/context-dependent classification;
- **Relator** — reified relational entity existentially dependent on participants;
- **Mode** — dependent capability/property/policy/objective/requirement;
- **Perdurant** — process/activity unfolding in time.

Relation choices follow those commitments, with conservative semantics preferred over unsupported stronger commitments.

## Design-science orientation

The research aligns its completed activities to DSRM logic: problem identification, objectives, design/development, demonstration, evaluation and communication. This is a methodological/reporting alignment; it is not a claim of repeated operational deployment cycles.

## Evidence

- [Research and model-development method](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/methodology/research-and-model-development.md)
- [Research rationale](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/research/rationale.md)
- [Publication traceability](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/research/publication-to-repository-traceability.md)

## Interpretation boundary

The V1 method supports a disciplined conceptual-model development process. It does not establish universal pharmaceutical-domain completeness, empirical implementation effectiveness or conformance to every external standard.

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V1
- **Documentation maturity:** Stable
- **Authoritative source:** `main` methodology and publication evidence
- **Last synchronized:** 2026-09-23
- **Last synchronized ref:** `5099888668d35f798e4759e3534e707ed906db24`
- **Related issues/PRs:** V1 research/evaluation closure lineage
- **Evidence status:** Supported by repository methodology and publication traceability
- **Future refresh:** None planned unless V1 evidence is formally corrected
- **Wiki baseline:** WB-2026.09.1

</details>
