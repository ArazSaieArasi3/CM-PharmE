# CM-PharmE 2.0 — Expert Review Brief

## Purpose of this review
You are invited to independently evaluate the current frozen CM-PharmE 2.0 conceptual model. The review concerns semantic adequacy, domain relevance, clarity, modular boundaries, provenance semantics, intended task usefulness, and potentially missing or inappropriate concepts/relations.

This is an expert review of the current model. Please evaluate what is present now rather than a hypothetical future extension.

## Model scope
CM-PharmE 2.0 is a pharmaceutical-ecosystem ontology and knowledge-infrastructure model grounded in UFO/OntoUML-style conceptualization and designed to support traceable realization across ontology, relational-database, and knowledge-graph representations.

The frozen conceptual registry contains **87 conceptual elements**:
- **32 Core** elements;
- **25 cross-cutting infrastructure (X-INFRA)** elements;
- **30 optional Extension** elements.

The project-native conceptual registry is a deterministic representation of the frozen conceptual decisions. It is **not** claimed to be an official OntoUML JSON export.

## Principal conceptual areas
The Core covers organizations and ecosystem roles, facilities and facility operation, regulatory authorization and establishment registration, regulatory jurisdiction, medicinal products, pharmaceutical substances, product presentations, classification, market listing, manufacturing/distribution activities, shortage situations, supply capacity, and observation-result specializations.

X-INFRA covers geography, time/reporting datatypes, dataset/release/source-record provenance, assertions and evidence support, observation activity/result semantics, identifiers, entity matching, provenance activity, and data-quality findings.

Extensions include regulation, contextual essential/critical-medicine classification, alternative medicines, supply dependency, disruption/procurement/stockout concepts, reimbursement/utilisation observations, risk and resilience concepts, pharmacovigilance, business-architecture view concepts, digital information-system components, and clinical-care participation.

## Protected distinctions to examine carefully
The current model deliberately keeps the following distinctions explicit:
1. Organization vs Facility
2. Facility vs Geographic Feature
3. Geographic Feature vs Regulatory Jurisdiction
4. Medicinal Product vs Pharmaceutical Substance
5. Medicinal Product vs Medicinal Product Presentation
6. Observation Activity vs Observation Result
7. Medicine Shortage Situation vs Source Record
8. Supply Capacity vs Supply Capacity Observation Result

Please rate these distinctions using the supplied frozen instrument and identify any distinction you consider semantically inappropriate, unnecessary, or insufficiently justified.

## Provenance pattern
The intended provenance chain distinguishes data sources and their releases from individual source records, assertions/observations, and evidence-support relations. The purpose is to keep claims traceable to source material without collapsing a source record into the real-world entity or situation it describes.

## Intended task families
The model is intended to support, within its stated boundaries:
- pharmaceutical-ecosystem semantic integration;
- ontology↔relational-database↔knowledge-graph traceability;
- actor/facility and jurisdiction-aware integration;
- shortage/resilience-oriented representation and analysis;
- provenance-aware querying and interpretation.

Please judge whether the current model is adequate for these task families and state any critical limitation.

## What is not being claimed in this review
The review package does not ask you to validate global pharmaceutical-domain completeness, prediction accuracy, operational resilience effectiveness, standards conformance, or AI performance. Those are separate claims and evidence families.

## Review procedure
Use the frozen 23-item expert instrument. Rating items use a 1–5 ordinal scale. Item-level confidence is recorded where requested. For any critical rating or material concern, provide a short rationale so that the finding can be adjudicated traceably.

Open-text questions explicitly invite you to identify:
- critically missing concepts;
- critically missing relations;
- inappropriate or unnecessarily complex distinctions/classes/relations.

## Independence and privacy
Participation is voluntary. Only minimum professional-profile metadata needed to establish eligibility is collected. Public research outputs use pseudonymous participant IDs; identifiable contact/consent material is not committed to the public repository.

This participant brief operationalizes the frozen E9 protocol; it does not modify the frozen eligibility rules, instrument, scoring, red-flag criteria, or analysis plan.