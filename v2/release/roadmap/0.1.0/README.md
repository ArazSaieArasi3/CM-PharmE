# Incremental release roadmap — planning record 0.1.0

**Current state: scope proposal awaiting Araz. GA readiness remains HOLD.**
Planning task [#328](https://github.com/ArazSaieArasi3/CM-PharmE/issues/328).
Source checkpoint `30c86fc4e7578593883315d9bb6f2eebc46a68d4`, 2026-10-28
Asia/Tehran. This record implements the requested backlog/operating organization;
it does not amend the original seven GA groups, approve a scientific decision,
adopt a license or publish another version. Published experimental
[2.1.0-rc.1](https://github.com/ArazSaieArasi3/CM-PharmE/releases/tag/2.1.0-rc.1)
remains unchanged.

## Mission and intended uses

CM-PharmE is an ontology-grounded shared conceptual and computational layer for
the pharmaceutical ecosystem: organizations, products/substances, facilities,
contextual roles, operations, governance, collaboration, supply and digital/evidence
dependencies. Business-architecture concerns guide coverage; UFO/OntoUML clarifies
identity, dependence and relation meaning. Global extensibility is a design goal,
not a claim of universal data coverage or verified regulation in every country.

| Use | Intended value | Boundary |
|---|---|---|
| Shared ecosystem/reference model | Consistent concepts and traceable cross-domain relations | No universal completeness claim |
| Relational databases and mappings | Explicit identity/context and SQL↔SPARQL consistency | Ontology axioms are not copied blindly into SQL constraints |
| RDF/OWL/SHACL and knowledge graphs | Interoperable identifiers, inference and scoped data validation | Supported profiles and evidence are versioned separately |
| Governance, supply/risk and architecture analysis | Connect actors, activities, capabilities and evidence | No legal-compliance or predictive/causal certificate |
| Observatory, semantic search and later AI applications | Explore/query with source provenance | Implemented tasks differ from product readiness or measured AI utility |
| Research/reproducibility | Source-to-claim traceability and immutable evaluated artifacts | Author/expert acceptance remains actual human evidence |

## What the live backlog actually contains

At the source checkpoint: **29 open issues, 4 open PRs, five explicit open epics
and one program**. None of those 29 issues has a GitHub milestone. Existing
release scope/build/replay/publication machinery works, but it is not a complete
recurring-release governance system. Missing links are an approved support cut,
explicit release allocation, ready-sized children and a regular release-cut rule.

| Workstream | Existing epic/program/coordination | Original open issues | Proposed emphasis |
|---|---|---:|---|
| Core, native validation, sources and release | Program #24; coordination #306; #310/#315 | 4 | Minimum accepted support cut in 2.1; broader native/data work incrementally later |
| RM/PV/BA/DS modules | #311–#314 under #306; not formal EPIC titles | 4 | Preserve experiments; promote one approved capability at a time from 2.2 |
| Human/scientific evaluation | Epic #21; register #103; #98/#159/#173 | 5 | Scoped author decisions before supporting the chosen core; broader expert track in 2.3 |
| Applications | Epic #22; #170 | 2 | Observatory/task evaluation independent of core publication |
| Paper/research release | Epic #23; #171 | 2 | Evidence-backed manuscript increments and later research freeze |
| Documentation | Epics #202/#228 and their retained children | 12 | Minimum support docs in 2.1; full portal/editorial/scoring thereafter |

[backlog.csv](backlog.csv) maps every original issue once. The six workstreams
are an operational view, not six newly created epics. Parent/child overlap must
not be counted as independent remaining release blockers. Open PRs are recorded
in [pull-requests.csv](pull-requests.csv): #305 native candidate (draft), #172
manuscript (draft), #201 observed RT-03 task evidence, and #308 Productium case
explorer (draft). **#308's Product Knowledge fixture browser is distinct from the
CM-PharmE W8 Observatory** and is not a new prerequisite for the ontology GA.

Two immediate child issues add to the backlog: #329 (RelComp author disposition)
and #330 (core contract inventory). After closing only the completed planning
task #328, expected open issue count is **31**: 29 retained originals + 2 bounded
children. This is sizing/traceability, not an increase in scientific work or a
readiness percentage.

## Proposed release sequence

| Version | Goal and proposed cut | Intentionally later |
|---|---|---|
| 2.1.0 | Exact accepted stable-core contract, compatible provenance/mapping path, truthful minimal docs and tested new release | Full modern-native validation, all modules, broader mappings, expert study and full portal/product completion |
| 2.1.x | Compatible fixes when actually needed | New semantics/functionality receives the appropriate minor/major version |
| 2.2.0 | The next completed compatible domain/native/data capability; not all the priority bucket at once | Further modules/mappings ship in subsequent eligible increments |
| 2.3.0 | Selected cross-context data/application capability and stronger evaluation | Paper/expert/docs remain their own evidence lanes; doc-only results do not force a minor bump |
| 3.0.0 | Reviewed integrated generation where intentional incompatible restructuring is justified | Migration and semantic change review required; maturity alone is not a major change |
| 4.0.0 | Optional longer-term horizon for future justified incompatible evolution | No committed features/date or prerequisite for 2.1 today |

The next core manifest audit starts from the frozen W5/W6 research contract and
bounded M1 provenance path. Its exact import closure and defects are not yet
inventoried. [requirements-allocation.csv](requirements-allocation.csv) accounts
for all 83 contracts: four functional audit seeds + twelve scoped quality rows
proposed for 2.1, 61 functional rows proposed for 2.2 and six for 2.3. All 83
scientific-review states remain pending. These are initial allocations, not
passing scores or an authorization to ignore a required dependency. The 2.2/2.3
rows are priority buckets; each actual release selects its own small coherent cut.

## Nondeferrable exit for the proposed 2.1 cut

1. Araz approves the strategy and the later exact supported manifest/claim scope.
2. The retained semantic/dependency closure has no unresolved critical defect;
   relevant author decisions are actual, and tool applicability is explicit.
3. Selected functional/quality contracts have required evidence and dispositions;
   affected current native/formal/admission/query/compatibility checks pass.
4. Supported imports/IRIs/definitions, DB mapping outputs, limitations, notices,
   minimal usage and reproduction instructions are explicit and version-aligned.
5. A new exact-commit release is assembled, independently replayed and reviewed;
   tag and downloaded assets are verified. Never relabel the RC archive as GA.

The original [GA inventory](../../2.1/ga/0.1.0/README.md) remains authoritative
until a recorded D-01 scope amendment. Deferring a claim is not correcting a known
critical defect or closing its original issue. The four modules remain preserved;
this plan does not delete or transfer them.

## Size, decisions and continuous delivery

[packets.csv](packets.csv) turns the retained work into small outcomes with
dependencies, S/M- scope and completion evidence. S means one audit/decision/
contract; M- means one coherent implementation plus its affected checks. They are
scope estimates, not guaranteed elapsed times or a fixed number of future turns.
Repeated families (one association/requirement/mapping/page) create separately
numbered children just in time; the first row is not all members completed.

- One active execution; at most three ready child issues. Larger issues remain
  rollups. If discovery expands scope, checkpoint the exact result/blocker and
  split before adding work. Closure requires the original child's actual exit.
- The assistant handles evidence, options, implementation and appropriate checks.
  Araz decides concrete scientific/release-scope/rights choices. Bring a concise
  recommendation, alternative, benefits, costs and exact approval effect.
- After **2–4 accepted packets**, inspect the smallest eligible release cut. Ship
  a meaningful eligible change; keep working if none meets the scoped gates.
  No automatic publication, promised weekly delivery or scheduled task is created.
- Use the existing builder/replay/publication method as reusable machinery; each
  new scope needs its own exact manifest/checks and release receipt. Reuse prior
  evidence only at its pinned scope. Do not add a recurring workflow merely to
  count issues or fabricate releases.

## Semantic version and compatibility rule

Keep MAJOR.MINOR.PATCH: compatible corrections → PATCH; compatible capability/
semantic additions → MINOR; incompatible public-contract changes → MAJOR. Public
contract includes IRIs/definitions/axioms, selected shape behavior, declared DB
mapping/query outputs and supported imports. New axioms can invalidate old data
or entailments even if they only add triples: an additive diff is not proof of
compatibility. Stricter default SHACL/SQL constraints or changed identity/domain/
range/cardinality can break consumers. New strict opt-in profiles get a separate
named/versioned contract. Paper status and maturity do not choose the version.

There is no invented published stable 2.0.0: v1.0.0 is the historical stable model
record; W5 formal 2.0.0-alpha.1 is a research baseline. The move into 2.x is a new
major generation relative to 1.x; compatibility promises for the declared 2.0
research consumers must still be tested. Do not create missing historical tags.
Preserve every published version. Use a new alpha/beta/rc suffix when needed;
documentation planning record 0.1.0 is not an ontology release number.

## Immediate next work and decisions

**First substantive follow-up: #329 / RC-001, the prepared RelComp decision**;
this is deliberately retained from the previous checkpoint. #330 / CORE-001 is
the next bounded manifest audit and may proceed read-only if a human decision is
pending. The best current recommendations and tradeoffs are in
[decision-proposals.md](decision-proposals.md). D-01 release strategy and the
RelComp scientific option require separate explicit dispositions. D-02's global/
profile design direction is authorized by the prompt; individual semantic edits
are not pre-approved. D-03 concerns actual rights/owned assets, not a blanket grant.

[release-plan.json](release-plan.json), [sources.json](sources.json), and
[validation.json](validation.json) make this plan inspectable. Run
`python v2/release/roadmap/0.1.0/verify_plan.py` for the static inventory and
preservation audit. It does not rerun the ontology, collect expert evidence or
turn HOLD into GA-ready. Milestone creation/assignment is an explicit next
governance packet after scope approval; no GitHub milestones are claimed here.
