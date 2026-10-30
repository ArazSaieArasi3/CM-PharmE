# RC-01 scope/claim decision — issue #324

Target **2.1.0-rc.1 experimental research checkpoint**, not final GA. Payload
source is the already verified commit `64edf150db8a78579928fd99b5a381f665c1afdf`.
No ontology or historical test is edited by this preparation package.

| ID | Scope decision | Boundary |
|---|---|---|
| RCS-D01 | Include every tracked source blob at the exact payload revision under source/. | This prevents silent dependency omissions. Files outside the selected review groups remain archival source and are not promoted as current validated assets. |
| RCS-D02 | Name the EvidenceRecord candidate as current; label ContextClass as predecessor and all other profiles by their actual versions/input scopes. | Experimental OWL modules, copied W6 profiles and the latest native file are not certified as one complete translation. |
| RCS-D03 | Expose original historical 88/89 and prospective 89/89 witness results side by side. | No retrospective expected-value change or hidden contract transition. |
| RCS-D04 | Keep unknown inventories, pending source/author/ORSD/GA status and non-production/empirical limits explicit. | Schema checks, synthetic witnesses and independent historical CI do not establish complete scientific acceptance. |
| RCS-D05 | Freeze source/provenance and metadata now; leave archive construction, cold replay and actual publication for RC-02/03. | No tag, release, merge or final approval exists from this scope checker. A new payload revision requires a new explicit freeze. |

The source snapshot includes its historical root CITATION.cff version 1.0.0;
it is not current RC citation metadata. No root blanket license file was found,
and this scope does not invent a license grant. RC-02 must provide truthful current
metadata and retain per-asset notices. No third-party dependency downloads are
bundled by this manifest. Publication still needs a supported write route or a
maintainer action after concrete assets exist.

The archive metadata generated in RC-02 will have its own content hashes and build
provenance. It may contain RC review documentation in addition to the frozen
source/ payload, but it must not silently alter any source entry. Tag target and
source/archive agreement must be explicitly checked then; no branch is tagged here.
