# EvidenceRecord projection and witness-contract decision — #323

Profile **CMPE-EvidenceRecordProjection/0.1.0**; prospective admission contract
**CMPE-QualifiedEvidenceWitness/0.2.0**. Delegated scoped candidate decisions.

| ID | Decision | Rationale and boundary |
|---|---|---|
| ER-D01 | evidenceRecord is a derived unstereotyped native Association over evidenceItem, filtered by EvidenceSupport and explicit EvidenceSourceRecordRole type/subtype. | Preserve existing IDs, role/nature, subsetting and prior ContextClass behavior. Do not infer the qualified role from SourceRecord alone or invent a primitive fact. |
| ER-D02 | Target 0..1 and inverse 0..*; target readOnly=true and inverse=false. | An EvidenceItem can be non-record evidence; a record need not support a contextual claim through this view. These are explicit model choices, not empirical frequencies. |
| ER-D03 | Primitive evidenceItem target readOnly=true under established EvidenceSupport identity. | Changing the supporting individual requires a different support identity. Missing data, different IRIs and a shared external code do not establish individual replacement. This does not establish the truth of the supported assertion. |
| ER-D04 | Version one witness-contract transition explicitly: a qualified existing primitive record fact is sufficient even when the redundant shortcut is absent. | Preserve the original false expectation and the earlier 88/89 observation. Prospective true is a newly adopted admission rule, not a rewritten historical oracle. |
| ER-D05 | Keep missing primitive evidence and a missing qualified role as genuine negatives for the documented-commitment witness. | An unsupported/stale shortcut must fail exact-projection validation. No claim that every non-record EvidenceSupport is invalid. |
| ER-D06 | Produce a separate candidate with exactly seven field changes relative to #322. | All earlier snapshots/evidence and every other field remain untouched; existing four-rule reports keep their historical inputs. |
| ER-D07 | Close only bounded implementation acceptance after native, SHACL/regression, finite identity and HermiT evidence. | No independent scientific acceptance, complete modern validator/20-family run, production migration, final GA tag or automatic claim-truth inference. |

Basis: concept passports C048 Evidence Item (a role serving as evidence), C049
Evidence Support (support truth-maker), C043 Source Record, and the preserved
three-proposal laboratory and original commitment counterexample. The specific
support-identity and admission policy is a candidate design decision. It is not
implied by an external source record key or by OWL/SHACL success.

Completion: 12 new SHACL cases, 12 preserved ContextClass cases, all 89 historical
rows with before=89/89, original-after=88/89 and prospective-after=89/89 under one
named transition; two genuine negative replacements; ten finite identity traces;
six HermiT expectations; two bounded native subsetting rows, guarded serialization
and six unauthorized-change refusals. Expected outcomes are frozen before code.
