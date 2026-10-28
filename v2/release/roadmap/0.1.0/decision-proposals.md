# Concrete decisions and tradeoffs

All options below are recommendations based on the current evidence and Araz's
stated priorities, not claims of a uniquely optimal answer. This package adopts
the requested operating direction; it does not record a new scientific approval.

| ID | Recommended choice | Main benefit | Cost / alternative | Actual decision needed |
|---|---|---|---|---|
| D-01 | A small stable 2.1.0 core, with unaccepted native/domain/empirical/product work separately experimental and retained for later releases | Shortens the critical path and creates a usable supported contract | Less scope than the whole research candidate; needs an exact dependency/compatibility manifest. Alternative: retain all original gates before any GA | Approve this release strategy; accept the concrete manifest later after CORE-001/002 |
| D-02 | Universal identity/meaning in core; jurisdiction/source/application completeness and implementation constraints in opt-in profiles | Global reuse and multiple RDB/KG implementations | Applications must select profiles. Alternative: one rigid global schema | Direction already authorized by this prompt; each actual axiom/cardinality delta remains reviewable |
| D-03 | After rights inventory, CC BY 4.0 for owned ontology/docs and MIT for owned code; preserve third-party terms | Clear reuse path and research attribution | Requires actual authority/ownership boundaries. Alternative: current per-asset notices pending clarification | Confirm rights-holder authority and preferred grant before any adoption |
| SC-REL | Retain the existing named positive-lower/shared-ATarget profile and explicit optional-example disagreement | Preserves source/engine boundaries and avoids an arbitrary global restriction | Example/text tension remains disclosed. Alternative requires a new separately versioned policy/oracle | Actual RC-A01/RC-A02 ACCEPT/REVISE/DEFER with rationale, separately from D-01 |

## The 2.1.0 cut proposed for inventory

Start from the frozen W5/W6 research contract, then assess the already tested M1
Dataset → DatasetRelease → SourceRecord/ProvenanceActivity path as a compatible
addition. This is a seed for the next exact manifest audit, not an assertion that
every historical result/IRI has approved new semantics. Four functional seeds
(FR-01, FR-02, FR-25, FR-28) and all twelve scoped quality obligations are listed
in [requirements-allocation.csv](requirements-allocation.csv). Sixteen assigned
rows are not sixteen passing or approved contracts and are not a complete import
closure. If identity, time, jurisdiction, conflicting claims or other dependency
semantics are needed, bring the relevant retained contract into the cut before
approval; a table assignment cannot authorize an inconsistent subset.

The modern 536-element native research model and four module experiments remain
preserved and distinctly labeled. A stable core entrypoint must not import their
unfinished changes implicitly. The published RC remains an immutable research
checkpoint. The same package may contain experimental artifacts only under an
explicit separate support boundary; an all-source tar is not itself that boundary.

No known critical defect in the retained closure can be deferred as mere future
improvement. Semantic choice review, affected formal/data/query checks, exact
current compatibility, distributed-asset notices and truthful support docs remain
required. A selected verified core release is not acceptance of the whole model.

## Why separate ontology and implementation constraints

OWL logical existence/cardinality is not a syntactic data-presence or SQL
NOT NULL rule. Use explicit profiles for such decisions. For example, a
particular import may require a source-record identifier and reject incomplete
rows, while an abstract organization in the global core need not carry every
country's registry number. Unknown information stays unknown; the selected
application can still require enough information for its own task.

Do not weaken essential identity/dependence, silently replace every lower bound
with zero, or call unconstrained terms a useful ontology. Generalization needs
source/CQ/counterexample review. Mappings record any information loss and keep
provenance, jurisdiction and time where relevant. W3C references are pinned in
[sources.json](sources.json); no SHACL 1.2 draft migration is proposed.

## RelComp is a detector interpretation, not a new universal minimum

[The existing scientific card](../../2.1/ga/0.1.0/relcomp-review.md) preserves the
text/example/archive tension. RC-A01 retains the positive-lower named detector
profile (explicit min > 0, max > 1 at the selected shared ATarget), while the
optional 0..* example is still recorded separately. RC-A02 retains explicit role
binding and supported-frame/refusal limits. A non-match does not prove a model
correct, and accepting this profile does not force every association to min=1.
No new source-table re-review, model execution or author response is claimed.

## Recording an approval

Use separate decision IDs, actual author response/identity/date, exact option,
rationale, accepted limits and affected artifacts. A generic approval of the
roadmap does not adjudicate all four source policies or all 83 ORSD rows. If a
choice changes, preserve the old evidence and publish a new profile/contract.
