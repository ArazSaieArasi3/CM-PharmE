# CM-PharmE Pages Shell and Information Architecture

Issue: #270  
Parent: #267  
Release dependency: R1 — Public Candidate

## Purpose

The Pages shell is a static, registry-driven navigation layer. It does not duplicate ontology semantics and it does not require JavaScript for navigation.

## Public route model

Global:
- `/` — landing / choose version;
- `/about/` — surface/authority explanation;
- `/ontology/` — version chooser;
- `/history/` — version-family history;
- `/citation/` — citation boundary/guidance.

Per registry version:
- `<version-route>/` — version overview;
- `<version-route>/reference/` — formal reference entry point;
- `<version-route>/explore/` — interactive-exploration entry point;
- `<version-route>/downloads/` — downloads/serializations entry point;
- `<version-route>/provenance/` — build/source provenance;
- `<version-route>/history/` — version-specific history;
- `<version-route>/citation/` — version-specific citation guidance.

Current production routes are not hard-coded in the generator:
- V1 resolves from the registry to `/ontology/v1.0.0/` as an immutable stable path.
- V2 resolves from the registry to `/ontology/v2/current/` as a mutable convenience path while V2 remains evolving.

## Navigation contract

Every generated page has static links to:
- portal home;
- ontology-version chooser;
- About;
- Research Wiki;
- repository;
- and, on version pages, the version root.

Every version root displays lifecycle, route kind, exact semantic source ref, citation status and documentation fingerprint.

## Accessibility / responsive baseline

The shell requires:
- semantic heading hierarchy with exactly one page-level `h1` intent;
- `main#main-content`;
- keyboard skip link;
- labelled primary navigation;
- meaningful text links;
- no JavaScript-only navigation;
- visible focus styling;
- responsive grid/navigation at mobile widths;
- viewport metadata.

## Future-version behavior

The shell iterates the version registry. A hypothetical V3 dry-run is tested by adding one registry entry only. The test requires:
- automatic V3 appearance on the landing/chooser;
- `/ontology/v3/current/` generation;
- the same version subroutes;
- no copied navigation implementation;
- collision rejection if V3 attempts to reuse a V2 route.

The synthetic V3 is test data only and is never written to the production registry or published as scientific content.

## Boundaries

This issue creates a deployable shell artifact only. WIDOCO content (#271), WebVOWL (#272), downloadable semantic artifacts (#273) and public deployment/render verification (#275) remain downstream.
