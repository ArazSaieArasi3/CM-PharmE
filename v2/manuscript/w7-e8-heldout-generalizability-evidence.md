# Manuscript Evidence Note — W7-E8 Held-out Generalizability

## Manuscript-safe result
CM-PharmE 2.0 was evaluated prospectively against three protected held-out source families that were not used for W3 concept/relation admission: ClinicalTrials.gov/AACT (H1), openFDA Drug Shortages (H2), and India NLEM 2022 (H3). Source/version/access metadata, 51 normalized semantic requirements and 12 held-out competency questions were frozen before first-pass mapping results were written.

Against the unchanged formal ontology baseline, **23/51 (45.10%)** held-out requirements were represented exactly and **38/51 (74.51%)** were represented exactly or partially. The unseen-concept rate was **5/30 (16.67%)**, while the unseen-relation rate was **8/21 (38.10%)**. Held-out competency questions were exactly answerable for **5/12 (41.67%)** and exactly or partially answerable for **9/12 (75.00%)**.

Performance differed by source family. H2 openFDA Drug Shortages achieved **18/18 exact-or-partial** first-pass representation, and H3 India NLEM 2022 achieved **13/14 exact-or-partial** representation. H1 ClinicalTrials.gov/AACT exposed substantial clinical-trial-specific extension pressure: the ontology could reuse Organization, Facility, Geography and pharmaceutical product/substance/presentation distinctions, but explicit Clinical Study, Arm/Group, Outcome, Phase/Status and study-specific relations were absent.

## Interpretation
The held-out findings support **bounded representational generalizability**, not global domain completeness. Importantly, no first-pass finding required reversing the frozen identity distinctions or modifying the Gate-D Core. No ontology adaptation was applied before first-pass scoring.

Three post-test adaptation packages were recorded separately: a Clinical Trials Extension, a Shortage Reporting Refinement, and an Essential-Medicines Refinement. Any later implementation must be reported as post-test adaptation and must not be counted as initial held-out success.

## Reproducibility
GitHub Actions run `32371213714`: SUCCESS.
Artifact `9407208016`, digest `sha256:47cac3a8d7a7218b010322cee046637bd92916b43b41b0733498fa44c9763fe6`.
Frozen ontology fingerprint remained `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`.

## Claim boundary
Do not write that the ontology is globally complete or that it fully supports clinical-trial semantics. The defensible claim is that the Core generalized well to held-out shortage and national essential-medicine semantics, while clinical-trial-specific gaps were exposed transparently as modular extension pressure.
