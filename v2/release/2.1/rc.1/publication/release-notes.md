## Experimental research checkpoint

CM-PharmE **2.1.0-rc.1** packages the existing bounded research evidence for inspection and reproduction. It is marked **Pre-release**; independent scientific acceptance and final 2.1.0 GA gates remain open.

### Exact identity

| Item | Revision |
|---|---|
| Release assembly / tag target | 76c547f02e56d116b9e86d0aef9388e9d99f0949 |
| Curated bundle source snapshot | 64edf150db8a78579928fd99b5a381f665c1afdf |
| Frozen scope snapshot | a0a9a539c3891476847b52fed4c65d9ccae8d485 |
| Bundle builder implementation | f58a935f5c8455cce7df1338d0d380cb6d7a0a3b |

Download **cm-pharme-2.1.0-rc.1.tar** and its SHA-256 sidecar for the curated replay bundle. It contains 2,001 files: 1,975 immutable source files, 13 frozen scope files and 13 current metadata/packaging files. Thirteen versioned review groups select 155 source files; remaining source material is archival. The attached provenance JSON records this mapping. GitHub's automatic Source code archives describe the assembly-tag tree and are different from this curated tar.

Tar size: **30,945,280 bytes**. SHA-256:
`21f140abb6ccde5eebb9302cd87724ce8616a2f71a046b22bf3c3c5ea01b10ba`.

### Verified scope

All 25 workflow families passed on the assembly commit within their individual scopes. Repeat builds and independent local/GitHub builds produced identical tar bytes. Fresh extracted replay with newly installed isolated Python/npm dependencies reproduced the complete bounded EvidenceRecord report: native schema/guarded serialization, 12 new and 12 ContextClass SHACL rows, 89 historical/prospective rows, 10 identity cases, 6 HermiT cases and scoped refusal checks. Historical-after remains **88/89**; prospective-after is **89/89 under one explicit versioned transition**. Original expectations are preserved.

The four-policy dossier integration and source/scope integrity audit also reproduce exactly. This audit does not rerun all policy detector engines or copied-W6 databases. M1–M4 retain their original copied-database evidence scopes. Instructions and dependency locks are inside the tar; Python 3.12, Node 24, Java 17 and external dependency downloads are required.

### Known limits and provenance

Native unknown readOnly/cardinality inventories are 76/60, with 11 untyped and 14 specialized Properties; these overlap and are not detector findings. Full 20-family candidate execution, complete native-to-OWL alignment, independent scientific/expert acceptance and production readiness are pending. Source-policy scientific acceptance remains 0/4; ORSD author acceptance remains 0/83. Issues #306/#310/#315 and the other scientific/GA work remain open; PR #305 stays draft.

Root bundle citation identifies this RC; source/CITATION.cff remains historical 1.0.0. Existing notices are preserved without a new blanket license grant. Prepared-status fields inside the immutable bundle describe its build-time state; this release page provides live publication status. No stable-main merge or final GA approval is asserted.
