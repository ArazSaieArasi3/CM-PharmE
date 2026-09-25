# V2 Provenance and Evidence Flow

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-25

CM-PharmE keeps **source lineage**, **assertion support**, **domain observations** and **entity-match assertions** separate so that provenance and uncertainty remain inspectable.

![DGM-ARC-005 Provenance evidence flow](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/architecture/DGM-ARC-005--provenance-evidence-flow.svg?sha=5ffa2749e9e8)

## Primary lineage

The implemented lineage starts with **Dataset → DatasetRelease → SourceRecord**. A SourceRecord may reference a **TransformationRun** that records the adapter execution which generated the admitted row.

A SourceRecord stores a deterministic `source_hash`, row number and `raw_key`. The hash is a content fingerprint used for traceability; it is not an entity identifier.

## Evidence support

An **Assertion** is the auditable proposition target. **EvidenceSupport** is the first-class relator linking a SourceRecord to an Assertion.

In the W6 fixture path, each admitted reimbursement-utilisation row creates:
- one SourceRecord;
- one Assertion;
- one EvidenceSupport relation;
- one relational ObservationResult aggregate.

The generated RDF graph retains SourceRecord and Assertion nodes and represents EvidenceSupport explicitly.

## Entity-resolution boundary

**EntityMatchAssertion is an assertion about two source records, not proof that the records are the same entity.**

The relational record preserves:
- both source-record endpoints;
- proposed matched entity type and public ID;
- matching method;
- numeric confidence;
- disposition: `accepted`, `ambiguous` or `rejected`.

W6 contains two accepted exact matches for the deterministic fixtures. This does not support precision/recall/F1 claims for real-world entity resolution.

## Queryable provenance

The reference view `cmpe.v_provenance_lineage` joins Assertion → EvidenceSupport → SourceRecord → DatasetRelease → Dataset and optional TransformationRun.

The bounded API also exposes `GET /v1/provenance/records/{source_hash}`.

## Related reference

- [[V2 Table source_record]]
- [[V2 Table assertion]]
- [[V2 Table evidence_support]]
- [[V2 Table entity_match_assertion]]
- [[V2 End-to-End Data Trace]]
---
<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 W6 data/representation artifacts and W7 E10 evidence
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- **Related issues/PRs:** #228, #236, #237
- **Evidence status:** Reference implementation evidence; production/full-ingestion claims excluded
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
