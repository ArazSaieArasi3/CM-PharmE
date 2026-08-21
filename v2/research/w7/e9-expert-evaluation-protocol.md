# W7-E9 Prospective Structured Expert Evaluation Protocol

## Purpose
Evaluate CM-PharmE 2.0 using real expert judgments that are collected prospectively and kept analytically separate from formal, dataset, held-out and application evidence.

## Integrity rule
No expert result may be synthesized, reconstructed, inferred from prior conversations, or fabricated. The protocol, eligibility criteria, instrument, analysis plan, anonymization rules and reporting boundary are frozen before the first response is collected.

## Expert strata
Recruit experts from two complementary strata:
1. **Pharmaceutical-domain experts** — pharmaceutical ecosystem, regulation, manufacturing, supply chain, market access, pharmacovigilance, clinical research, health-finance or closely related practice/research.
2. **Ontology/conceptual-modeling experts** — ontology engineering, OntoUML/UFO, knowledge graphs, semantic modeling or conceptual modeling.

A participant may qualify for both strata, but the qualification basis must be recorded before response analysis.

## Eligibility
A participant is eligible if they satisfy at least one of the following and can review the supplied model materials independently:
- at least 3 years of relevant professional/research experience in a pharmaceutical-domain area; or
- at least 3 years of relevant professional/research experience in ontology/conceptual modeling/semantic technologies; or
- a doctoral degree or documented peer-reviewed research record directly relevant to one of the two strata.

Exclusion: direct authorship of CM-PharmE 2.0 artifacts under evaluation, inability to provide informed consent, or inability to complete the minimum instrument sections.

## Recruitment target
Target **6–12 completed expert responses**, preferably with representation from both strata and at least two eligible participants in each stratum. This is a recruitment target, not a guarantee of statistical representativeness. If fewer responses are obtained, the sample is reported transparently and interpreted descriptively.

## Materials shown to experts
Provide a controlled review package containing:
- concise purpose and scope of CM-PharmE 2.0;
- modular architecture overview;
- selected OntoUML/UFO conceptual diagrams or equivalent readable views;
- glossary for principal concepts/relations;
- selected competency/use-case examples;
- explicit statement that the review concerns the current frozen model, not a hypothetical future extension.

## Dimensions
The instrument evaluates:
- clarity;
- semantic adequacy;
- domain relevance;
- appropriateness of key distinctions;
- missing concepts/relations;
- usefulness for intended tasks;
- confidence/uncertainty per judgment.

## Rating scale
Unless an item states otherwise, use a five-point ordinal scale:
1 = strongly inadequate / strongly disagree
2 = inadequate / disagree
3 = mixed or uncertain
4 = adequate / agree
5 = strongly adequate / strongly agree

Each scored item also records confidence on a 1–5 scale. Open-text comments are available for missing concepts/relations, inappropriate distinctions and rationale.

## Prospective red-flag rules
The following trigger mandatory review before a strong article claim is made:
- any principal identity distinction is judged semantically incorrect by at least two eligible experts;
- median semantic-adequacy or domain-relevance rating <= 2 for a principal module or protected distinction;
- two or more independent experts identify the same missing concept/relation as critical to an intended principal use case.

A red flag does not automatically require changing the ontology; it requires documented adjudication and either revision or a bounded limitation statement.

## Analysis
Report each dimension separately. Use median, interquartile range, full response counts and favorable-response proportion (ratings 4–5). Do not collapse all dimensions into a single composite score. Report domain and ontology strata separately when sample size permits. Open comments are coded thematically with traceable codes and disagreement retained.

Optional I-CVI may be reported only for relevance items if the number and composition of expert responses make the statistic interpretable; it is supplementary and not the sole acceptance rule.

## Change control
Any ontology change motivated by expert feedback must be recorded as a post-review adaptation with: triggering evidence, decision, affected concepts/relations, rationale, and whether the original expert result is retained unchanged.

## Ethics and privacy
This protocol describes a minimal-risk expert review, but it does **not** claim ethics approval or exemption. The applicable institutional process must be checked before recruitment if required. Participation is voluntary; only the minimum professional-profile metadata needed to establish eligibility is collected; published results are anonymized/pseudonymized.

## Completion rule
W7-E9 is complete only when:
1. this protocol and its companion artifacts were frozen before data collection;
2. real eligible expert responses are available;
3. anonymized results are analyzed under the frozen plan;
4. deviations and post-review adaptations are documented;
5. no fabricated or reconstructed expert result is present.
