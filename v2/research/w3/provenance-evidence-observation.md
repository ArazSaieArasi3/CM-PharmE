# W3 Provenance, Evidence and Observation Semantics

## Objective
Make source traceability part of the semantic design rather than an after-the-fact documentation layer. This is required for the approved Ontology↔RDB↔KG Consistency & Provenance demonstrator and for defensible multi-source research claims.

## 1. Layer separation
CM-PharmE 2.0 should distinguish at least four layers:

1. **Domain reality layer** — organizations, sites, products, substances, activities, shortages, jurisdictions, etc.
2. **Observation/assertion layer** — source-bounded statements or measurements about domain reality.
3. **Source/data layer** — datasets, releases, records, documents and identifiers.
4. **Research transformation layer** — ingestion, normalization, entity resolution, mapping and validation activities that transform source representations into RDB/KG artifacts.

This separation prevents a CSV row, API record or regulatory page entry from being treated as if it were the real-world entity itself.

## 2. Core infrastructure candidates
| Candidate | Purpose | Typical evidence | Admission |
|---|---|---|---|
| Data Source | Identifies the maintaining/publishing authority/system/resource. | FDA, EMA, WHO, NHIF, GeoNames, Zenodo record | X-INFRA |
| Dataset | Identifies an organized collection. | P1/P2/C1/S1/S2 | X-INFRA |
| Dataset Release / Version | Freezes a specific dataset snapshot/version for reproducibility. | DOI version, API/download snapshot date | X-INFRA |
| Source Record | Identifiable source-level row/entry/document record. | NHIF row; FDA/EMA API record | X-INFRA |
| Assertion | Explicit proposition represented in research artifacts/KG. | “facility F bears role R” | X-INFRA |
| Observation | Evidence-bearing observation about a subject in time/space/context. | demand, reimbursement, availability, inventory | X-INFRA parent pattern |
| Measure / Quantity Value | Numeric/coded result with unit/currency/count semantics. | patient count, pack count, expenditure, lead time | X-INFRA |
| Evidence Item | Research evidence supporting an assertion, mapping or design decision. | source record, official definition, DOI metadata | X-INFRA |
| Mapping Assertion | Traceable mapping from source representation to canonical representation. | source `hospital_code` → canonical Facility | X-INFRA |
| Provenance Activity | Ingestion/transformation/normalization/mapping process. | ETL job, geocoding, normalization | X-INFRA |
| Data Quality Finding | Recorded validation result/exception. | unresolved identifier; SHACL violation; parse issue | X-INFRA |

## 3. Observation families discovered in W3
The generic `Observation` pattern is needed because multiple sources provide measurements/status records rather than enduring objects:

- Reimbursement / Utilisation Observation — P1/P2.
- Availability Observation — EMA/ESMP evidence.
- Demand Observation — EMA/ESMP, C1, P1/P2 aggregate usage signals.
- Supply Capacity Observation — EMA/ESMP/C1.
- Inventory Observation — C1.
- Lead-Time Observation — C1.
- Cost/Price/Expenditure values — measures attached to observations rather than standalone ecosystem actors.

### Important anti-conflation rule
`patients_num` in P1/P2 is an aggregate **measure**. It does not support instantiating individual Patient entities. Likewise, `costs` is a measure, not a Finance actor/domain; and a shortage status record is evidence about a shortage case, not the medicine itself.

## 4. Minimal provenance chain
Every empirical assertion used in W6/W7 should be recoverable through a chain equivalent to:

`Canonical Assertion ← supportedBy ← Source Record ← containedIn ← Dataset Release ← releaseOf ← Dataset ← maintained/publishedBy ← Data Source`

For transformed assertions:

`Canonical Assertion ← generatedBy ← Provenance Activity ← used ← Source Record(s)`

For mappings:

`Canonical Entity/Assertion ← resultOf ← Mapping Assertion ← supportedBy ← Evidence Item/Source Record`

Exact relation names and PROV-O/SOSA alignments are deferred to W4/W5.

## 5. Reproducibility metadata required later
Each ingested source should eventually record:
- source registry ID (P1, P2, etc.);
- source URL/DOI/stable identifier;
- release/snapshot date and version;
- retrieval date;
- license/reuse status;
- raw artifact hash where redistribution/storage is permitted;
- transformation software/version/commit;
- mapping version;
- validation status;
- generated RDB/KG artifact version.

## 6. Provenance-aware query requirements
Demonstrator C should support questions such as:
1. Which source record(s) support this product/site/shortage assertion?
2. Which transformation/mapping generated this canonical entity or relation?
3. Which identifier mapping caused two source records to be merged?
4. Which dataset version was used for a reported metric/result?
5. Can an SQL row and a SPARQL result be traced to the same underlying source evidence?
6. Which assertions depend on conditional sources such as C1 or C2?
7. Which assertions come from held-out evaluation and therefore must not retroactively change the W3 Core inventory?

## 7. Standards alignment candidates for W4/W5
Evaluate rather than automatically import:
- **W3C PROV-O** for Entity/Activity/Agent provenance patterns.
- **SOSA/SSN** for observation/result patterns where semantically suitable.
- **Dublin Core / DCAT** for dataset/source metadata where useful.
- project-specific minimal mappings only when a standard pattern would distort the pharmaceutical semantics.

## 8. Evidence hierarchy for concept admission
Evidence strength is not reduced to a single numeric score. W3 uses a structured hierarchy:
- convergence across multiple primary/authoritative sources;
- one strong primary source plus V1/use-case requirement;
- one conditional source only — usually Extension/Conditional, not Core;
- V1-only concept — generally Extension/Deferred unless current evidence independently supports Core relevance;
- held-out-only structure — **cannot be admission evidence in W3**.

## Conclusion
Provenance is a first-class V2 research contribution because multi-source integration without source-level traceability would make later ontology↔RDB↔KG consistency and generalizability claims difficult to audit. The W3 inventory therefore treats evidence, observation and transformation semantics as cross-cutting infrastructure rather than optional documentation.
