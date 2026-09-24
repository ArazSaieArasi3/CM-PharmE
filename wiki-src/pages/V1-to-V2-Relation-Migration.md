# V1 to V2 Relation Migration

> **Version scope:** Cross-version  
> **Status:** Stable-to-date / Evolving  
> **Updated:** 2026-09-23

## V1 baseline

V1 records **40 canonical semantic relations**: 39 object-property-style records plus one explicit generalization.

V2 does not preserve relation identity merely because a V1 relation exists. Relation continuity is determined by meaning, evidence and ontological treatment.

## Stable relation-family migration

| V1 relation family | V2 disposition |
|---|---|
| Enterprise structure/capability/resource | Move to Business Architecture extension |
| Generic stakeholder/actor relations | Refine into role-bearing and typed participation |
| Generic ecosystem relationship | Split into typed relators/material/formal relations |
| Clinical pathway/provider/patient | Move to Clinical extension |
| Governance/oversight | Refine into Authority/Jurisdiction/Requirement/Authorization/Oversight patterns |
| Generic business-process | Split into typed activities and participation |
| Supply-chain | Split into logistics/procurement/supply-dependency/shortage/alternative patterns |
| Digital-platform | Move to Digital/Application extension |
| Safety/pharmacovigilance | Move to Pharmacovigilance extension |
| Risk-management | Move/alignment to Risk Management extension |

## V2 relation-design change

V2 more explicitly separates:
- **Relators** as truth-makers of persistent contextual relationships;
- **Mediation** between relators and participants;
- derived **Material** relations for convenient domain statements;
- **Characterization** for modes/qualities and bearers;
- event participation;
- formal/aboutness/context relations;
- propositions/assertions from the domain relationships they describe.

## Key V2 relation patterns

Stable current patterns include:
- Facility Operation → `operates(Organization, Facility)`;
- Establishment Registration → registered-with relation;
- Regulatory Authorization → authorized-for relation;
- Product Classification Assignment → classified-as relation;
- Market Listing → listed/marketed-in-context relation;
- Contextual Medicine Classification Assignment;
- Alternative Medicinal Product Assignment;
- Supply Dependency;
- Identifier Assignment;
- Evidence Support;
- Regulatory Oversight extension;
- Strategic Partnership Agreement extension.

## Important semantic refinements

### Record is not relationship
A registration/license/source record is evidence about a regulatory relation, not necessarily the relation itself.

### Identifier is not identity
NDC, ATC, GeoNames or local identifiers are values under schemes/assignments, not universal identity providers.

### Assertion is not domain truth-maker
Mapping Assertion and Entity Match Assertion are propositions. Evidence Support/provenance governs support for those propositions.

### Physical containment is not assumed from operation
Facility Operation does not make Facility a mereological component of Organization.

## What is not yet final

The W3 migration matrix provides relation-family migration, and W4 provides explicit V2 relation patterns. However, a complete one-row-per-V1-relation final human-reviewed mapping is not yet asserted as complete.

This gap is intentional and must be resolved through the Human Ontology Review relation catalog/review work under #173 and synchronized through #213.

## Evidence

- [V1 relation index](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/relations/index.md)
- [V1 relation catalog](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/catalog/relations.yaml)
- [W3 migration matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w3/v1-v2-migration-matrix.md)
- [W4 relator/material patterns](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/relator-material-patterns.md)
- [Integrated OntoUML model](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/integrated-ontouml-model.md)

---

<details>
<summary>Documentation record</summary>

- **Page scope:** Cross-version
- **Documentation maturity:** Stable-to-date / Evolving
- **V1 authority:** V1 relation catalog and mappings on `main`
- **V2 authority:** W3 relation-migration policy and W4 relation-pattern specification
- **Last synchronized:** 2026-09-23
- **Related issues/PRs:** #159, #173, #206
- **Evidence status:** Stable relation-family migration and V2 relation-pattern evidence; exhaustive per-relation V1→V2 disposition remains a human-review dependency
- **Future refresh:** #213
- **Wiki baseline:** WB-2026.09.1
- **Authoritative source:** V1: main; V2: v2/research-program
- **Last synchronized ref:** V1: main; V2: v2/research-program

</details>
