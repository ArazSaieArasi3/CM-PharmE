# Explorer deployment workbench 0.25.0

This extends the existing CM-PharmE source Explorer with a persistent software-product declaration workflow. The pharmaceutical extract stays read-only. Software deployments, versions and capabilities are a separate Product Ontology population.

## Start

Unzip the package. With Python 3.10 or newer, run `python server.py` in this folder, then open `http://127.0.0.1:8765`. The application itself uses only the Python standard library and browser JavaScript. On Windows, `py server.py` can be used if that is the installed launcher.

`workspace.sqlite` is created beside the server on first use. Restarting the service retains the ledger. Use `--db PATH` for another ledger, or `--port NUMBER` when the default port is occupied. The server listens only on the loopback address. `Explorer_Read_Only.html` remains the prior self-contained read-only view.

## Use

1. Search a pharmaceutical source record and inspect its packaging and source pointers.
2. In Software deployment workbench, load a restart, upgrade or uncertain-continuity example. Examples are labelled `SCENARIO` and receive separate workspace identifiers.
3. Validate and record the declaration. Accepted declarations populate a scoped RDF graph. Rejected and review-required attempts appear in the audit history, with no accepted graph writes.
4. Select a history record to attach its exact declaration and decision to the selected pharmaceutical research brief. The two identities and evidence scopes remain separate.
5. Download the research brief, declaration or accepted RDF. A rejected record's workspace can still contain earlier accepted assertions; the graph export is the workspace's cumulative accepted graph, not a proof that the selected attempt was accepted.

Real operator declarations may use `DECLARED_OPERATIONAL` in a new workspace. That records an operator's statement and evidence locator, not independent verification or a deployment action. Scenario workspaces cannot be relabelled as operational. The application neither updates installed software nor verifies causal continuity. Its build fingerprint identifies the code and bundled input; it does not establish the identity of a concrete realization.

## Engineering evidence

Run `python test_runtime.py` after installing `requirements-test.txt`. It exercises the actual HTTP service, isolated SQLite databases, 25 controlled transition scenarios, persistence, repeat submissions, concurrency and focused SHACL validation.

Run `node test_ui.mjs` with LinkeDOM 0.18.12 available. Set `LINKEDOM_PATH` to its module directory. These are DOM-to-service functional checks and executable-bundle checks, not visual-browser or human usability results.

`identity_policy.py` preserves the v0.22 `assess` function source exactly. The runtime adds input, transaction, scope and history controls. The scoped relational tables and audit metadata are not new ontology concepts or the full 101-class relational projection. The application does not run OWL reasoning on each request; it enforces the tested application contract.

The original source projection, five product rows and seven package projections are retained byte-for-byte from CM-PharmE commit 27a33d47c6c37c12e9ac7968a47b874075154c08. It is a historical openFDA extract, not live market coverage. Source labeler identity does not establish manufacturer, distributor or regulatory approval.

## Remaining boundaries

Visual browser verification, independent conceptual acceptance and observed user effectiveness remain open. The attempted Chromium download in the execution environment failed before a browser was installed. Multi-user production deployment, a full lifecycle engine, authentication and a full Workbench authoring workflow are outside this local prototype.

No conference manuscript is included in this application package.

## Source role observations in 0.25.0

The organization evidence panel and exported brief now retain the harmonized manufacturer-name field separately from native roles. Read `Role_Evidence_Policy_v0_25_0.md`, the five-row mapping table, source register and JSON execution reports. Run `node test_roles.mjs` for the 39 role-policy checks. No native manufacturer, wholesale-distributor or approval assertion is derived from these name fields.
