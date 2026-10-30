# G3-3-E — connectivity and isolate evidence review

Date: 2026-10-09 Asia/Tehran. Branch: `v2/connectivity-audit-2-1-candidate`. This is a bounded review packet, not ontology release or author sign-off.

## Recomputed topology

The inputs are the [B2 native OntoUML overlay](../2.1.0-alpha.1-g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json), the [G3-C aligned OWL](../2.1.0-alpha.1-g3-3-c-integrated-validation/active.ttl), the [G3-D compressed real-source ABox](../2.1.0-alpha.1-g3-3-d-real-source-migration/real-source-abox.nt.gz.b64), and the frozen [14-row prior isolate review](source-isolate-review.json). Exact hashes and row-level results are in [connectivity-evidence.json](connectivity-evidence.json).

| Metric | Native | OWL | Difference |
|---|---:|---:|---:|
| Named non-datatype classes | 138 | 138 | 0 |
| Direct named subclass edges | 99 | 99 | 0 |
| Object-property edges with both explicit named ends | 71 | 71 | 0 |
| Distinct undirected class-graph edges | 168 | 168 | 0 |
| Components | 15 | 15 | 0 |
| Largest component | 124 | 124 | 0 |
| Single-class components | 14 | 14 | 0 |

Class, object-property and named subclass sets match exactly. The 71 typed edges also match by property name **and** endpoint. This diagnostic treats each explicit named class hierarchy or domain–range association as an undirected graph edge; it does not infer anonymous unions, restrictions, datatypes, subproperty closures or OntoUML semantics. Thus 124/138 classes occur in the giant component under this **specific** metric; it is not a domain-completeness or quality percentage.

Three native/OWL relations already name an isolated source class but have no typed named target: `baViewRepresents`, `capacityBearer`, and `riskTreatmentAddresses`. Their omission from this graph is intentional. A geometric island in this projection does not prove the class has no conceptual relation.

## Fourteen proposal dispositions from actual P1 records

The deterministic NHIF sample has 768 rows in five nonrandom byte-range strata. No sampled ABox individual is explicitly typed as any of the 14 isolated source classes, and none asserts any proposed connector. Two proposed targets have direct instances: `MedicinalProduct` (264) and `ObservationResult` (3,072). A destination instance alone cannot verify the relation or its temporal/clinical truthmaker.

| Isolated class | Proposed connector → target | Target instances | P1 decision and key guard |
|---|---|---:|---|
| AdverseEventReportingActivity | reportConcernsProduct → MedicinalProduct | 264 | Hold; a product/reimbursement row is not a submitted safety report. |
| BusinessArchitectureView | baViewRepresents → Organization | 0 | Hold optional BA dependency; no versioned view witness. Existing end is broad/untyped. |
| DigitalInformationSystemComponent | supportsObservationActivity → ObservationActivity | 0 | Hold; dataset access does not identify a deployed system component or support event. |
| DistributionLogisticsActivity | logisticsAtSite → DistributionSiteRole | 0 | Hold; no dated movement at a distribution site. |
| ManufacturingActivity | manufacturingAtSite → ManufacturingSiteRole | 0 | Hold; a marketed product is not a batch manufacture at a site. |
| PharmacovigilanceRequirement | requirementAppliesInJurisdiction → RegulatoryJurisdiction | 0 | Hold; reimbursement region codes do not establish authoritative legal scope. |
| PostMarketSurveillanceActivity | surveillanceProducesResult → ObservationResult | 3,072 | Hold; aggregate utilization results do not prove a surveillance process produced them. |
| ProcurementActivity | procurementBuyer → Organization | 0 | Hold; reimbursement cost is not a purchase transaction with a buyer. |
| RegulatoryRequirement | requirementAppliesInJurisdiction → RegulatoryJurisdiction | 0 | Hold; normative source, version and effective period absent. |
| RiskTreatmentActivity | executesRiskTreatmentPlan → RiskTreatmentPlan | 0 | Hold; no performed mitigation or plan; existing `riskTreatmentAddresses` is broad/untyped. |
| RiskTreatmentPlan | planAddressesDependency → SupplyDependency | 0 | Hold; no plan naming a dependency. |
| ServiceOfferingSpecification | referencesOfferedActivity → ManufacturingActivity | 0 | Continue optional deferral; no provider commitment or offering source. |
| StockoutSituation | stockoutAtFacility → Facility | 0 | Hold; dispensed pack count cannot establish a local stockout with site and interval. |
| SupplyCapacity | capacityBearer → Facility | 0 | Hold; aggregate quantity cannot establish an intrinsic capacity Mode or its unique bearer. Existing end is broad/untyped. |

These are **P1-sample dispositions**, not permanent rejections. The 14 rows span eight module labels from the prior review: CORE_EVENT (2), OPTIONAL_BA (2), OPTIONAL_DIGITAL (1), PHARMACOVIGILANCE (2), REGULATORY_POLICY (2), RISK_RESILIENCE (2), SUPPLY_EVENT (1), SUPPLY_RESILIENCE (2). These labels describe coverage of the isolate docket, **not** coverage of every domain or the complete ontology.

If all 14 prospective links were hypothetically connected to their proposed targets, this graph would have one component and no isolates. That number is a topology calculation only. **No model edge was added or deleted**, because none of those instances establishes a source-class truthmaker or relation. The approved SupplyCapacity typed Organization/Facility exactly-one-of-two route still needs its own design, positive and negative witnesses, and formal implementation. The full official 20-antipattern engine has not run.

## Reproduction and limits

```bash
PYTHONPATH=/tmp/cmpe-g3c python audit_g3e.py
```

For a fresh environment, install `rdflib==7.6.0` and invoke the script in this directory. When checked out under the repository, its defaults refer to the three sibling candidate directories shown above. The inputs are SHA-256 pinned in the JSON. The compressed G3-D ABox is decoded in memory and compared to the verified 39,272-triple hash.

The bounded sample contains no explicit witnesses for the proposed source concepts; it cannot establish absence across the complete NHIF source, other intended sources or inferred facts. The 14 decisions, 29 relation dispositions, 10 ImpAbs endpoint questions, 19 RepRel uniqueness policies, typed SupplyCapacity bearer, and official anti-pattern detector are still open. PR #305 remains draft; issue #306 remains open; the W6 filename contract mismatch is issue #307.

## Next exact turn

**G3-3-F:** assemble a single traceability matrix from scientific decision → native element → OWL/SHACL constraint → positive and negative fixture → real-source witness/absence → review owner and gate; produce the human-review handoff with explicit unresolved items and no premature release claim. Afterwards, obtain the necessary scientific decisions and execute the remaining formal/detector gates before closing G3.
