# V2-080 → V2-083 Evaluation Handoff

Issue: #151
Tasks: T04 SQL↔SPARQL paired question; T05 governed analytic

## Evidence to consume in V2-083
- dedicated V2-080 hosted run on the exact merge-candidate head;
- freshly generated `sql-sparql-equivalence.json`;
- freshly generated bounded analytics JSON and HTML outputs;
- frozen registry `v2/data/queries/sql-sparql-benchmarks.json`;
- W7-E11 AN-08 evidence boundary.

## Representative-task assertions
1. all and only QREP-01..QREP-04 are executed;
2. each SQL answer equals the canonicalized SPARQL answer for the reference fixture;
3. dashboard output reports both SQL and SPARQL row counts and explicit provenance state;
4. the interpretation and semantic-source boundaries are visible in generated output;
5. no deferred analytics/AI candidate is presented as benchmark-supported.

## Deferred evaluation
V2-083 may assess representative-task correctness and provenance visibility. Successful generation/rendering alone is not usability or effectiveness evidence. No arbitrary-query, real-world completeness, predictive, causal, or AI claim is admissible from V2-080.