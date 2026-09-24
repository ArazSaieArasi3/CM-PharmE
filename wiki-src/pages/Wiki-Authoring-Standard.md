# Wiki Authoring Standard

> **Page scope:** Version-neutral governance  
> **Documentation maturity:** Stable governance policy  
> **Last synchronized:** 2026-09-23  
> **Related issues:** #202, #203, #204–#208, #215, #216

## Purpose

This standard defines the mandatory structure and evidence discipline for CM-PharmE Wiki pages.

## Mandatory metadata contract

Reader-facing pages use progressive disclosure.

### Compact reader header

Normal Narrative, Navigation, Concept/Model, Evaluation, Evolution and Reference pages expose only:

1. **Version scope** — V1 / V2 / Cross-version / Version-neutral.
2. **Status** — the truthful documentation/evidence maturity.
3. **Updated** — last synchronization date.

### Documentation record

The complete operational provenance moves to a collapsible **Documentation record** near the end of the page. It must retain or provide:
- Page scope;
- Documentation maturity;
- authoritative source branch/ref;
- last synchronized date;
- last synchronized commit/ref when available;
- related issue(s)/PR(s);
- evidence status;
- pending refresh checkpoint(s), when applicable;
- Wiki baseline identifier.

Status/Governance and Status/Changelog pages may retain expanded metadata at the top because operational state is their subject.

The canonical progressive-disclosure policy is maintained at `wiki-src/editorial/progressive-metadata-contract.md`. Metadata must be relocated, not discarded.

## Page classes

Use one of these page classes:
- Narrative / Navigation
- Narrative / Research
- Concept / Domain / Model
- Evaluation / Evidence
- Cross-Version Evolution
- Reference / Index
- Status / Governance
- Status / Changelog

Templates are maintained under `wiki-src/templates/`.

## Naming and slug rules

- Use descriptive English titles.
- Prefer stable nouns over temporary task language.
- Use hyphenated file names corresponding to stable Wiki page slugs.
- Do not put issue numbers in canonical end-user page names.
- Version-sensitive pages must make version visible either in title or metadata.
- Renamed pages require an explicit redirect/deprecation note in the source manifest/navigation.

## Version discipline

- V1 facts come from `main`.
- V2 facts come from `v2/research-program`.
- Never present V2-only concepts, counts or evidence as V1.
- Never describe V2 as final while its final freeze gate is unresolved.
- Cross-version pages must distinguish continuity, refinement, renaming/repackaging, semantic change and genuinely new contribution.

## Reader-facing terminology and provenance

Reader-facing documentation should use descriptive scientific/technical language first. Internal workstream, Gate, issue, PR, branch and review-control identifiers are retained as provenance, not as vocabulary a reader must learn before understanding the project.

Required practice:
- use descriptive research-stage names before W0–W8 identifiers;
- use descriptive decision names before Gate A–H identifiers;
- use **Semantic Review** or **Ontology Review** as the public-facing review label unless the fact of human/expert review is itself methodologically important;
- keep exact historical/internal names when linking repository artifacts whose canonical filenames/titles contain them;
- place internal identifiers in provenance/history, parenthetical audit notes or technical-reference columns;
- do not remove a limitation, warning, pending state or evidence link merely to simplify prose.

The canonical terminology policy is maintained at `wiki-src/editorial/reader-facing-terminology.md`.

## Evidence discipline

A claim-bearing paragraph must be traceable to authoritative repository evidence, a publication, or a clearly identified external source.

Do not:
- convert a protocol into a result;
- convert an open issue into an achieved result;
- suppress negative/partial findings;
- infer generalizability, production readiness, regulatory compliance, clinical effectiveness or AI performance beyond evaluated evidence;
- use numerical “improvement” language where V1/V2 denominators are not comparable.

## Definition discipline

Wiki definitions synthesize authoritative model material for readability; they do not become a competing semantic source.

When meanings differ across versions:
- label both meanings;
- link each to its own authority;
- explain the migration/evolution relation.

## Citations and external references

For an external reference include enough context to identify it: author/organization, title, year/date where known, and durable link/DOI where available. Repository-internal evidence should link to the exact branch/path appropriate to the version.

## Diagrams and images

Diagrams are governed documentation artifacts. The complete policy is maintained in `wiki-src/diagrams/STYLE-GUIDE.md` and the reader-facing [[Diagram Standards and Inventory]] page.

Every non-decorative diagram/image must have:
- title and purpose;
- version scope;
- explicit notation;
- source/provenance;
- version-controlled editable source;
- SVG or equivalent publication artifact;
- authoritative / authoritative projection / illustrative status;
- generation method/tool;
- checked ref / last updated;
- caption and accessible alt text;
- related Wiki page(s).

Notation must match the documentation problem:
- ontology/conceptual model → OntoUML/UFO-aware or explicitly defined ontology notation;
- relational model → Crow's Foot ERD / relational notation;
- data/query pipeline → data-flow/architecture notation;
- software/application architecture → C4 where appropriate;
- research/evaluation process → process/activity notation;
- cross-version change → lineage/evolution notation.

C4 must not be used as ontology notation. ERD must not substitute for conceptual ontology semantics. A diagram must not visually imply stronger semantics than its authoritative source.

## Pending and deferred work

Use controlled wording:
- Stable in current V2 baseline
- Stable-to-date / evolving
- Semantic review in progress
- Evaluation pending
- Implementation pending
- Manuscript integration pending
- Deferred / future work
- Final/Frozen only after an explicit final research-release decision

Internal Gate identifiers may be retained in provenance, but they should not be required to interpret these statuses.

## Duplication policy

The Wiki should synthesize and navigate rather than copy large blocks from README, docs or manuscripts. Prefer:
1. concise explanation;
2. current interpretation/status;
3. authoritative links;
4. cross-links to related Wiki pages.

## Deprecation and redirects

When a page is renamed:
- preserve old-page discoverability with a short deprecation/redirect notice where GitHub Wiki behavior permits;
- update Home and Sidebar;
- update inbound links;
- log the rename in the update register;
- do not silently reuse an old slug for a different meaning.

## Authoring checklist

Before considering a page complete:
- [ ] compact header or governance metadata is present;
- [ ] full Documentation record/provenance is present for reader-facing pages;
- [ ] version scope is correct;
- [ ] source ref is correct;
- [ ] claims are evidence-linked;
- [ ] pending work is labeled;
- [ ] terminology matches authoritative artifacts;
- [ ] internal links resolve in source;
- [ ] no stale issue/PR state is encoded;
- [ ] diagrams have provenance/captions;
- [ ] relevant index/navigation links are bidirectional;
- [ ] update register impact has been considered.


## Generated ontology reference

Exhaustive V2 module/concept/property reference pages are **generated projections**, not semantic authorities.

Rules:
- generated pages must identify the V2 authority ref;
- conceptual counts and formal OWL counts must remain distinct;
- missing OWL domain/range constraints remain `unspecified`;
- generated pages may expose registered evidence and review state but may not approve semantics;
- curated explanatory pages remain responsible for interpretation, evolution and evidential boundaries;
- semantic changes flow through #213 and trigger regeneration rather than direct leaf-page editing;
- `tools/wiki/check_ontology_reference.py` must pass before publication.

Canonical architecture and authority rules live under `wiki-src/ontology-reference/`.
