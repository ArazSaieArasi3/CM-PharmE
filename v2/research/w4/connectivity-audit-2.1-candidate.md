# CM-PharmE 2.0 connectivity audit and 2.1 candidate decision package

Status: **analysis and candidate discovery only**. The Gate-D/W5 `2.0.0-alpha.1` semantic baseline, OWL, SHACL, mappings, evaluation results and manuscript claims are unchanged. Human semantic review is pending under #159/#173.

## Scope and reproducibility

This audit reads the project-native 87-element registry, the W4 PlantUML overview, W3 relation inventory, W4 relation-pattern specification, W5 TTL and the frozen W7-E3/E7/E8 evidence. Run `python tools/v2_ontology/connectivity_audit.py` to reproduce the [JSON graph metrics](connectivity-audit-baseline.json); add `--write-review-projection` to regenerate the corrected PlantUML view. The script treats generalizations and displayed relations as undirected edges **only for visualization connectivity**. It does not prove that OWL instances are connected, certify OntoUML, or approve a proposed relation.

The separately delivered `CM-PharmE_2.0_OntoUML_Complete.svg` (02 October 2026) is a 17-panel domain atlas, not an integrated cross-domain graph. Its 87 nodes and displayed relations formed 18 components with 12 isolated nodes when unknown endpoints and auxiliary rendering junctions were excluded. Because the SVG is not checked into this repository, the versioned W4 overview is the reproducible baseline below; the two projections have different edge sets and must not be presented as equivalent measurements.

## Quantitative baseline

| Projection | Elements | Components | Isolates | Meaning |
|---|---:|---:|---:|---|
| W4 overview, all elements | 87 | **20** | **12** | 81 classes plus 6 datatypes; 85 drawn edge instances. |
| W4 overview, classes only | 81 | **16** | **8** | Excludes the six datatype nodes and their incident diagram edges. |
| After showing three relations already documented in W5/W4 | 81 classes | **13** | **7** | The [corrected review projection](integrated-ontouml-review-projection.puml) only; no new ontology assertion. |
| If *all ten* additional candidates passed source and author review | 81 classes | **3** | **2** | Hypothetical topology, **not** the attained ontology state. |

The two remaining isolated classes in the hypothetical scenario are `ClinicalCareParticipant` and `ServiceOfferingSpecification`. They must be justified, moved to a separately described extension, deferred or removed through a versioned decision; they must not be attached by an invented relationship. In the present overview, the other six isolated classes are `DiagnosisClassificationReference`, `DigitalInformationSystemComponent`, `DisruptionEvent`, `ProcurementActivity`, `ProvenanceActivity` and `StockoutSituation`. Four isolated nodes are datatypes (`Address`, `GeospatialPosition`, `ReportingPeriod`, `TimeInterval`), not independent domain entities. `IdentifierValue` and `MeasureValue` are the other two datatypes and are already attached in the W4 overview.

W5 declares **52 object properties**. **17** do not declare *both* an explicit `rdfs:domain` and `rdfs:range`. That is a queryable typing/documentation gap, not automatically an error: some properties intentionally accept bearers with different identities and cannot safely acquire a single narrow range. Audit each property's intended end types using union/SHACL/companion conceptual metadata as appropriate; avoid a range that would infer false types in OWL.

## Candidate disposition

The machine-readable [connection register](connection-candidates.csv) records endpoints, treatment, source and review condition. It has **3 documented relations missing from the W4 overview, 10 review candidates and 2 deferred cases**.

| Priority | IDs | Decision required |
|---|---|---|
| Projection repair | C01, C02, C15 | Show existing `EvidenceSupport→SourceRecord`, contextual classification→product and provenance activity→assertion links. Check their OntoUML visual treatment before rendering. |
| Research-semantic bridges | C03–C06 | Define observation/aboutness, assertion/aboutness, scoped identifier assignment and risk-assessment targets. Product is an illustrative endpoint, **not** a universal range. |
| Supply and access extension | C08–C11 | Verify disruption target, procurement participants, stockout product/site/time scope and diagnosis context against admitted sources. The C1-based relations remain conditional. |
| Safety and digital extension | C07, C12 | Activate only with source-backed task and stated extension scope; reporting activity must not be conflated with an adverse-event case. |
| Deferred | C13, C14 | Do not force a business service or clinical role onto Organization. Resolve the appropriate service bearer and clinical-care activity/role pattern first. |

