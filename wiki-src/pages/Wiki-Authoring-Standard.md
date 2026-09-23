# Wiki Authoring Standard

> **Page scope:** Version-neutral governance  
> **Documentation maturity:** Candidate policy  
> **Last synchronized:** 2026-09-23  
> **Related issues:** #202, #203, #204–#208, #215, #216

## Purpose

This standard defines the mandatory structure and evidence discipline for CM-PharmE Wiki pages.

## Mandatory metadata contract

Every substantive page must state, in a compact header or equivalent structured section:

1. **Page scope:** V1 / V2 / Cross-version / Version-neutral.
2. **Documentation maturity:** Stable / Stable-to-date-Evolving / Candidate / Frozen / Pending as applicable.
3. **Authoritative source branch/ref.**
4. **Last synchronized date.**
5. **Last synchronized commit/ref when available.**
6. **Related issue(s)/PR(s).**
7. **Evidence status.**
8. **Known pending refresh checkpoint(s), when applicable.**
9. **Wiki baseline identifier, once declared.**

Index-only pages may use a shorter header only when the linked entries themselves carry the required version/evidence information.

## Page classes

Use one of these page classes:
- Narrative / Research
- Concept / Domain / Model
- Evaluation / Evidence
- Cross-Version Evolution
- Reference / Index
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

Every non-decorative diagram/image should have:
- caption;
- version scope;
- source/provenance;
- generation/source file when available;
- note if illustrative rather than authoritative.

A diagram must not visually imply stronger semantics than its source model.

## Pending and deferred work

Use controlled wording:
- Stable in current V2 baseline
- Stable-to-date / evolving
- Under human review
- Evaluation pending
- Implementation pending
- Manuscript integration pending
- Deferred / future work
- Final/Frozen only after explicit final gate

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
- [ ] metadata is present;
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
