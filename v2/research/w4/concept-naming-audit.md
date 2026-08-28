# CM-PharmE 2.0 Concept Naming Audit

Issue: #156  
Scope: CM-PharmE 2.0 only  
V1/main impact: none

## Decision
The 87-element Gate-D conceptual inventory is preserved exactly. This work normalizes human-facing canonical labels while keeping all V2 IRIs, OntoUML stereotypes, class hierarchies, formal axioms, SHACL constraints, data mappings, evaluation evidence, and claim boundaries unchanged.

## Naming rules
1. The OntoUML stereotype carries metamodel semantics; canonical domain labels should not redundantly end in `Role` merely because the stereotype is `<<Role>>`.
2. Canonical labels should be readable noun phrases rather than CamelCase implementation identifiers.
3. Slash-based labels should be replaced by one cohesive canonical phrase when possible; source terminology is retained with `skos:altLabel` where useful.
4. `Activity`, `Situation`, `Observation Result`, `Assignment`, `Plan`, and similar terms are retained when they express a real ontological distinction rather than a stereotype echo.
5. Stable IRIs are not renamed by a label-quality cleanup.
6. Any rename that could alter extension scope or split a concept requires a separate design decision.

## Audit statistics
- Gate-D conceptual elements reviewed: **87/87**
- Core: **32**
- X-INFRA: **25**
- Extensions: **30**
- OntoUML stereotype changes: **0**
- IRI changes: **0**
- Canonical concept labels materially refined: **19**
- Previously identified CamelCase-style multiword `rdfs:label` values normalized for human readability: **50**
- Concepts split/merged: **0**
- Open semantic split decision after this audit: **1** (`Reimbursement and Utilization Observation Result`)

## Canonical label changes
| Stable V2 IRI local name | Previous human-facing label | Canonical human-facing label | Handling |
|---|---|---|---|
| `RegulatoryAuthorityRole` | Regulatory Authority Role | Regulatory Authority | `Role` retained only as stereotype/IRI history |
| `ManufacturerRole` | Manufacturer Role | Manufacturer | same |
| `ImporterRole` | Importer Role | Importer | same |
| `ProductResponsibleLabelerRole` | Product-Responsible / Labeler Role | Product Responsible Organization | `Labeler` retained as altLabel |
| `WholesaleDistributorRole` | Wholesale Distributor Role | Wholesale Distributor | role semantics remain `<<Role>>` |
| `ThirdPartyLogisticsProviderRole` | Third-Party Logistics Provider Role | Third-Party Logistics Provider | role semantics remain `<<Role>>` |
| `ManufacturingSiteRole` | Manufacturing Site Role | Manufacturing Site | role semantics remain `<<Role>>` |
| `DistributionSiteRole` | Distribution Site Role | Distribution Site | role semantics remain `<<Role>>` |
| `DistributionLogisticsActivity` | Distribution / Logistics Activity | Pharmaceutical Logistics Activity | old wording retained as altLabel |
| `DataSourceResource` | Data Source Resource | Data Source | stable IRI retained |
| `EssentialMedicineClassification` | Essential Medicine Classification | Essential Medicine Classification Assignment | clarifies assignment semantics |
| `CriticalMedicineClassification` | Critical Medicine Classification | Critical Medicine Classification Assignment | clarifies assignment semantics |
| `AlternativeMedicinalProductRole` | Alternative Medicinal Product Role | Alternative Medicinal Product | role semantics remain `<<Role>>` |
| `AlternativeMedicineAssignment` | Alternative Medicine Assignment | Alternative Medicinal Product Assignment | terminology aligned with product layer |
| `LeadTimeObservationResult` | Lead-Time Observation Result | Lead Time Observation Result | punctuation normalization |
| `PayerFundingOrganizationRole` | Payer / Funding Organization Role | Healthcare Financing Organization | umbrella retained; payer/funder kept as altLabels |
| `ReimbursementUtilisationObservationResult` | Reimbursement / Utilisation Observation Result | Reimbursement and Utilization Observation Result | wording only; split question remains open |
| `AssetAtRisk` | Asset-at-Risk | Asset at Risk | punctuation normalization |
| `DigitalInformationSystemComponent` | Digital / Information System Component | Digital System Component | cohesive canonical phrase |

## R2 decisions
### Product Responsible Organization
Resolved for V2 labeling. The existing IRI and `<<Role>>` stereotype remain unchanged. `Labeler` is retained as an alternative/source-facing label. No conceptual split is introduced.

### Healthcare Financing Organization
Resolved provisionally as a single umbrella role so the 87-element Gate-D inventory remains stable. `Payer Organization` and `Funding Organization` are retained as alternative labels. If later evidence shows materially different dependence or identity commitments, a separate split decision is required.

### Reimbursement and Utilization Observation Result
Only the human-facing wording is normalized in this work item. Whether reimbursement and utilization observations should be represented as two separate subkinds is **not** decided here because that would change the conceptual inventory and may affect mappings/evaluation. This requires human conceptual review.

## Formalization boundary
The ontology continues to use stable IRIs such as `cmpe:ManufacturerRole`, `cmpe:PayerFundingOrganizationRole`, and `cmpe:ReimbursementUtilisationObservationResult`. Human-facing `rdfs:label` values are presentation/communication artifacts and do not redefine the underlying semantic identity.

## V1 isolation
No CM-PharmE 1.x source, ontology, manuscript artifact, or reviewer-facing `main` content is modified by this audit. CM-PharmE 2.0 remains isolated on the V2 branch line while the previous journal article is under review.