## OntoUML quality risks beyond graph connectivity

1. W7-E3 passed 17 project-native checks with **three warnings**: incomplete extension Relator mediation for `RegulatoryOversight` and `StrategicPartnershipAgreement`; Role dependence not fully enforced in OWL; no bearer property for the `Vulnerability` and `EnterpriseCapability` Modes. Passing those checks is not official OntoUML tool certification.
2. For every active Relator, specify its mediated individuals and justified lower multiplicities. For every Mode/Quality, specify its bearer and characterization. Define the event/situation/information-object boundaries before drawing any bridge. A generic `relatedTo` edge cannot satisfy this gate.
3. `AlternativeMedicinalProductRole` inherits `EcosystemParticipant` in W5 while the W4 RoleMixin spans organizational/facility participation. Review whether a product can legitimately be an ecosystem participant in the same sense; this is a **semantic question**, not a proven inconsistency.
4. W7-E7 retained nine unsupported source semantics, including an adverse-event case/event and several source-specific regulatory, product, inventory and funding details. W7-E8 exposed trial-specific gaps (Clinical Study, Arm/Group, Outcome, Phase/Status and relations). These are candidate **extension** discoveries, not permission to inflate the Core or revise the already-scored first-pass held-out result.
5. The six datatypes require appropriate data-value or reference treatment. Do not add false OntoUML associations to make a connectivity statistic look better. Cardinalities remain source- and rule-specific; `0..*` or `1..*` must not be guessed from table foreign keys.

## Controlled 2.1 progression

1. **Projection repair:** incorporate the three already documented links in a review diagram labeled `2.0.0-alpha.1 — corrected projection`. Recompute graph metrics; preserve the Gate-D conceptual and W5 formal fingerprints.
2. **Relation decision register:** for C03–C12 and every one of the 17 partially typed W5 object properties, record definition, source row/field or normative reference, domain/range alternatives, UFO/OntoUML type, identity/dependence/temporality, multiplicities, counterexample, target CQ and human disposition. Do not promote merely because it joins components.
3. **Concept discovery:** inspect the nine E7 gaps and H1 extension pressure against article scope. For each suggested new type record `accept / refine / split / defer / reject`. Keep post-test changes outside the frozen E8 first-pass scoring.
4. **Human Gate:** disposition under #159/#173, with a migration matrix from all 87 baseline elements and an explicit decision about optional Digital Systems, Clinical Care and Business Architecture modules. Only approved semantic changes become `2.1.0-alpha.1` on a separate branch; unchanged presentation fixes can remain in 2.0.
5. **Regression and release:** rerun the project-native E3 checks, official OntoUML validation if a native serialization is produced, OWL 2 DL/reasoners, SHACL, 18 frozen CQs plus new CQs, mappings, the four SQL↔SPARQL benchmark pairs, W7 claim ledger and manuscript/Wiki/figure traceability. Preserve earlier baseline results rather than overwriting them.

### Acceptance and rejection gates

- Every active class must have a justified semantic path within its declared module or an explicit external-extension/deferred disposition; datatype nodes are assessed separately.
- Every new relation must have source/requirement provenance, defined ends and OntoUML treatment; every Relator and Mode must satisfy its dependence/bearer obligations.
- No existing protected Organization/Facility, geography/jurisdiction, product/substance/presentation or observation/phenomenon distinction may be collapsed for connectivity.
- Reject an edge motivated only by graph layout, a guessed cardinality, an unsupported full-data claim, a silent Core expansion, or retroactive improvement of held-out first-pass scores.

## Current quality conclusion

**The quantity of the ontology has not changed:** 87 conceptual elements (81 classes, 6 datatypes), 52 W5 object properties and the frozen `2.0.0-alpha.1` baseline. The quality of *review and defect visibility* has improved through an executable baseline and 15 traceable candidate entries. The quality of the **approved semantic ontology has not yet increased**, because no candidate has been authorized or formalized. The measured class-only W4 diagram remains at **16 components and 8 isolates**; the corrected projection shows **13 components and 7 isolates** with existing relations; the `3 components / 2 isolates` figure is a conditional what-if, not a result. No claim of complete connectedness or official OntoUML conformance is warranted at this station.
