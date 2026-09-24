#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGES = ROOT / "wiki-src" / "pages"

EXPECTED_H1 = {
    "V2-Research-Program-and-Gates.md": "CM-PharmE 2.0 Research Method and Development",
    "V2-Evaluation-E1-E13.md": "CM-PharmE 2.0 Evaluation Framework",
    "V2-Human-Ontology-Review.md": "CM-PharmE 2.0 Semantic Review",
    "Gate-and-Claim-Dispositions.md": "Evidence Scope and Supported Claims",
}

EXPECTED_ALIASES = {
    "V2 Research Program and Gates": "CM-PharmE 2.0 Research Method and Development",
    "V2 Evaluation E1-E13": "CM-PharmE 2.0 Evaluation Framework",
    "V2 Human Ontology Review": "CM-PharmE 2.0 Semantic Review",
    "Gate and Claim Dispositions": "Evidence Scope and Supported Claims",
}

FORBIDDEN_H1 = [
    re.compile(r"\bGate\b", re.I),
    re.compile(r"\bWave\b", re.I),
    re.compile(r"Human Ontology Review", re.I),
    re.compile(r"E1\s*[-–]\s*E13", re.I),
]

LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")

def h1(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None

def visible_links(path):
    result = []
    text = path.read_text(encoding="utf-8")
    for target, alias in LINK_RE.findall(text):
        result.append((target.strip(), (alias or target).strip()))
    return result

def count_exposure():
    result = {"gate": 0, "wave": 0, "human_review": 0, "pages": len(list(PAGES.glob("*.md")))}
    for path in PAGES.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        result["gate"] += len(re.findall(r"\bGate\b", text))
        result["wave"] += len(re.findall(r"\bW[0-8]\b|\bWave\b", text))
        result["human_review"] += len(re.findall(r"Human Review|Human Ontology Review|human review", text, re.I))
    return result

def main():
    errors = []

    for filename, expected in EXPECTED_H1.items():
        path = PAGES / filename
        actual = h1(path)
        if actual != expected:
            errors.append(f"{filename}: expected H1 '{expected}', got '{actual}'")

    for path in PAGES.glob("*.md"):
        title = h1(path)
        if not title:
            continue
        for pattern in FORBIDDEN_H1:
            if pattern.search(title):
                errors.append(f"{path.name}: internal-process terminology exposed in canonical H1: '{title}'")
                break

    for nav_name in ["Home.md", "_Sidebar.md"]:
        nav = dict(visible_links(PAGES / nav_name))
        for target, label in EXPECTED_ALIASES.items():
            if nav.get(target) != label and not (nav_name == "_Sidebar.md" and target == "V2 Research Program and Gates" and nav.get(target) == "Research Method and Development") and not (nav_name == "_Sidebar.md" and target == "V2 Evaluation E1-E13" and nav.get(target) == "Evaluation Framework") and not (nav_name == "_Sidebar.md" and target == "V2 Human Ontology Review" and nav.get(target) == "Semantic Review") and not (nav_name == "_Sidebar.md" and target == "Gate and Claim Dispositions" and nav.get(target) == "Evidence Scope and Supported Claims"):
                errors.append(f"{nav_name}: target [[{target}]] lacks approved reader-facing alias; got '{nav.get(target)}'")

    standard = (PAGES / "Wiki-Authoring-Standard.md").read_text(encoding="utf-8")
    if "reader-facing-terminology.md" not in standard:
        errors.append("Wiki Authoring Standard does not reference the canonical terminology policy")

    print(json.dumps({"exposure_metrics": count_exposure(), "errors": errors}, indent=2))
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
