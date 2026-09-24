# V1 Evaluation Index

> **Page scope:** V1  
> **Documentation maturity:** Stable  
> **Authoritative source:** `main/docs/evaluations/` and `main/evaluation/`  
> **Last synchronized:** 2026-09-23  
> **Related issues/PRs:** V1 evaluation and semantic-engineering closure  
> **Evidence status:** Stable V1 evidence navigation  
> **Future refresh:** None unless V1 evidence is formally corrected  
> **Wiki baseline:** WB-2026.09.1

## Evidence map

| Evaluation area | Current state | Primary repository evidence |
|---|---|---|
| Syntax Validation | PASS | evaluation index / validation pipeline |
| Logical Consistency | PASS for current logical axiom set | ROBOT/HermiT evidence |
| Structural Integrity | PASS | structural extraction/audit |
| Ontological Soundness | CONDITIONAL | semantic/anti-pattern findings |
| Semantic & Expert Validation | PARTIAL | publication/expert evidence; broader independent replication future |
| Data & Mapping Validation | PASS within bounded constructed scenario | scenario/mapping evidence |
| Competency Questions | PASS within bounded expectations | executable CQ regressions |
| Application Validation | PARTIAL / illustrative | vaccine demonstration/application evidence |
| Research Reproducibility | PASS for completed repository-engineering scope | deterministic build/CI evidence |

## Principal records

- [Evaluation overview](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/evaluations/index.md)
- [V1 structural audit](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/evaluations/v1.0.0-structural-audit.md)
- [Formal ontology audit](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/evaluations/b3-formal-ontology-audit.md)
- [Evaluation plan](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/evaluations/b4-evaluation-plan.md)
- [Executed evaluation matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/evaluations/b4-evaluation-matrix.md)
- [Final evaluation report](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/evaluations/b4-final-evaluation.md)
- [Semantic finding disposition](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/evaluations/b4-10-semantic-finding-disposition.md)
- [Machine-readable evaluation area](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/evaluation/README.md)

## Key executed evidence

The selected V1 baseline records:
- 28/28 structural and traceability checks passing;
- 8/8 positive competency queries;
- 4/4 negative regression competency queries;
- a machine-readable vaccine scenario covering all five domains;
- SHACL execution with registered findings retained;
- anti-pattern re-evaluation;
- ROBOT/HermiT logical validation;
- deterministic graph/serialization/build checks.

## Findings that remain visible

V1 evidence deliberately preserves:
- targeted semantic-refinement candidates;
- conditional ontological-soundness findings;
- partial expert/semantic evidence;
- illustrative rather than operational application validation;
- formal/profile boundaries.

## Interpretation rule

Do not convert V1's nine layers into a single quality score. Do not generalize a PASS result beyond the exact procedure that produced it.

## Related pages

[[V1 Evaluation and Evidence]] · [[V1 Reproducibility]] · [[Evaluation and Assurance]]
