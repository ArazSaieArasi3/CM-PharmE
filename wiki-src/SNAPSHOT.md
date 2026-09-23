# Wiki Snapshot and Archive Procedure

## Purpose

Create a reproducible source archive for a declared or candidate Wiki baseline while keeping Wiki documentation identifiers distinct from CM-PharmE semantic/model releases.

## Build

From repository root:

```bash
python tools/wiki/build_wiki_snapshot.py build --baseline WB-2026.09.1
```

Outputs:
- `dist/wiki-WB-2026.09.1/` — normalized source snapshot;
- `dist/wiki-WB-2026.09.1/ARCHIVE-MANIFEST.json`;
- `dist/wiki-WB-2026.09.1.zip` — deterministic ZIP.

## Verify / read-back

```bash
python tools/wiki/build_wiki_snapshot.py verify --archive dist/wiki-WB-2026.09.1.zip
```

Verification checks:
- archive opens;
- archive manifest exists;
- every manifested file exists;
- every SHA-256 digest matches.

## What is captured

- all files under `wiki-src/pages/`;
- page inventory;
- baseline manifest;
- Wiki authoring/source README;
- update register as part of pages;
- generated archive manifest;
- repository source commit when available.

## Actual Wiki commit

Before #218 publication, the archive records the source-controlled candidate and has no authoritative GitHub Wiki commit.

After actual GitHub Wiki synchronization, a final snapshot must additionally record:
- exact GitHub Wiki Git commit/ref;
- source-to-published page manifest;
- rendered QA result;
- publication event.

## Naming safety

`wiki-WB-...` identifies a documentation archive only. It must not be described as:
- a CM-PharmE semantic/model release;
- a GitHub Release unless attached to a real GitHub Release;
- a DOI-backed research release unless such a package actually exists.

## Restoration

To reconstruct source state:
1. verify the ZIP;
2. extract it;
3. use the included `pages/` Markdown and metadata files;
4. compare `ARCHIVE-MANIFEST.json` hashes;
5. synchronize pages only through the controlled Wiki publish process.

## Final archive gate

#217 remains open until a QA-approved **published** Wiki baseline is archived with its exact Wiki commit/ref. A pre-publication source snapshot proves the procedure, but is not the final release archive.
