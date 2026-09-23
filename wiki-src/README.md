# CM-PharmE Wiki Source

This directory is the source-controlled authoring and QA mirror for the CM-PharmE GitHub Wiki.

## Why this exists

GitHub Wiki content is maintained in a separate Git repository. Keeping the authored Markdown, metadata contract, QA inputs and snapshot manifest here allows the documentation program to remain reviewable, reproducible and traceable to the CM-PharmE research repository.

## Authority boundary

- **CM-PharmE 1.x semantic/research authority:** `main`.
- **CM-PharmE 2.0 semantic/research authority:** `v2/research-program`.
- **Wiki source authority for documentation text:** this `wiki-src/` package once merged.
- The Wiki explains, synthesizes and navigates. It does not redefine ontology semantics or promote pending evidence to completed results.

## Current documentation status

- Candidate Wiki baseline: **WB-2026.09.1**
- Candidate maturity: **Candidate**
- V1 documentation maturity: **Stable**
- V2 documentation maturity: **Stable-to-date / Evolving**
- V1 source ref inspected: `main@5099888668d35f798e4759e3534e707ed906db24`
- V2 source ref inspected: `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- Formal repository Release at foundation check: **none**
- Wiki publication state: **source-controlled draft; GitHub Wiki publication still requires synchronization**

## Publication model

Files under `wiki-src/pages/` are designed to map to GitHub Wiki pages. Files under `wiki-src/templates/` are authoring templates and are not required to be published as end-user pages.

## Governance

See:
- `pages/Wiki-Versioning-and-Lifecycle.md`
- `pages/Wiki-Authoring-Standard.md`
- `pages/Wiki-Update-Register.md`
- `baseline-manifest.json`

## Related issues

#202, #203, #210, #211, #215, #216, #217.
