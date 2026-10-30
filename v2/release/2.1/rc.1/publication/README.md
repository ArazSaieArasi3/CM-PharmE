# Published experimental 2.1.0-rc.1 — RC-03 verified

**[Open the published prerelease](https://github.com/ArazSaieArasi3/CM-PharmE/releases/tag/2.1.0-rc.1).**
GitHub release **426685466**, published **2026-10-28T13:13:41Z**
(16:43 Asia/Tehran). `draft=false`, `prerelease=true`; it is not the stable latest
release. This completes issue #326 and the finite RC-01/02/03 route. Final GA
scientific/author/expert gates are still open; draft PR #305 is not merged.

The [publication plan](release-plan.json), [exact notes](release-notes.md),
[target CI cohort](target-ci.json) and [contract/refusal expectations](publication-contract.json)
were frozen before publication at `05a43dd43e8efcd11251b876b85d5dbd3c3b39be`.
Contract SHA-256 `d0f6859900cc6512b313ed6f6ba13b08bafaa3565a929a14bc1e6bdbf30e1de4`.
An independent read-only review checked both the frozen plan and live API result.

| Identity | Exact revision |
|---|---|
| Tag `2.1.0-rc.1` / release branch | `76c547f02e56d116b9e86d0aef9388e9d99f0949` |
| Curated tar source | `64edf150db8a78579928fd99b5a381f665c1afdf` |
| Curated scope source | `a0a9a539c3891476847b52fed4c65d9ccae8d485` |
| Bundle builder implementation | `f58a935f5c8455cce7df1338d0d380cb6d7a0a3b` |

The tag identifies the release assembly. GitHub's automatic source ZIP/tarball
represent that assembly tree; the separately uploaded curated tar is the replay
bundle. Preparation-state fields inside the frozen tar remain historical facts;
this live publication receipt records subsequent publication. Neither source nor
archive bytes were rewritten to manufacture agreement.

Three uploaded assets were verified in the draft, then downloaded from their
published public URLs with independent HTTP requests and checked byte-for-byte:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| cm-pharme-2.1.0-rc.1.tar | 30,945,280 | `21f140abb6ccde5eebb9302cd87724ce8616a2f71a046b22bf3c3c5ea01b10ba` |
| cm-pharme-2.1.0-rc.1.tar.sha256 | 91 | `9fac328ebbd108d04580c8ba1a105572834a463b200bd5e47e75f9ecd14b1dae` |
| cm-pharme-2.1.0-rc.1.provenance.json | 2,096 | `3ea9d84ac01249d484bf154db297be58f233d99cd6793e1dcb3452e99d3723d2` |

[Published results](published-results.json) identify the actual release/tag and
asset IDs/URLs/hashes. [Download verification](download-verification.json),
[release API snapshot](published-release.json), [tag ref](tag-ref.json),
[latest-release query](latest-release.json), [staging result](staging-results.json)
and [UI proof](published-2.1.0-rc.1-20261028.jpg) preserve the evidence. The latest
stable endpoint returned 404, consistent with the sole experimental prerelease.
The published body equals the frozen notes after **CRLF-to-LF only** transport
normalization (29 line endings); no content, expectation or scientific claim
changes. The read-only verifier also passes all eight frozen refusal controls.

```sh
python v2/release/2.1/rc.1/publication/verify_publication.py \
  --assets-dir /path/to/three-independently-downloaded-assets \
  --release-json v2/release/2.1/rc.1/publication/published-release.json \
  --tag-json v2/release/2.1/rc.1/publication/tag-ref.json \
  --latest-json v2/release/2.1/rc.1/publication/latest-release.json \
  --output /path/to/verification.json
```

The assembly commit passed 25 distinct workflow families, each with its original
scope; RC-02 cold replay and archive checks are unchanged. Publication used the
already signed-in GitHub release UI after exact plan/assets/target checks, under
the user's explicit publication instruction. No new credential or security access
was created. The connector lacks release writes; [GitHub API rules](https://docs.github.com/en/rest/releases/releases#create-a-release)
also require Workflows authorization for this assembly, which Actions' GITHUB_TOKEN
cannot receive. No token scope or source-target workaround was introduced.

This is an experimental research checkpoint. Source-policy scientific acceptance
remains 0/4, ORSD author acceptance 0/83, original-after witnesses 88/89 versus
prospective-after 89/89 under one declared transition, and native inventories
76/60/11/14 remain overlapping input counts. Full-candidate 20-family execution,
complete native-to-OWL alignment and independent scientific/expert/GA acceptance
are pending. #306/#310/#315 and original work stay open. Future work follows the
[GA gates](../../0.1.0/README.md); no additional feature is required to claim this
already verified experimental publication.
