# Wiki Update Register

> **Page scope:** Version-neutral governance  
> **Documentation maturity:** Stable  
> **Last synchronized:** 2026-09-23  
> **Related issues:** #202, #210, #211, #212, #213, #214, #217

This register records material CM-PharmE Wiki synchronization events.

| Date | Candidate/Baseline | Pages / area | Trigger | V1 ref | V2 ref | Impact class | Evidence/status change | Follow-up |
|---|---|---|---|---|---|---|---|---|
| 2026-09-24 | WB-2026.09.1 | Diagram standard, manifest, four sample notation artifacts, authoring/CI rules | #232 | V1 semantic content unchanged; legacy diagram assets inventoried | V2 semantic content unchanged; current PlantUML source inventoried | Documentation-only / visual standard | Formal notation selection, source→SVG artifact contract, accessibility and staleness rules established | #233–#235 ontology/research visuals; #236 ERD; #237 KG/data-flow visuals |
| 2026-09-24 | WB-2026.09.1 | Documentation profile model, Home profile declaration, Documentation Profiles page | #242 | V1 semantic content unchanged | V2 semantic content unchanged | Documentation-only / profile architecture | Research/Ontology declared primary; Data/Engineering supporting; Software/Product and Business explicitly not declared | #243 / OGCM-RF#45–#50 generalization |
| 2026-09-24 | WB-2026.09.1 | 58 reader-facing pages + templates/authoring metadata contract | #231 | V1 semantic content unchanged | V2 semantic content unchanged | Documentation-only / metadata presentation | Compact 3-field headers; complete provenance moved to collapsible Documentation record; top metadata lines reduced 470→213 with 0 provenance-contract errors | #240 final editorial pass |
| 2026-09-24 | WB-2026.09.1 | Home/Sidebar and nine reader-centered section landing pages | #230 / PR #247 | V1 semantic content unchanged | V2 semantic content unchanged; navigation-only | Documentation-only / information architecture | Reader journeys introduced; all source-complete pages reachable from Home within <=2 steps; zero orphan/unreachable pages | #231 metadata progressive disclosure; #242 multi-profile composition |
| 2026-09-24 | WB-2026.09.1 | Home/Sidebar, V2 research method, evaluation, semantic review, supported-claims and evolution pages | #229 / PR #246 | V1 semantic content unchanged | v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999 | Documentation-only / editorial | Reader-facing terminology separated from internal Gate/Wave/HORP controls; no semantic/evidence/status change | #230 IA/slug review; #231 metadata progressive disclosure; #240 final editorial pass |
| 2026-09-24 | WB-2026.09.1 (Declared current baseline) | Full current source-complete Wiki baseline | #209, #217, #218 | main current declaration source | v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999 | Documentation release | Source QA PASS; first controlled publish 56/56 rendered URLs PASS; V2 remains evolving | Future refresh checkpoints #212/#213/#214 |
| 2026-09-23 | WB-2026.09.1 (Declared current baseline) | Governance foundation, authoring contract, Home/navigation source | #202, #210, #215, #203 | `5099888668d35f798e4759e3534e707ed906db24` | `1226b0a5484f8f5d3a8d214e0d0f52f066b88999` | Documentation-only / governance | Establishes versioning and source-controlled Wiki pipeline; does not change research semantics | Populate V1/V2 content, QA, publish/synchronize to GitHub Wiki |

## Required fields for future entries

Every material synchronization entry must identify:
- date;
- Wiki candidate/baseline identifier;
- pages or documentation family affected;
- triggering issue/PR/gate/release;
- source refs checked;
- impact class;
- evidence/status change;
- unresolved follow-up.

A change must not be described as a semantic update unless the corresponding semantic decision already exists in the authoritative research artifacts.
