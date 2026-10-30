# Authorized Pages replacement at the complete 2.2 cutover

Decision: **PAGES-CUTOVER-22-01**, explicitly instructed by Araz on 2026-10-30.
Execution issue: #346. [Policy](policy.json) · [Initial readiness](readiness.json).

Remove the published 2.0 and 2.1 model content from GitHub Pages and replace it
with the complete 2.2 model when that replacement is accepted and ready. This
new direct instruction overrides the older public version-path retention rule
for the two named Pages families. It does not authorize deletion of repository
source, tags, releases, scientific evidence, Wiki history or unrelated V1.

The main registry at42a5ae4da0e87af161e91110a044c6b146982e89 identifies the initial
retirement roots as ontology/v2/current/ and ontology/2.1.0/m1/ (IDs v2/v2-m1).
Before execution, inventory their complete current routes, aliases and assets.
Remove their old reference, explorer, downloads, citation and chooser content
from the deployed artifact; update reader navigation to ontology/2.2.0/.
Never silently put 2.2 RDF bytes under an old 2.0/2.1 semantic download URL.
Use actual retired-route/alias checks so that removing a chooser entry alone
cannot count as removal of old model content.

The applicable model/requirements/semantic/validation gates (G22-A–D), complete
candidate diagrams/reference/coverage/local browser QA (G22-E), and prepublication
compatibility/support/package checks (G22-F) must be evidenced first. Then deploy
the complete replacement in one coordinated publication, followed by actual
public E/F verification. Requiring those public outcomes before the first
deployment would be circular; they close the cutover after deployment.

Implementation must update the active version registry and common build matrix,
old V2 retention/download expectations, public verification and navigation as
needed for the authorized retirement. Keep the old baseline archives as GitHub
evidence. Archive and verify the prior deployment before switching; restore it
if the replacement fails public QA. Record the exact source/deploy identities,
removed-route inventory, public hashes/browser results and new baseline.

**Current state is BLOCKED**: only an unaccepted native review assembly exists;
the accepted complete 2.2 model and full publication candidate are not ready.
No old Pages content was removed in this preparation turn. The user authorizes
the future replacement already; another permission request is unnecessary once
its concrete release prerequisites are met.

[automation.json](automation.json) records the enabled daily condition check.
It checks actual evidence and the active readiness record, performs no deletion
while unready, and carries out the already authorized cutover only when the
complete replacement is ready. After verified completion it reports and stops.
The active plan must select a new versioned readiness record when state changes;
this initial blocked snapshot remains historical evidence.
