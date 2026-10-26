# RDB-M3 manufacturer context — 0.4.0

Bounded implementation of #320 / ORSD FR-02. The contract, primary-source
extraction and independent oracles were committed before implementation at
`0508dc0cb5ce20856f3068abdbdb25c245dd0d13`. The current scientific gate remains
#306 and the integration PR #305 remains draft.

## Scope and semantics

See [semantic-contract.md](semantic-contract.md) for six delegated candidate
decisions. Existing Organization and MedicinalProduct identities are reused in
contextual ManufacturerRole and ManufacturingResponsibilitySubjectRole
participation. Every relator has exactly one holder and product counterpart;
multiple contexts preserve independent IDs, source assertions and dates.
There is no global organization/product uniqueness constraint.

The [FDA source witness](source-witness.json) supplies one explicit documentary
manufacturer attribution. The separately named commissioned-for party is a
negative-inference witness. The product ID is scoped to the document, not a global
brand/product identity match. A label supports the reported attribution; interpreting
it as the candidate relator is a bounded modeling decision pending #306 review.
It establishes no legal duty, executed manufacturing event, facility or batch.
Neither source revision nor retrieval time is a responsibility start/end date.

Three additional scenarios are **synthetic fixtures**: the same synthetic
organization participates in two product contexts and in two successive
assignments for one product. Their intervals are not empirical. Date-only fixture
values use the existing export convention of midnight UTC for query normalization;
they do not assert an observed event instant. The real witness has unknown dates.

## Reproduce

Use Python 3.12, Java 21, PostgreSQL 16 / PostGIS 3.4 and the dependency versions
pinned in `.github/workflows/v2-21-rdb-m3.yml`.

```sh
python tools/v2_data/bootstrap_ingest.py --reset --report build/v2-21-rdb-m3/ingest.json
python v2/data/migrations/2.1/0.4.0/verify_m3.py
```

Run only on a disposable copied database. An offline subset is also available:

```sh
python v2/data/migrations/2.1/0.4.0/verify_m3.py --offline --output-dir build/v2-21-rdb-m3-offline
python v2/data/migrations/2.1/0.4.0/verify_source.py --pdf /path/to/125514Orig1s186lbl.pdf
```

The offline command does not execute PostgreSQL, SQL constraints, legacy paired
queries or rollback. Its report explicitly marks that boundary. The source replay
checks the reviewed extraction offline; the optional PDF argument rechecks source
bytes and page attribution with Poppler. CI does not silently replace the source
with a newer label.

## Executed contract

- Q21-03 compares the complete 12-field normalized SQL/SPARQL tuple, including
  relator, parties, scope, intervals and source/assertion/evidence/run lineage.
- Eleven independent invalid SQL admissions check required participants/source,
  foreign keys, public identity, source/assertion uniqueness, dates and evidence
  alignment. The commissioned-for assertion must fail manufacturer admission.
- Eleven frozen SHACL expectations cover positives, cardinality, role context,
  type, source/evidence completeness and non-entailment. A separate supplemental
  mutation tests misaligned RDF assertion provenance.
- Six HermiT expectations distinguish closed-world admission from open-world
  consistency and show countermodels for unsupported manufacturer inference.
- Native role/relator/mediation anchors and exact typed `1` ends are checked.
- The existing four legacy SQL/SPARQL pairs run before/during/after the addition;
  W6 validation runs while the new data is present. Old output is unchanged after
  cleanup. All W6 base-table row/schema hashes and existing sequence states match.

M3 uses a new table plus a correlated evidence-validation trigger. Existing W6
schema/view/ontology defaults and the old exporter remain intact. Explicit,
collision-checked negative fixture keys prevent sequence advancement. Cleanup is
executed in a finally block after a successful seed transaction. This is a
reversible prototype, not an automatic production migration.

## Remaining release boundary

This slice does not implement importer/wholesale contexts, all 36 mappings, M025
EvidenceSupport's unapproved role interpretation, full anti-pattern validation,
ORSD content acceptance, author/expert review or 2.1 GA. Generic provenance links
preserve EvidenceSupport SQL identity without asserting its unresolved 2.1 type.
Source-backed documentary attribution is distinct from independently observed
manufacturing responsibility and must remain qualified in manuscript claims.

## Verified hosted outcome

[Run 40402255076](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40402255076) passed on implementation commit `79a4601cae90d8f4351b18ccce6db283eeb6d97d`. [hosted-results.json](hosted-results.json) records PostgreSQL/PostGIS execution; [ci-evidence.json](ci-evidence.json) pins 16 successful distinct workflow families, the run and evidence-artifact identity/digest. [offline-results.json](offline-results.json) remains separately labeled as the earlier local RDF-only subset. [source-verification.json](source-verification.json) records the original local PDF-byte/page recheck. [traceability.csv](traceability.csv) links FR-02 to the model, decisions, mapping, constraints, query, source and remaining review gate.

Result: Q21-03 4/4 complete tuples agree; 11/11 expected SQL rejections, 11/11 SHACL expectations, the separate provenance-alignment mutation and 6/6 HermiT expectations pass. Four legacy pairs pass at each phase and all pre-existing rows/schema/sequences and old canonical KG match after cleanup. This satisfies the bounded #320 contract. Candidate-wide scientific/author acceptance remains open.
