#!/usr/bin/env python3
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki-src"
PAGES = WIKI / "pages"
BASELINE_ID = "WB-2026.09.1"
DECLARATION_DATE = "2026-09-24"
INITIAL_WIKI_COMMIT = "e470b7a50642a1bc46bcf36bdbea3a6ea0ca60d8"
INITIAL_PUBLICATION_RUN = "35885115760"

def replace(path, old, new, required=False):
    text = path.read_text(encoding="utf-8")
    if required and old not in text:
        raise SystemExit(f"required text not found in {path}: {old!r}")
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")

def set_maturity(filename, value):
    p = PAGES / filename
    text = p.read_text(encoding="utf-8")
    new, count = re.subn(
        r"> \*\*Documentation maturity:\*\*[^\n]*",
        f"> **Documentation maturity:** {value}  ",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit(f"could not set maturity in {p}")
    p.write_text(new, encoding="utf-8")

def main():
    manifest_path = WIKI / "baseline-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("candidate_baseline_id") != BASELINE_ID:
        raise SystemExit("unexpected candidate baseline")
    if manifest.get("declared") is True:
        print("baseline already declared")
        return 0

    for p in sorted(PAGES.glob("*.md")):
        replace(p, BASELINE_ID + " Candidate", BASELINE_ID)

    for name in [
        "Project-Overview.md",
        "Applications-and-Boundaries.md",
        "Scope-and-Research-Boundaries.md",
        "Current-Status-and-Limitations.md",
    ]:
        set_maturity(name, "Stable-to-date / Evolving")

    set_maturity("Repository-and-Branch-Policy.md", "Stable")
    set_maturity("Wiki-Update-Register.md", "Stable")
    set_maturity("Wiki-Authoring-Standard.md", "Stable governance policy")
    set_maturity("Wiki-Versioning-and-Lifecycle.md", "Stable governance policy")
    set_maturity("Wiki-QA-and-Coverage.md", "Stable / QA-approved current baseline")

    home = PAGES / "Home.md"
    replace(home, "> **Candidate Wiki baseline:** WB-2026.09.1  ",
            "> **Current Wiki baseline:** WB-2026.09.1  ", True)
    replace(home, "> **Baseline maturity:** Candidate — not yet QA-declared  ",
            "> **Baseline maturity:** Stable current documentation baseline — QA-approved on 2026-09-24  ", True)
    ht = home.read_text(encoding="utf-8")
    marker = "> **Formal GitHub Release:** none at this synchronization point  "
    if "First controlled Wiki publication:" not in ht:
        ht = ht.replace(
            marker,
            marker + "\n> **First controlled Wiki publication:** 56/56 rendered page URLs verified; initial published Wiki commit "
            + INITIAL_WIKI_COMMIT + "  "
        )
    home.write_text(ht, encoding="utf-8")

    status = PAGES / "Current-Status-and-Limitations.md"
    replace(
        status,
        "## Documentation limitations\n\nThis source package is not yet a declared QA-clean Wiki baseline. It is a candidate foundation. Publication to the GitHub Wiki surface, complete V1/V2 page population, automated QA and snapshot archiving are still required.\n",
        "## Documentation baseline status\n\nWB-2026.09.1 is the current QA-approved documentation baseline. The controlled publication workflow has published the source-complete page set to the GitHub Wiki and verified the rendered surface. V2 remains **Stable-to-date / Evolving**, so later research changes must flow through the governed refresh checkpoints rather than silently changing this baseline.\n",
        True
    )

    qa = PAGES / "Wiki-QA-and-Coverage.md"
    qt = qa.read_text(encoding="utf-8")
    qt = qt.replace(
        "This page does **not** declare WB-2026.09.1 a final/QA-clean published Wiki baseline.\n\nStill required:\n1. #218 — publish/synchronize accepted source to the actual GitHub Wiki repository and verify rendering.\n2. #209 — combined final source + published-surface + status/claim audit.\n3. #217 — archive the QA-approved published baseline with exact Wiki commit/ref.",
        "WB-2026.09.1 has passed source validation, controlled GitHub Wiki publication and rendered-surface verification. The final combined QA audit found no unresolved documentation blocker. The baseline is therefore accepted as the current documentation baseline while V2 itself remains Stable-to-date / Evolving."
    )
    qt = qt.replace(
        "## Publication blocker\n\nThe currently connected GitHub API surface has no direct Wiki write operation. Therefore source completion must not be represented as actual Wiki publication. #218 remains the explicit publication/render-verification gate.",
        "## Publication evidence\n\nThe controlled GitHub Actions publication path successfully cloned and pushed the separate Wiki Git repository. The first controlled publication verified **56/56 rendered URLs with 0 failures** and recorded Wiki commit " + INITIAL_WIKI_COMMIT + ". Issue #218 is closed."
    )
    if "## Final QA disposition" not in qt:
        qt += "\n\n## Final QA disposition\n\n**Disposition: ACCEPTED — WB-2026.09.1 is the current QA-approved documentation baseline.**\n\nEvidence used:\n- source validator and intentional-failure self-test: PASS;\n- controlled Wiki publication: PASS;\n- rendered URL verification: 56/56, 0 failures;\n- initial published Wiki commit: " + INITIAL_WIKI_COMMIT + ";\n- live status re-check on 2026-09-24: #98, #159, #170, #171 and #173 remain open as documented; PR #172 and PR #201 remain open/unmerged;\n- V2 remains Stable-to-date / Evolving; Gate G/H and E9 human evidence remain pending;\n- unresolved documentation-critical blockers: 0.\n\nFuture research changes are handled by #212, #213 and #214.\n"
    qa.write_text(qt, encoding="utf-8")

    lifecycle = PAGES / "Wiki-Versioning-and-Lifecycle.md"
    replace(
        lifecycle,
        "The initial source-controlled candidate is **WB-2026.09.1**. It must not be described as a frozen or final Wiki baseline until the required QA gate has passed.",
        "The first declared current documentation baseline is **WB-2026.09.1**. It passed the required source, publication and rendered-surface QA gates. This declaration freezes the documentation snapshot only; it does **not** declare CM-PharmE 2.0 final or frozen.",
        True
    )

    register = PAGES / "Wiki-Update-Register.md"
    rt = register.read_text(encoding="utf-8")
    rt = rt.replace("WB-2026.09.1 (Candidate)", "WB-2026.09.1 (Declared current baseline)")
    row = "| 2026-09-24 | WB-2026.09.1 (Declared current baseline) | Full current source-complete Wiki baseline | #209, #217, #218 | main current declaration source | v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999 | Documentation release | Source QA PASS; first controlled publish 56/56 rendered URLs PASS; V2 remains evolving | Future refresh checkpoints #212/#213/#214 |\n"
    header = "|---|---|---|---|---|---|---|---|---|\n"
    if row not in rt:
        rt = rt.replace(header, header + row, 1)
    register.write_text(rt, encoding="utf-8")

    readme = WIKI / "README.md"
    rd = readme.read_text(encoding="utf-8")
    rd = rd.replace("- Candidate Wiki baseline: **WB-2026.09.1**", "- Current Wiki baseline: **WB-2026.09.1**")
    rd = rd.replace("- Candidate maturity: **Candidate**", "- Documentation maturity: **Stable current baseline**")
    rd = rd.replace("- Wiki publication state: **source-controlled draft; GitHub Wiki publication still requires synchronization**",
                    "- Wiki publication state: **published through the controlled Wiki synchronization workflow; rendered verification passed**")
    readme.write_text(rd, encoding="utf-8")

    manifest.update({
        "declared": True,
        "maturity": "Stable",
        "declared_date": DECLARATION_DATE,
        "wiki_publication_state": "published and rendered-verified; declaration synchronization controlled by wiki-publish workflow",
        "initial_controlled_publication": {
            "source_commit": "d8251c9adb0b485b811e03269f19d18963ccf473",
            "wiki_commit": INITIAL_WIKI_COMMIT,
            "workflow_run": INITIAL_PUBLICATION_RUN,
            "rendered_urls_expected": 56,
            "rendered_urls_verified": 56,
            "failures": 0
        }
    })
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    inv = WIKI / "page-inventory.csv"
    rows = list(csv.DictReader(inv.open(encoding="utf-8", newline="")))
    fields = list(rows[0].keys())
    for row in rows:
        if row["source_status"] == "source-complete":
            row["publish_status"] = "published"
    with inv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    final = WIKI / "qa" / "WB-2026.09.1-final-qa.md"
    final.write_text(
        "# WB-2026.09.1 — Final Combined QA\n\n"
        "Date: 2026-09-24\n\n"
        "## Disposition\n\n"
        "**ACCEPTED — current QA-approved documentation baseline.**\n\n"
        "This disposition applies to the Wiki/documentation baseline only. CM-PharmE 2.0 remains **Stable-to-date / Evolving**.\n\n"
        "## Source QA\n- Wiki source validator: PASS.\n- Intentional invalid-fixture self-test: PASS.\n- Page inventory / metadata / internal-link / duplicate-slug controls: PASS.\n\n"
        "## Publication QA\n- Controlled publication workflow run: 35885115760.\n- Initial controlled published Wiki commit: " + INITIAL_WIKI_COMMIT + ".\n- Expected rendered URLs: 56.\n- Verified rendered URLs: 56.\n- Failures: 0.\n\n"
        "## Status freshness re-check\nChecked on 2026-09-24:\n- #98 open.\n- #159 open.\n- #170 open.\n- #171 open.\n- #173 open.\n- PR #172 open/unmerged.\n- PR #201 open/unmerged.\nNo Wiki statement implies completion of these dependencies.\n\n"
        "## Known intentional pending content\n- Representative Task Evaluation remains future-refresh content under #212 after W8/Gate G stabilization.\n\n"
        "## Blocking finding register\n- Unresolved documentation-critical blockers: **0**.\n\n"
        "## Future synchronization\n- #212 — post-W8 / Gate G.\n- #213 — post-human-review semantic stabilization.\n- #214 — final V2 freeze/release.\n",
        encoding="utf-8"
    )

    print(json.dumps({
        "baseline": BASELINE_ID,
        "declared": True,
        "source_complete_pages": sum(1 for r in rows if r["source_status"] == "source-complete"),
        "planned_pages": [r["page"] for r in rows if r["source_status"] != "source-complete"]
    }))
    return 0

if __name__ == "__main__":
    sys.exit(main())
