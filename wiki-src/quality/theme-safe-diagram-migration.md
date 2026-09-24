# Browser/theme-safe diagram migration QA

**Issue:** #260  
**Date:** 2026-09-24

## Result

**PASS — all 20 governed SVG diagrams were migrated to a self-contained browser/theme-safe rendering contract.**

## Root cause addressed

The earlier governed SVGs could depend on the embedding page for text/stroke color and used transparent canvases. In GitHub dark mode this could make headings, labels and relation text outside white boxes hard to read, depending on browser/theme behavior.

## New rendering contract

Every governed SVG now:
- contains a full-canvas white background (`#ffffff`);
- pins root foreground to `#24292f`;
- carries `data-theme-safe="true"`;
- remains self-contained when embedded in GitHub Wiki Light/Dark modes;
- does not require readers to change Chrome/Edge/GitHub appearance settings.

## Migration result

Workflow `36014611901`:
- governed SVGs normalized: **20**
- generic diagram validation errors: **0**
- governed diagrams checked: **20**
- V2 ontology semantic-validation errors: **0**

The V2 ontology generator was also changed so future regenerated ontology SVGs are theme-safe natively.

## Permanent controls

- `tools/wiki/normalize_diagram_theme.py` — migration/normalization utility.
- `tools/wiki/check_diagrams.py` — now rejects governed SVGs without:
  - `data-theme-safe="true"`;
  - explicit root foreground/background;
  - internal `diagram-background` white canvas.
- `wiki-src/diagrams/STYLE-GUIDE.md` — documents the browser/theme-safe rendering standard.
- `tools/wiki/generate_v2_ontology_diagrams.py` — emits the contract directly.

## Semantic boundary

This migration changes only visual rendering and browser independence. It does not change ontology semantics, labels, relations, evaluation evidence or database semantics.
