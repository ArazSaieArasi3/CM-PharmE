# Four-domain coherence and isolate experiment

This is a separate additive proposal. Four-domain removal/transfer stays on hold. No author acceptance, merge or full native/UFO validation is claimed.

Run `run_lab.py`, `run_pv.py`, then `run_regression.py`, then the existing `../2.1.0-alpha.1-native-fidelity-audit/check_native_fidelity.cjs` with the new native JSON, installed OntoUML node_modules and native-results.json as arguments, then `finalize.py`. Use PYTHONDONTWRITEBYTECODE=1, the preceding labs' Python environment (rdflib 7.6.0, pyshacl 0.30.1, owlready2 0.49), Java 17 and the native runtime versions recorded in native-results.json. Earlier sibling labs are runtime dependencies. Do not import their build scripts because they write artifacts.

run_pv.py downloads the PDF only if its manifest is absent. Extraction rows are manually transcribed from the primary source; replay validates the graph and queries, not an independent extraction. The PDF itself is not archived. Generated blank nodes are not byte-stable. The manifest hashes delivered artifacts, excluding itself.

The topology now has zero isolates in a separate experimental copy. Ten new relations still have pending stereotypes and provisional optional bounds. The native projection adds only those relations to the previous refinement; it does not silently integrate every subsequent information/PROV proposal.

Two bounded countermodels deliberately force particular classes empty, so their expected unsatisfiable named classes are explicit. The unmodified combined schema must still have none. Initial over-strict test results are retained.

See the Persian decision report, complete 23-task status, source register, domain-coherence.json, decision-dossier.json and machine-readable results.
