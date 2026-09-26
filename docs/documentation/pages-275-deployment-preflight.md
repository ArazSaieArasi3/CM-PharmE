# PAGES-08 Deployment Preflight and Trigger Contract

Issue: #275  
Parent: #267

## Slice 1 objective

Create a **deploy-ready but not yet publicly deployed** Pages artifact with a source-controlled separation between:
1. change classification / trigger policy;
2. governed semantic build;
3. static-site assembly;
4. deployment preflight;
5. Pages artifact upload;
6. public deployment;
7. post-deployment rendered verification.

This slice implements 1–5 and scaffolds 6 with an explicit source-controlled lock. Step 7 remains a later #275 slice.

## Current deployment lock

`docs/documentation/pages-deployment-policy.json` sets:

`public_deploy_enabled: false`

Therefore ordinary PR/push builds cannot publish the site. The deploy job is additionally restricted to:
- manual `workflow_dispatch`;
- explicit `deploy=true`;
- `main` branch;
- source-controlled deployment authorization.

The lock is intentionally retained until Pages is enabled with **GitHub Actions** as the publishing source and WebVOWL/public rendered-verification prerequisites are ready.

## Path-aware / cost policy

Full Pages candidate builds are requested for changes to:
- governed V1 semantic source/build evidence;
- documentation/version/surface contracts;
- Pages source/assets/tooling;
- Pages workflows;
- repository changelog.

Ordinary README, issue-template and Wiki prose changes do not trigger this full candidate workflow.

V2 lives on `v2/research-program`. Rather than duplicating the deployment workflow into that branch, default-branch Pages orchestration listens for successful completion of **CM-PharmE 2.0 Formal Ontology CI**. A V2 completion is eligible only when its head SHA already matches the exact V2 source SHA registered on `main`; otherwise publication waits for the governed registry update on `main`.

This avoids both silent V2 drift and duplicated deployment logic.

## Build/deploy separation

The build job:
- rebuilds exact-ref V1 and V2 inputs;
- executes semantic publication gates;
- generates WIDOCO reference outputs;
- packages verified downloads/provenance/checksums;
- wraps them with the multi-version shell;
- creates deterministic `reference/index.html` aliases from generated WIDOCO `index-en.html`;
- writes `.nojekyll`;
- runs download/traceability QA;
- runs deployment preflight;
- uploads a GitHub Pages artifact.

The deploy job is a distinct job and uses the `github-pages` environment with Pages/OIDC permissions only when explicitly authorized.

## Toolchain pins

The workflow pins release commits for GitHub-maintained actions rather than floating major tags:
- checkout v7.0.1;
- setup-python v7.0.0;
- setup-java v6.0.1;
- configure-pages v6.0.0;
- upload-pages-artifact v5.0.0;
- deploy-pages v5.0.1.

WIDOCO remains pinned to 1.4.25 with its verified JAR SHA-256.

## Preflight gates

The deployment preflight rejects:
- missing top-level entry point or `.nojekyll`;
- route-inventory gaps;
- missing V1/V2 reference/download/provenance/citation routes;
- a reference route that serves the shell placeholder instead of generated WIDOCO;
- source-ref disclosure gaps;
- stable/evolving lifecycle violations;
- generic `latest` path;
- symlinks;
- obvious private-key/token patterns or restricted-evidence markers;
- a V2 semantic-CI trigger whose head SHA is not the registered source SHA.

The preflight emits `pages-deployment-manifest.json` with build ref, registry hash, generator versions, per-version source refs/fingerprints and deferred WebVOWL/rendered-verification status.

## Remaining #275 work

This slice does **not** claim the site is public. Remaining work:
- one-time repository Settings → Pages → Source = GitHub Actions if not already enabled;
- authorize and execute candidate deployment;
- capture exact deployment ref and public URL;
- after #272, verify WebVOWL public assets/load;
- public HTTP/render smoke tests for V1/V2 reference/download routes;
- intentional rendered-verification failure test;
- final release-gate disposition.
