# RC-02 frozen packaging decisions

RCP-D01: Keep payload source 64edf15 and scope snapshot a0a9a53 immutable. Include
all 1,975 source files and all 13 scope files; root RC metadata and packaging code
are separate additions. Historical 1.0.0 citation, notices, GA register and original
88/89 witness expectation are preserved. No new feature or scientific approval.

RCP-D02: Use a deterministic uncompressed tar with fixed POSIX metadata, exact
file-set and per-file SHA-256 inventory, archive sidecar hash and code provenance.
Archive bytes must match across repeat builds and local/hosted environments.
No generated timestamp, host path, Git cache, installed dependencies or replay
output enters the bundle. Code content hashes plus CI commit identify the builder.

RCP-D03: Clean replay means fresh extraction and isolated freshly installed Python/
npm dependencies, with Python 3.12, Node 24 and Java 17. Rerun the bounded existing
EvidenceRecord semantic/native checks and the four-policy evidence integration.
Compare complete reports, not only totals. This does not rerun policy detector
engines, copied-W6 databases, full 20-family candidate validation or human review.

RCP-D04: Exact dependency versions and npm lock integrities are pinned; external
downloads are required. No offline distribution or pinned Python wheel hashes are
claimed. Preserve existing terms without inventing a root blanket license. Root
RC-specific citation metadata stays separate from the historical source citation.

RCP-D05: Freeze layout/claims/metadata/refusal expectations before implementation.
Retain the generated archive and evidence as a hosted CI artifact; committed
build code and exact inputs allow reconstruction after finite artifact retention.
Do not claim publication from artifact upload. RC-03 must still verify tag/asset/
source agreement and actual experimental prerelease publication; draft #305 and
scientific/GA gates #306/#310/#315 remain unchanged.
