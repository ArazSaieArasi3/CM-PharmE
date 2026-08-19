# W7-E5 — SHACL and Data-Conformance Evaluation

## Status
**Mandatory Gate-E fixture conformance: PASS**  
**Family interpretation: PASS WITH WARNING**

W7-E5 evaluates the frozen Gate-E schema-faithful fixture graph against both the frozen W5 SHACL profile and a W7-E5 evaluation-only research-integrity SHACL profile. The latter operationalizes provenance, geography, observation and entity-match integrity measures already frozen in the W7 protocol; it does not modify the W5 ontology or W5 SHACL baseline.

## Frozen evaluation inputs
- W5 SHACL: `v2/ontology/shapes/cm-pharme-v2.shacl.ttl`
- W7-E5 integrity profile: `v2/evaluation/protocol/e5-data-integrity-shapes.ttl`
- controlled mutation registry: `v2/evaluation/protocol/e5-controlled-mutations.json`
- evaluation target: deterministic Gate-E schema-faithful fixture KG
- held-out H1–H3: not used

The E5 integrity profile and controlled mutation cases were committed before the first E5 CI execution. The mutation cases are sensitivity probes on copies of the synthetic fixture; they are not real-data findings.

## Final CI evidence
- GitHub Actions run: `32282623007`
- conclusion: **SUCCESS**
- evidence artifact: `cm-pharme-v2-w7-e5-shacl-evidence`
- artifact ID: `9376416247`
- artifact digest: `sha256:0ca0ac4145f4d3aa5128d55daf518007f352838e2de39a6cfe720e0326d69c3c`

## Pristine fixture result
| Measure | Result |
|---|---:|
| Fixture triples | 398 |
| W5 SHACL conforms | true |
| W5 SHACL results | 0 |
| W7-E5 integrity profile conforms | true |
| W7-E5 integrity results | 0 |
| Combined profile conforms | true |
| Combined violations/warnings/info | 0 |

### Integrity completeness on evaluated fixture
| Integrity dimension | Result |
|---|---:|
| SourceRecord → provenance activity | 7/7 |
| Facility → geography | 2/2 |
| Observation → product/presentation context | 28/28 |
| Observation → geography | 28/28 |
| Observation → source provenance (`wasDerivedFrom`) | 28/28 |
| Observation → transformation provenance (`wasGeneratedBy`) | 28/28 |
| IdentifierAssignment → entity | 4/4 |
| IdentifierAssignment → scheme | 4/4 |
| EvidenceSupport → source record | 7/7 |
| EvidenceSupport → assertion | 7/7 |

## Shape activation and coverage boundary
The pristine fixture directly activates only **3 of the 11 W5 NodeShapes**:
- `MedicinalProductPresentationShape` — 2 focus nodes;
- `IdentifierAssignmentShape` — 4 focus nodes;
- `EvidenceSupportShape` — 7 focus nodes.

The other eight W5 shapes have zero direct focus nodes in this fixture because the Gate-E synthetic population does not instantiate those corresponding classes (e.g., authorization, registration, shortage, supply dependency and contextual medicine classification patterns).

The W7-E5 integrity profile adds six evaluation-only shapes, all of which are activated in the fixture:
- DatasetRelease trace — 2 focus nodes;
- EntityMatch audit — 2;
- Facility geography — 2;
- MatchConfidence value — 2;
- Observation integrity — 28;
- SourceRecord provenance — 7.

This is why the family interpretation is **PASS WITH WARNING** rather than an unqualified global SHACL-conformance claim: the mandatory controlled regression fixture conforms, but it does not exercise every W5 domain shape.

## Controlled mutation sensitivity review
Eight predefined graph mutations were applied one at a time to copies of the pristine fixture. All **8/8** produced the expected registered SHACL finding:

1. remove `presentationOf` → Violation detected;
2. remove `evidenceAssertion` → Violation detected;
3. remove `identifierScheme` → Violation detected;
4. remove Facility `locatedIn` → Violation detected;
5. remove Observation `prov:wasDerivedFrom` → Violation detected;
6. remove Observation `dct:spatial` → Violation detected;
7. add shortage situation without jurisdiction → Warning detected;
8. remove SourceRecord `prov:wasGeneratedBy` → Violation detected.

The warning case remains conformant under the configured `allow_warnings` policy, as intended. The seven Violation cases become non-conformant.

### Interpretation of mutation review
The 8/8 result demonstrates sensitivity for these selected, predefined defects. It **does not** estimate a population-level false-positive or false-negative rate. No random or representative sample of all possible invalid graphs was generated.

## Empirical boundary
- full admitted real datasets were **not** executed in W7-E5;
- H1–H3 held-out sources were **not** used;
- zero findings on the pristine synthetic fixture do not imply zero violations in real operational data;
- W7-E5 does not establish domain completeness, global data quality, standards conformance or application effectiveness;
- real-source mapping/data findings remain to W7-E6/E7 and held-out conformance/generalizability to W7-E8.

## Manuscript-safe claim
The manuscript may state that the Gate-E schema-faithful regression fixture conformed to the frozen W5 SHACL profile and the W7-E5 provenance/geography/observation integrity profile, with zero findings on the pristine fixture and successful detection of all eight predefined controlled mutation cases. The statement must retain that only 3/11 W5 domain NodeShapes had direct fixture focus nodes and that full real/held-out data conformance was not evaluated in E5.

## Next
W7-E6 / V2-068 / #95 — dataset-to-ontology mapping-quality evaluation.
