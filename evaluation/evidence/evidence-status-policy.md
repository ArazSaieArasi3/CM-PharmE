# Evidence Status Policy

CM-PharmE separates research claims from repository verification state. Evidence records must not imply stronger validation than the recorded procedure supports.

## Status vocabulary

| Status | Meaning |
|---|---|
| `reported-in-published-paper` | Result or claim appears in the published conference paper |
| `reported-in-journal-manuscript` | Result or claim appears in the journal manuscript under review |
| `repository-provenance-recorded` | Source, method, and boundary have been transferred into the repository |
| `repository-structurally-verified` | Repository artifacts have been checked structurally with a documented procedure |
| `repository-computationally-verified` | An executable tool/query/reasoner test has reproduced the relevant result |
| `repository-externally-validated` | Evidence derives from a documented external expert, stakeholder, dataset, or deployment evaluation |
| `not-yet-reproduced` | Publication-reported evidence has not been independently reproduced from repository artifacts |
| `superseded-or-narrowed` | A later research stage retains the historical claim but narrows its current interpretation |

## Required evidence fields

A substantive evaluation record should identify:

- claim or question;
- source publication or repository artifact;
- model/release/commit scope;
- evaluation layer E1–E9;
- method/procedure;
- expected result where applicable;
- observed result;
- evidence status;
- evidential boundary;
- reproducibility information.

## Strength boundaries

- A manual inspection does not establish OWL logical consistency.
- A conceptual answer to a competency question is not an executable query result.
- A constructed scenario does not establish empirical validity.
- An expert panel does not establish statistical generalizability unless the study design supports it.
- A semantic mapping to FHIR, IDMP, or another standard does not by itself establish standards conformance.
- A publication claim is not automatically a current repository verification result.

## Historical evidence

Historical claims are retained even when a later study adopts more conservative wording. The repository records both the original claim and the later boundary so that the research evolution remains auditable.