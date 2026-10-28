# M1 isolated provenance support profile — 0.1.0

This is the bounded #331 implementation for the approved small **2.1.0** release
strategy. It provides an isolated four-class/two-property vocabulary, explicit
opt-in admission checks, the unchanged M1 SPARQL query and reproducible synthetic
tests. It does not publish the ontology or complete copied-W6 integration.

## Contents and exact support boundary

| Artifact | Meaning |
|---|---|
| profile.ttl | 50 triples: the 30 unchanged selected defining triples, necessary declarations and attributed/versioned profile metadata; no owl:imports |
| shapes.ttl | 143 triples; direct targetClass shapes for Dataset, DatasetRelease, SourceRecord and ProvenanceActivity; link-subject/object targets also catch missing types |
| profile.py | Standalone admission: SHACL, nonempty declared scope and composite/public-ID consistency; no DB, Java or historical model needed |
| query.rq | Byte-identical historical Q21-01 / PAIR_SPARQL; full RDF values remain queryable |
| incoming-axioms.csv | Five outside-signature incoming references explicitly excluded; no full-source semantic-module equivalence claim |
| contract.json, fixed-oracles.json, fixtures/ | Pre-implementation frozen contract and 24 synthetic positive/negative/boundary witnesses |
| verify_profile.py | Roundtrips, fixed query tuples, coverage/import guards, standalone CLI and bounded OWL checks |

Contract/oracles/fixtures were frozen at **699bd799c0c0234e9ded1422de83885c9bde24bb**
before the verifier implementation. Their hashes and the original source pins
are checked on every verification. Historical P3, M1, W5/W6, detector reports,
the modern native model and published RC stay unchanged.

## Use the opt-in admission profile

```bash
python -m pip install -r v2/ontology/profiles/2.1/m1-provenance/0.1.0/requirements-runtime.txt
python v2/ontology/profiles/2.1/m1-provenance/0.1.0/profile.py admit path/to/export.ttl
```

Exit 0 means the selected export profile is admitted; exit 1 reports the failed
stage. Runtime needs only profile.py, profile.ttl and shapes.ttl, with query.rq
available for the unchanged query. The portability check copies those four files
to a fresh temporary directory and successfully exercises admission/rejection
without copying repository or historical source files.

This is a profile for the **M1 export contract**, not a requirement that all
datasets or organizations everywhere carry these fields. Each selected record
has its owning release, integer row and opaque nonempty source-hash value, with
the existing canonical JSON composite key and percent-encoded IRI. A generating
run is optional. Extra metadata remains allowed. No guessed positive-only row
bound, digest algorithm, global owl:sameAs or universal OWL cardinality is added.
The SQL source still has its own CHAR(64) column; accepting an opaque profile
witness does not establish arbitrary SQL-row admission.

## RDF payload and the strict OWL view

The historical export stores the row number using **rdf:value**. That reserved
IRI cannot be declared as a custom OWL 2 DL data or annotation property. Both
declaration probes were refused by OWLAPI; the normative restriction is in
[W3C OWL 2 sections 2.4 and 5.4–5.5](https://www.w3.org/TR/owl2-syntax/).

The raw RDF export is retained intact for SHACL, identity checks, roundtrips and
the unchanged SPARQL query. `logical_view` explicitly excludes only rdf:value
serialization triples from the strict OWL view and reports their count. It does
not rename that field, rewrite the query, drop other assertions or claim a
lossless full-RDF-to-OWL conversion. The isolated TBox and the declared logical
positive witness pass OWLAPI's OWL 2 DL profile and Pellet consistency checks.
Five HermiT cases include the explicit inconsistent owl:Nothing control. Missing
record-key data and local export-kind aliasing remain logically consistent under
the limited OWL axioms while the opt-in data profile rejects them.

## Verification and claim limits

```bash
python -m pip install -r v2/ontology/profiles/2.1/m1-provenance/0.1.0/requirements-verify.txt
python v2/ontology/profiles/2.1/m1-provenance/0.1.0/verify_profile.py
```

Formal verification additionally requires Java 17 and the existing repository
OWLAPI helper. Reports/logs are written to build/m1-provenance-profile. The
dedicated `CM-PharmE 2.1 M1 Isolated Core` workflow repeats the bounded checks in a
fresh Python/Java environment and uploads its report.

The 24 admission oracles comprise eight accepted synthetic cases and sixteen
expected refusals (SHACL, identity or empty-scope). Reports record each shape's
explicit target-union count, four-format roundtrips and every accepted case's
frozen query tuples. Missing targets and an implicit whole-model import are
independently refused. Local/hosted evidence must keep its exact commit/runtime
scope; these are not expert samples or a full ontology conformance score.

The next packet replays an isolated copied-W6 database through this profile,
compares old/new SQL↔SPARQL tuples and verifies default-schema/data preservation.
Only then proceed to new GA bundle/replay and reviewed publication. Full native
20-family, remaining source-policy/module/ORSD/expert work remains separately
tracked; no new scientific acceptance is inferred here.

## Verified checkpoint

Implementation `42708dc83599a84d161631ccf6d4960189a54581` passed the direct push
[run 40734338360](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40734338360).
[hosted-execution.json](hosted-execution.json) identifies the actual tested commit;
[hosted-results.json](hosted-results.json) and [local-results.json](local-results.json)
agree on the sixteen normalized fields in
[local-hosted-comparison.json](local-hosted-comparison.json). The primary ZIP
digest matches GitHub's artifact digest. [ci-evidence.json](ci-evidence.json) keeps
the exact run/job/artifact identifiers and distinguishes the PR merge tree.
#331's bounded exit is complete; [#332](https://github.com/ArazSaieArasi3/CM-PharmE/issues/332)
is the next separate copied-W6 integration packet.

Original project ontology, shapes, fixtures and documentation in this new profile
are offered under CC BY 4.0; original Python code is MIT under approved D-03.
See [NOTICE.md](NOTICE.md). No external runtime/data or historical RC is relicensed.
