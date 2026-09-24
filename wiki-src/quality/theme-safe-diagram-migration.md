# Browser/theme-safe diagram migration QA

**Issue:** #260  
**Date:** 2026-09-24

## Result

**PASS — all 20 governed SVG diagrams were migrated to a self-contained browser/theme-safe rendering contract.**

## Root cause addressed

Two independent failure modes are addressed:

1. **Rendering inheritance:** governed SVGs can become unreadable if they rely on transparent canvases or page-inherited foreground colors.
2. **Stale raw-image caching:** even after the SVG itself is corrected, a Wiki page that embeds a branch-floating `raw/.../main/...svg` URL can allow a browser/CDN cache to continue displaying an older copy. The reported Chrome-versus-Edge difference is consistent with this second failure mode because the current repository SVG was already theme-safe while the Chrome screenshot still showed the older appearance.

## New rendering contract

Every governed SVG now:
- contains a full-canvas white background (`#ffffff`);
- pins root foreground to `#24292f`;
- carries `data-theme-safe="true"`;
- remains self-contained when embedded in GitHub Wiki Light/Dark modes;
- does not require readers to change Chrome/Edge/GitHub appearance settings.

## Migration result

Theme-safety validation:
- governed SVGs normalized/checked: **20**
- generic diagram validation errors: **0**
- V2 ontology semantic-validation errors: **0**

Cache-safe embedding migration (workflow `36015123137`):
- governed SVG assets covered: **20**
- stale/unversioned image embeds detected and corrected: **25**
- Wiki pages updated: **8**
- updated pages include Diagram Standards, Research/Evolution diagrams, V1/V2 research pages, V2 Ontology Diagram Suite, V2 Ontology Reference and V2 UFO/OntoUML Architecture.

The V2 ontology generator was also changed so future regenerated ontology SVGs are theme-safe natively.

## Permanent controls

- `tools/wiki/normalize_diagram_theme.py` — migration/normalization utility.
- `tools/wiki/check_diagrams.py` — rejects governed SVGs without:
  - `data-theme-safe="true"`;
  - explicit root foreground/background;
  - internal `diagram-background` white canvas.
- `tools/wiki/sync_diagram_image_urls.py` — rewrites governed raw-image embeds with `?sha=<content-hash>`.
- Wiki CI runs the URL synchronizer in `--check` mode and rejects stale/unversioned embeds.
- `wiki-src/diagrams/STYLE-GUIDE.md` — documents both browser/theme-safe rendering and cache-safe embedding.
- `tools/wiki/generate_v2_ontology_diagrams.py` — emits theme-safe ontology SVGs natively.

## Semantic boundary

This migration changes only visual rendering and browser independence. It does not change ontology semantics, labels, relations, evaluation evidence or database semantics.
