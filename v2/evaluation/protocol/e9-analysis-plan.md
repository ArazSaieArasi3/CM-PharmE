# W7-E9 Expert Analysis Plan

## Analysis principle
Expert evidence is descriptive and criterion-specific. It is not merged into a single ontology-quality score and is not used to overwrite formal, dataset or held-out evidence.

## Quantitative summaries
For each 1–5 rating item report:
- number of valid responses;
- median;
- interquartile range;
- full category counts (1–5);
- favorable proportion (4–5);
- critical proportion (1–2).

When both expert strata have sufficient observations, report the same summaries separately for pharmaceutical-domain and ontology/conceptual-modeling experts. Do not infer population representativeness from a small purposive sample.

## Confidence handling
Item-level confidence is reported alongside substantive ratings. Low-confidence judgments are not deleted. Sensitivity analysis may show results with and without responses whose confidence is 1–2, but the primary table retains all eligible responses.

## Red-flag rules frozen before collection
A finding is flagged for mandatory adjudication when any of the following occurs:
1. a protected identity distinction is rated semantically incorrect (rating 1–2) by at least two eligible experts;
2. median semantic-adequacy or domain-relevance rating is <=2 for a principal module/distinction;
3. at least two independent experts identify the same missing concept/relation as critical to a principal intended use case;
4. at least two experts select `requires_material_refinement` or `not_suitable_for_stated_scope` and provide a convergent rationale.

A red flag is not automatically a failure. It must produce a traceable decision: revise, defer to extension, reject the suggestion with rationale, or bound the claim/limitation.

## Qualitative analysis
Open comments are coded into a controlled finding taxonomy:
- missing concept;
- missing relation;
- inappropriate distinction;
- terminology/clarity;
- scope/module boundary;
- identity/granularity;
- regulatory/jurisdiction context;
- provenance/data semantics;
- application/usability;
- other.

Each unique finding receives an ID and records: anonymous participant ID, stratum, affected term(s), severity (`minor`, `material`, `critical`), confidence, analyst decision, and post-review action.

## Inter-rater/validity statistics
No agreement statistic is mandatory. If sample size and item structure are adequate, supplementary ordinal agreement may be reported. I-CVI may be reported only for clearly relevance-oriented items and only as supplementary evidence; it is not used as the sole acceptance threshold.

## Missing data
- A participant who does not complete the minimum substantive sections is excluded from completed-response analysis, with count and reason reported.
- Item nonresponse is reported item-by-item; no imputation is performed.
- Open-text absence is not interpreted as agreement.

## Deviations
Any deviation from the frozen instrument, eligibility rules or analysis plan after first response collection must be entered in an `E9 deviation log` with date, reason, affected items and whether primary analysis was changed.

## Reporting boundary
The manuscript may claim that a prospective structured expert evaluation was performed only after real eligible responses have been collected and analyzed under this plan. Until then, the repository may state only that the protocol/instrument are frozen and recruitment-ready.
