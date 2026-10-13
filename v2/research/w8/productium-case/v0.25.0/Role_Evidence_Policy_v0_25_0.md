# Role evidence policy 0.25.0

The Explorer separates source observations from native ontology role assertions. The bounded role policy is now implemented; the stronger real-world manufacturer and wholesale-distributor mapping remains partial.

| Input or condition | Representation | Assertion boundary |
|---|---|---|
| Matching labeler name, product NDC, source pointer and digest-shaped locator | Source-reported listing responsibility | A locator is not independent verification of source bytes or real-world activity |
| Reported `openfda.manufacturer_name`, string or array | Individual observations with exact field pointers | No automatic ManufacturerRole projection |
| Equal company-name text | Exact text agreement | No organization identity merge |
| Different or multiple names | Review state with all observed names preserved | No forced choice of manufacturer |
| No manufacturer name | Not reported | Absence is not evidence of no manufacturer |
| Missing or malformed source binding | Listing inference withheld pending review | Previously frozen graph is preserved; this observation layer does not rewrite it |
| Packager or application-number fields | Original source values retained | No inferred wholesale distribution or regulatory approval |

The native model and retained RDF source projection are unchanged. This release does not add classes, alter OntoUML stereotypes, or run new OWL reasoning. Existing HermiT/ROBOT results retain their original scope. Manufacturer and distributor activity would need attributable identity, explicit activity evidence and a reviewed native role pattern.

Validation comprises 39 role-policy assertions (20 on the five retained source rows and 19 controlled boundaries), 72 HTTP/SQLite/graph checks and 24 UI-to-service checks. These are internal engineering checks, not independent domain review or a usability study. Browser visual validation remains open because the executable download failed.
