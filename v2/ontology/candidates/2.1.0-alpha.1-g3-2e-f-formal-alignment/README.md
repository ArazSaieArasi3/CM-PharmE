# G3-2e-F — scoped OWL/SHACL candidate and time-bound operation query

Date: 2026-10-08 Asia/Tehran. Source OWL and SHACL: G3d integrated candidate. Native design: G3-2e-E. This is a draft candidate, not a 2.1 release.

## Aligned effects

`active.ttl` adds `productHasActiveSubstance` as a Product→Substance subproperty of the broad `hasActiveSubstance`. This maps the bounded M016 Product hook. It does not create a Presentation domain, global minimum, maximum one or mereological claim. `MatchConfidence` gains a qualified exactly-one inverse bearer restriction to `EntityMatchAssertion`; no assertion-wide confidence existence is required. The existing OWL exactly-one `capabilityBearer` restriction on `EnterpriseCapability` is retained.

`constraints.ttl` adds three bounded admission shapes: Product-only subject and typed substance values for the child property, exactly one Organization for each explicitly modeled EnterpriseCapability, and exactly one Assertion for each MatchConfidence. Organization and unscored Assertion are allowed to have no respective feature. The Product shape has no minCount. No shape is claimed to validate source provenance, formulation composition or legal scope.

## Operation derivation decision

`operates-snapshot.rq` is a read-only SPARQL SELECT. Bind `?at` as `xsd:dateTime`. It returns Organization, Facility, and the **same** FacilityOperation relator only when role/base types are explicit; one Facility and an unambiguous validity interval are present; and the interval contains the requested instant (inclusive start, exclusive end). This preserves the relator for provenance and prevents a historical episode from becoming an unqualified timeless `operates` triple. `active.ttl` retains the existing annotation and object property but has **no OWL property chain**; querying the snapshot does not materialize it. Source registration without an operation, a missing interval, an expired operation or a split-relator pair yields no result.

## Tests and limits

Run `python validate_candidate.py` in this directory (RDFLib 7.6.0 used). It reads G3d OWL/SHACL from the sibling directory and runs **23/23 bounded checks**: Turtle parsing and selected graph assertions; hand-evaluated admission conditions corresponding to the three added shapes; and SPARQL snapshot positive/negative fixtures. Baseline→candidate triples: OWL 1588→1599, shapes 655→678. This is **not a pySHACL execution**, an official OntoUML parser/anti-pattern run, a HermiT/Pellet run on this candidate, or a complete regression over the combined old shapes. The runtime lacks pySHACL and owlready2; installation from its network-restricted package index failed. Do not infer full SHACL or OWL conformance from these checks.

`integration-manifest.json` lists each effect and every known gate. G3 remains 2/7 packages closed (28.6%) and stage 3 of 5 active; G1/G2 closed. G3-P3 scientific adjudication and P4 formal integration remain open. The named-class graph remains 138 classes, 15 components and 14 isolates. Draft PR #305 and issue #306 stay open.

Next bounded turn: **G3-3-A**, official native OntoUML parser/schema and anti-pattern tooling on the G3-2e-E overlay, recording raw findings and tool versions. Later G3-3-C executes full OWL DL and SHACL validation of the integrated candidate.
