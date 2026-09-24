# Diagram browser/theme compatibility QA

**Date:** 2026-09-24  
**Scope:** all governed SVG diagrams  
**Related:** #232, #235

## Problem observed

A GitHub Wiki page viewed in Chrome Dark Mode rendered headings and relation strokes in low contrast because some governed SVGs used a transparent canvas and relied on `currentColor` or browser defaults. The same page could appear acceptable in another browser/theme configuration, which made rendering browser-dependent.

## Resolution

All governed SVGs now use a self-contained rendering contract:

- internal full-canvas white background: `#ffffff`;
- explicit root foreground color: `#24292f`;
- `data-theme-safe="true"` on the SVG root;
- no dependence on the embedding page's foreground/background;
- semantic line/text styles remain inside the SVG.

The project deliberately prefers a stable light diagram canvas over browser-dependent adaptive theming.

## Coverage

- Governed diagrams: **20**
- Governed SVGs normalized: **20/20**
- V2 ontology diagrams regenerated against authority before normalization: **PASS**
- Generic diagram artifact validation: **PASS**
- V2 ontology-suite validation: **PASS**
- V2 ontology-reference validation: **PASS**

## Example

`DGM-ONT-002` now begins with a theme-safe SVG root and explicit background:

```xml
<svg ... data-theme-safe="true" style="color:#24292f;background:#ffffff">
  <title>...</title>
  <desc>...</desc>
  <rect id="diagram-background" ... fill="#ffffff" stroke="none" />
```

## Permanent controls

- `tools/wiki/normalize_diagram_theme.py` can normalize governed SVGs.
- `tools/wiki/check_diagrams.py` rejects governed SVGs that do not include the theme-safe contract.
- `tools/wiki/generate_v2_ontology_diagrams.py` now emits theme-safe SVGs natively.
- `wiki-src/diagrams/STYLE-GUIDE.md` defines the browser/theme-safe rendering rule.

## Expected browser behavior

The diagram itself should now look the same in:
- GitHub Light Mode;
- GitHub Dark Mode;
- Chrome;
- Edge;
- other browsers that display the SVG without destructive image filters.

A browser extension or experimental forced-dark feature may still transform the entire image, but because foreground and background are now inside the same SVG, they should transform together and remain legible.
