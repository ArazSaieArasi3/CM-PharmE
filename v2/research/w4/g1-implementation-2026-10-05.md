# G1 disposition implemented — 2026-10-05

The project author explicitly approved the preceding 22-decision batch:
20 active refinements and the two deferrals S-04/S-05. The October 4 register
and semantic report remain historical records of the unapproved state at that
time; they do not describe the current approval status.

Current implementation, quantified findings, experiment limitations and next
gates are in the [candidate report](../../ontology/candidates/2.1.0-alpha.1-candidate/README.md).
The machine-readable [decision record](../../ontology/candidates/2.1.0-alpha.1-candidate/decisions.json)
retains RR-01 through RR-15 and S-01 through S-07. RR identifiers correspond to
the W3/W4 source pointers in the [earlier register](g1-relrig-decision-register.json).

- 125 active concepts: 119 classes and six datatypes; 57 object properties.
- 34 new Roles and seven new RoleMixins; three dependent/deferred classes outside
  the active import. Contextual classification reuses general assignment identity.
- All eight protected distinction pairs preserved.
- 120 expected outcomes reproduced by SQL and SHACL (36 valid, 84 deliberately invalid).
- Official JSON schema, HermiT, Pellet and OWLAPI profile checks pass in their
  stated scopes. A missing annotation-property declaration was found and repaired.
- No official anti-pattern-engine execution or all-domain conformance certificate.
- Remaining: 36 native relation dispositions, nine inherited Role grounding
  decisions, G2 source-backed connections and full mapping/held-out regression.

G1 author disposition and the scoped implementation are complete. G2–G5 remain
open; G3/G4 have partial evidence from this work. PR #305 stays draft and #306
stays open. No comprehensive diagram or final 2.1 release is authorized by this
checkpoint alone.
