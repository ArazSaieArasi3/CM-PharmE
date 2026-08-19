# W5 Formalization Notes

## Translation principle
OWL is an implementation of the Gate-D conceptual model, not a replacement for UFO/OntoUML semantics. Where OWL DL does not natively encode distinctions such as `RoleMixin`, `Relator`, `Mode`, `Situation` or identity principles, CM-PharmE preserves the conceptual commitment through stable classes, structural axioms, explicit annotations and companion model metadata.

## Main translations
- `Kind`, `Role`, `RoleMixin`, `Relator`, `Event`, `Situation`, `Mode`, `Quality`, `Subkind` → OWL classes with `cmmeta:ontoumlStereotype` annotations.
- Conceptual datatypes → declared `rdfs:Datatype` entities.
- Material relations → OWL object properties annotated with their grounding Relator where applicable.
- Relator participants → explicit object properties from the Relator class to mediated participants/context.
- Contextual classifications → assignment classes/relators rather than permanent product subclasses.
- Observations → Observation Activity and Observation Result remain distinct.
- Source evidence → Dataset/Release/Record/Assertion/Evidence Support/Provenance Activity remain separate from domain phenomena.

## Protected semantic distinctions
The Formal Gate checks explicit disjointness for the Gate-D distinctions that can be safely represented as OWL disjointness. Identifier values are not modeled as domain identities. The formal source does not collapse Organization with Facility, Geography with Jurisdiction, Product with Substance/Presentation, Observation Activity with Result, Shortage Situation with Source Record, or Supply Capacity with its Observation Result.

## Open-world boundary
OWL axioms are intentionally not used to encode every dataset-level completeness requirement. SHACL provides bounded validation profiles for research-data structures while preserving the distinction between open-world ontology semantics and closed-world validation expectations.

## Residual W4 items
Product/Presentation source granularity, detailed dosage-form/package modeling, empirical population of Supply Dependency, deeper normative UFO-C treatment and exact COVER/ROSE alignment remain bounded follow-up items. None is silently presented as resolved by OWL syntax alone.
