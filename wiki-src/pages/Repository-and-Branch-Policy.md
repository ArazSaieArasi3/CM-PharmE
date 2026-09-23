# Repository and Branch Policy

> **Page scope:** Version-neutral governance  
> **Documentation maturity:** Candidate  
> **Last synchronized:** 2026-09-23  
> **Related issues:** #202, #210, #215  
> **Evidence status:** Repository/documentation governance

## Authoritative branches

- `main`: selected stable CM-PharmE 1.x authority.
- `v2/research-program`: selected CM-PharmE 2.0 research-integration authority.

Short-lived feature branches should support bounded changes and then be merged/retired through the normal issue → branch → PR → review/CI → merge path.

## Wiki source

The source-controlled Wiki package is maintained under `wiki-src/` in the main repository. Its purpose is to make documentation changes reviewable and reproducible before/alongside synchronization to the GitHub Wiki Git repository.

The source-controlled package does not alter the semantic authority hierarchy:
- ontology/model semantics remain in version-specific authoritative artifacts;
- evaluation results remain in their evidence artifacts;
- the Wiki remains explanatory/navigation material.

## Link policy

V1 pages should link to `main` unless a historical snapshot is intentionally cited.

V2 pages should link to `v2/research-program` unless a historical/feature branch is intentionally cited and clearly labeled.

A mutable branch link may be useful for navigation, but a claim/evidence audit should also record an exact commit/ref where practical.

## Status resolution

When an Epic body, Wiki summary and live child issue/PR disagree, current status must be resolved from live repository evidence before the Wiki is updated.

## Publication path

1. Author/revise under `wiki-src/`.
2. Review via branch/PR.
3. Run required Wiki QA.
4. Merge accepted source to `main`.
5. Synchronize the corresponding page files to the GitHub Wiki repository.
6. Verify rendered navigation and links.
7. Record the synchronization event in [[Wiki Update Register]].
8. Archive declared baselines under the #217 procedure.

Until step 5 is completed, a source page must not be falsely described as already published on the GitHub Wiki surface.
