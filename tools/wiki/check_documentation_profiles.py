#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGES = ROOT / "wiki-src" / "pages"
SPEC = ROOT / "wiki-src" / "navigation" / "documentation-profile-model.md"

def main():
    errors = []
    home = (PAGES / "Home.md").read_text(encoding="utf-8")
    profile_page = (PAGES / "Documentation-Profiles.md").read_text(encoding="utf-8")
    spec = SPEC.read_text(encoding="utf-8")

    required_home = [
        "## Documentation profiles",
        "Research / Ontology",
        "Data / Engineering",
        "Software / Product",
        "Business",
        "[[Documentation Profiles]]",
    ]
    for item in required_home:
        if item not in home:
            errors.append(f"Home missing profile declaration: {item}")

    required_profile_states = [
        "| **Research / Ontology** | Active — primary |",
        "| **Data / Engineering** | Active — supporting |",
        "| **Software / Product** | Not declared |",
        "| **Business** | Not declared |",
    ]
    for item in required_profile_states:
        if item not in profile_page:
            errors.append(f"Documentation Profiles missing expected CM-PharmE state: {item}")

    required_spec = [
        "## Profile 1 — Research / Ontology",
        "## Profile 2 — Data / Engineering",
        "## Profile 3 — Software / Product",
        "## Profile 4 — Business",
        "## Ownership boundary matrix",
        "## Cross-profile linking rules",
        "## Multi-profile Home pattern",
        "## Anti-patterns",
        "## CM-PharmE classification",
    ]
    for item in required_spec:
        if item not in spec:
            errors.append(f"profile model missing section: {item}")

    anti_patterns = [
        "Universal mega-template",
        "Ontology-as-product documentation",
        "Database-as-ontology",
        "Demonstrator-as-product",
        "Business Architecture extension = Business Profile",
        "Duplicated definitions",
    ]
    for item in anti_patterns:
        if item not in spec:
            errors.append(f"profile model missing anti-pattern: {item}")

    if "Software / Product | **Active" in profile_page or "Business | **Active" in profile_page:
        errors.append("CM-PharmE must not silently activate Product or Business profiles")

    report = {
        "cm_pharme_profiles": {
            "Research/Ontology": "Active — primary",
            "Data/Engineering": "Active — supporting",
            "Software/Product": "Not declared",
            "Business": "Not declared",
        },
        "profile_families_defined": 4,
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
