# W7-E4 Manuscript Notes — Competency Questions

## Evidence state
W7-E4 completed successfully under the frozen prospective protocol.

- CQ registry frozen before execution at commit `b96d7317aa1203a35c1282631a1cd19147f64007`.
- GitHub Actions run `32237841582`: SUCCESS.
- Evidence artifact ID: `9359621534`.
- Total frozen CQs: 18.
- Positive CQs: 8/8 PASS.
- Negative CQs: 10/10 PASS.
- Held-out H1–H3 used: false.

## Manuscript-safe result
A suitable bounded result statement is:

> Eighteen competency questions were specified and frozen before execution against the Gate-E reference fixture KG and asserted ontology. All 18 produced the predefined outcomes, comprising eight positive retrieval questions and ten negative regression/consistency questions.

The result should be immediately bounded by noting that the reference KG is schema-faithful synthetic fixture data, not the full external datasets.

## Negative-CQ interpretation
Negative ASK queries are used as regression/consistency checks. Under OWL open-world semantics, a `false` ASK result does not by itself prove that the queried pattern is impossible in the domain. Explicit logical impossibility/disjointness evidence belongs to the formal W7-E2 family.

## Claims strengthened by E4
- Product/Substance/Presentation distinctions are queryable on the populated reference graph.
- Facility/geography representation is executable.
- Dataset/release/source-record provenance traversal is executable.
- Entity-match/confidence representation is executable.
- Identifier-assignment resolution is executable.
- Observation results retain subject, time, geography and source provenance in the reference projection.
- EvidenceSupport connects source records and assertions in the reference graph.

## Claims not established by E4
- global domain completeness;
- held-out or cross-jurisdiction generalizability;
- real-world mapping accuracy;
- entity-resolution accuracy;
- application effectiveness;
- universal answerability across pharmaceutical ecosystem questions.
