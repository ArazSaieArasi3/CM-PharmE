# CM-PharmE 2.0 Human Review — Disposition Log

Issue: #159  
Scope: CM-PharmE 2.0 only  
Status: review-record scaffold; no human dispositions recorded yet

## Purpose

Provide one controlled place to record actual author/reviewer decisions for the 87-concept provenance matrix and the risk-first queue. This artifact records review outcomes only after a real review occurs; it must never pre-populate approval, expert evidence, or semantic changes.

## Governing boundaries

- Gate-D remains the frozen conceptual baseline until an explicit reviewed change is approved.
- `main` and CM-PharmE 1.x are out of scope.
- A row in the risk-first queue is a prioritization signal, not a defect finding.
- Evidence-gap class is not itself a semantic disposition.
- Human/author review is distinct from E9 prospective expert evaluation and must not be reported as expert-validation evidence unless the actual reviewer role and protocol support that claim.
- Any semantic change after Gate D must be routed to a separate V2 design-decision issue before OWL/SHACL/RDB/KG artifacts are changed.
- Missing evidence remains `G1`–`G9`/bounded rather than being filled by inference.

## Allowed disposition vocabulary

| Disposition | Meaning | Automatic ontology change? |
|---|---|---|
| `APPROVE` | Current semantic commitment accepted for the reviewed scope. | No |
| `APPROVE_WITH_WORDING_CHANGE` | Semantics accepted; definition/claim wording must be bounded or clarified. | No |
| `REVISE_SEMANTICS` | Current semantic commitment requires a governed design change. | No — create/link design-decision issue first |
| `SPLIT_MERGE` | Concept identity/granularity requires explicit redesign. | No — create/link design-decision issue first |
| `MOVE_DOMAIN_MODULE` | Semantic ownership/domain or module placement requires review-controlled change. | No — create/link design-decision issue first |
| `DEFER` | Decision intentionally postponed with reason and claim impact recorded. | No |

## Review record schema

Each completed review record must contain all fields below. Use one row per concept per review round; later rounds append rather than overwrite earlier judgments.

| Field | Required | Rule |
|---|---:|---|
| `review_record_id` | yes | Stable ID, e.g. `HR-0001` |
| `concept_iri` | yes | Stable V2 IRI from the provenance matrix |
| `concept_label` | yes | Current human-facing canonical label |
| `domain` | yes | Current canonical domain |
| `review_round` | yes | Integer starting at 1 |
| `reviewer_role` | yes | `AUTHOR`, `DOMAIN_REVIEWER`, `ONTOLOGY_REVIEWER`, or other explicit role |
| `reviewer_id` | yes | Named author or pseudonymous reviewer ID as appropriate |
| `review_date` | yes | ISO date |
| `primary_gap` | yes | `G0`–`G9` from the provenance-gap register |
| `evidence_checked` | yes | Exact repository artifacts/source locators reviewed |
| `disposition` | yes | One controlled value above |
| `rationale` | yes | Concise semantic/evidence rationale |
| `claim_boundary` | yes | What can and cannot be claimed after this review |
| `semantic_change_required` | yes | `YES` or `NO` |
| `follow_up_issue` | conditional | Required when semantic change or unresolved material work is routed onward |
| `resolution_evidence` | conditional | Commit/PR/artifact only after resolution exists |
| `status` | yes | `OPEN`, `RESOLVED`, or `DEFERRED` |

## Recorded dispositions

No real review dispositions are recorded in this scaffold.

| Review ID | Concept | Domain | Round | Reviewer role / ID | Date | Gap | Disposition | Semantic change? | Follow-up | Status |
|---|---|---|---:|---|---|---|---|---|---|---|
| _none yet_ |  |  |  |  |  |  |  |  |  |  |

## Risk-first queue completion ledger

The 19 rows in `human-review-high-risk-queue.md` are considered reviewed only after a real disposition record exists here or in a directly linked successor artifact.

- P0 reviewed: **0/6**
- P1 reviewed: **0/10**
- P2 reviewed: **0/3**
- Risk-first total reviewed: **0/19**
- Full 87-concept review: **0/87** recorded here

These zero values are factual initialization, not a quality judgment.

## Per-review checklist

Before recording a disposition:
1. inspect the row in `human-review-concept-provenance-matrix.md`;
2. inspect its `G0–G9` gap state and relevant bounded evidence packet;
3. inspect current definition, OntoUML stereotype, V1 lineage and stable formal IRI;
4. inspect dataset/official-source, literature/ontology and held-out evidence actually linked for the row;
5. separate semantic adequacy from evidence completeness and claim strength;
6. record the reviewer identity/role and real date;
7. append the disposition without overwriting prior review rounds;
8. if semantics change, create/link the design-decision issue before any formal implementation delta.

## Exit criteria for #159 review recording

The review-recording component is complete when:
- all 87 concepts have at least one real author/reviewer disposition or an explicit deferred state;
- all 19 risk-first rows have explicit dispositions;
- every semantic-change decision is traceable to a follow-up issue and resolution artifact;
- evidence gaps remain visible after review rather than being silently converted into support;
- publication wording reflects the strongest evidence actually available.

This artifact alone does not close #159 and does not constitute prospective expert evaluation.