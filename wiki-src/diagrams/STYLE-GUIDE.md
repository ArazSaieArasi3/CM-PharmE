# CM-PharmE diagram standard

**Issue:** #232  
**Status:** Active documentation standard  
**Pilot scope:** CM-PharmE Wiki and source-controlled documentation

## 1. Principle

A diagram is a semantic/documentation artifact, not decoration.

Every published diagram must answer:
- what question it answers;
- which version/scope it describes;
- which notation is used;
- whether it is authoritative, an authoritative projection, or illustrative;
- where its editable/version-controlled source lives;
- where its publication artifact lives;
- when and against which source ref it was checked.

## 2. Notation selection matrix

| Documentation problem | Preferred notation | Allowed implementation source | Do not substitute |
|---|---|---|---|
| Ontology/conceptual model | OntoUML/UFO-aware class/relationship notation | PlantUML, draw.io, other explicit ontology notation | C4, generic ERD |
| Relational logical/physical model | Crow's Foot ERD / explicit relational ER notation | Mermaid ER, draw.io ERD, PlantUML ERD | OntoUML, generic boxes/arrows |
| Data/query pipeline | Data-flow / architecture flow | Mermaid flowchart, Graphviz DOT, draw.io | Ontology notation |
| Software/application architecture | C4 where system/container/component abstraction is intended | PlantUML C4, Structurizr, draw.io C4 | OntoUML or ERD |
| Research/evaluation process | Process/activity/flow notation | Mermaid flowchart, BPMN/activity style, Graphviz | C4 |
| Cross-version evolution | Lineage/evolution notation | Graphviz/Mermaid lineage, explicit migration map | Unlabeled before/after screenshots |

C4 is not ontology notation. ERD is not a conceptual ontology substitute.

## 3. Artifact status

Use exactly one:
- **Authoritative** — the diagram itself is the governed canonical model artifact.
- **Authoritative projection** — generated/synchronized from authoritative semantic/data artifacts; useful visually but not the semantic source of truth.
- **Illustrative** — explanatory view that must not introduce new semantics.

Most Wiki diagrams should be **authoritative projections** or **illustrative**.

## 4. Folder convention

```text
wiki-src/diagrams/
├── manifest.json
├── source/
│   ├── ontology/
│   ├── erd/
│   ├── architecture/
│   ├── process/
│   └── evolution/
└── rendered/
    ├── ontology/
    ├── erd/
    ├── architecture/
    ├── process/
    └── evolution/
```

## 5. Naming convention

`<diagram-id>--<stable-kebab-name>.<ext>`

IDs:
- `DGM-ONT-nnn` ontology/conceptual;
- `DGM-ERD-nnn` relational;
- `DGM-ARC-nnn` architecture/data-flow/software;
- `DGM-PRC-nnn` research/process;
- `DGM-EVO-nnn` evolution/lineage.

Source and rendered artifact share the same ID and stable name.

## 6. Diagram artifact contract

Each manifest entry records:
- id;
- title;
- purpose;
- version_scope;
- notation;
- artifact_status;
- source_path;
- rendered_path;
- generation_method;
- authoritative_source;
- last_updated;
- checked_ref;
- related_pages;
- legend_required;
- alt_text;
- caption.

## 7. SVG publication convention

Preferred publication artifact: SVG.

SVG requirements:
- explicit `viewBox`;
- no fixed assumption of desktop-only width;
- `<title>` and `<desc>`;
- text remains selectable where practical;
- no externally loaded fonts/images;
- arrows/markers must be defined in-file;
- relation meaning must come from notation/labels, not color alone;
- avoid rasterized text;
- diagrams should remain intelligible when scaled to normal GitHub Wiki width.

PNG may be retained for legacy/grandfathered artifacts, but new diagrams should prefer SVG.

## 7A. Browser/theme-safe rendering

GitHub Wiki may be viewed in light or dark mode and browsers/extensions can apply different dark-mode policies. Governed SVGs must therefore render consistently without inheriting page colors.

Required for every governed SVG:
- an internal white canvas (`#ffffff`) covering the complete viewBox;
- explicit root foreground color `#24292f`;
- `data-theme-safe="true"` on the SVG root;
- no reliance on the embedding page's `currentColor` without the root color being pinned;
- no transparent-canvas assumption for headings, relation labels or legends.

The project intentionally prefers a stable light documentation canvas over browser-dependent adaptive theming. This makes Chrome, Edge, GitHub Light/Dark and forced-dark configurations render the diagram as one self-contained visual artifact.

The mechanical contract is enforced by `tools/wiki/check_diagrams.py`. Existing governed SVGs are normalized by `tools/wiki/normalize_diagram_theme.py`.

### Cache-safe embedding

GitHub Wiki pages must not embed governed SVGs using only a branch-floating raw URL. Browsers and intermediary caches can retain an older SVG after the repository file changes.

Every governed raw-image embed appends a content-derived query key:

`?sha=<first-12-hex-of-SHA256>`

The key is generated from the committed SVG bytes by `tools/wiki/sync_diagram_image_urls.py`. When a diagram changes, its URL changes automatically, forcing a fresh fetch while keeping the canonical repository path stable.

CI runs `sync_diagram_image_urls.py --check` and rejects stale or unversioned governed diagram embeds.

## 8. Styling rules

- Styling is secondary to notation semantics.
- Use consistent spacing and alignment.
- Use limited visual hierarchy: title, package/group, entity, relation.
- Never rely on color as the only semantic carrier.
- If color encodes module/layer, repeat the module/layer in text/legend.
- Avoid dense edge crossings; split diagrams by question/abstraction level.
- Do not mix ontology classes, database tables and software components in one unlabeled abstraction plane.

## 9. Tool rules

### PlantUML
Preferred for reproducible textual ontology/C4/process sources when the required notation can be expressed clearly. Pin renderer/runtime version in any automated export workflow.

### Mermaid
Appropriate for ERD and lightweight flows. Pin Mermaid CLI version if automated SVG export is used. GitHub-rendered Mermaid is acceptable for lightweight explanatory diagrams, but authoritative published baselines should retain a source-controlled publication artifact when practical.

### Graphviz DOT
Appropriate for lineage, dependency and data-flow diagrams where graph semantics are primary. Pin Graphviz version for deterministic release exports if pixel-level reproducibility matters.

### draw.io
Allowed when visual/manual layout materially improves readability. The `.drawio` file is the source; exported SVG must be versioned and linked. Do not keep only PNG/SVG.

## 10. Legacy/grandfathered artifacts

Existing V1 PNG/draw.io pairs are grandfathered because editable draw.io sources exist. Legacy publication-only assets without editable source, if discovered, must be marked `grandfathered-source-missing` and cannot be used as the pattern for new work.

## 11. Captions and embedding

Every Wiki use of a non-decorative diagram should state:
- diagram title/ID;
- one-sentence purpose;
- version scope;
- artifact status;
- source/provenance link.

## 12. Staleness rule

A diagram must be reviewed when:
- referenced model/schema changes;
- a version/ref in its manifest becomes stale;
- page claims materially change;
- relation cardinality/semantics change;
- diagram terminology changes under the editorial policy.

## 13. QA checklist

Before publication:
- correct notation selected;
- title/purpose/scope present;
- abstraction level coherent;
- relation arrows/cardinalities unambiguous;
- source exists;
- rendered artifact exists;
- manifest paths resolve;
- caption/alt text present;
- authoritative/illustrative status explicit;
- version/ref not stale;
- readable at Wiki width;
- no unsupported semantic claim introduced.

Mechanical checks live in `tools/wiki/check_diagrams.py`.
