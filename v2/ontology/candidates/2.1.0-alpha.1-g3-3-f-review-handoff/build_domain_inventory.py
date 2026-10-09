#!/usr/bin/env python3
"""Crosswalk 17 approved Gate-D domain names to 2.1 candidate class IDs.

The 60 new-class domain assignments are editorial primary-domain proposals.
This script enforces exact coverage and keeps the three deferred Gate-D IDs
outside the current candidate. It does not change ontology semantics.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
NATIVE = HERE.parent / "g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json"
EVIDENCE = HERE.parent / "g3-3-e-connectivity-evidence/connectivity-evidence.json"

CANONICAL_DOMAINS = [
    "Ecosystem Organization", "Facility Operations", "Regulatory Governance",
    "Pharmaceutical Product", "Supply Operations", "Ecosystem Observation",
    "Spatiotemporal Context", "Evidence Traceability", "Entity Identity",
    "Regulatory Policy", "Supply Resilience", "Market Access",
    "Risk Management", "Pharmacovigilance", "Business Architecture",
    "Digital Systems", "Clinical Care",
]

ADDITIONS = {
    "Facility Operations": """
        OperatedFacilityRole OperatingOrganizationRole
    """,
    "Regulatory Governance": """
        AuthorizedFacilityRole AuthorizedOrganizationRole AuthorizedParty
        AuthorizingAuthorityRole RegisteredFacilityRole
        RegisteredOrganizationRole RegisteredParty RegisteringAuthorityRole
    """,
    "Pharmaceutical Product": """
        AppliedClassificationEntryRole ClassifiedEntity
        ClassifiedMedicinalProductRole ClassifiedPharmaceuticalSubstanceRole
        ListedPresentationRole ListingResponsibleOrganizationRole
        ProductLabelCommitmentOrganizationRole ProductLabelResponsibility
        ResponsibilitySubjectProductRole
    """,
    "Supply Operations": """
        AssigningDistributionSiteUseOrganizationRole
        AssigningManufacturingSiteUseOrganizationRole
        CommissioningLogisticsClientRole DistributionSiteUse
        ImportResponsibility ImportResponsibilitySubjectRole
        LogisticsServiceCommitment ManufacturingResponsibility
        ManufacturingResponsibilitySubjectRole ManufacturingSiteUse
        WholesaleResponsibility WholesaleResponsibilitySubjectRole
    """,
    "Evidence Traceability": """
        EvidenceObservationResultRole EvidenceSourceRecordRole
        SupportedAssertionRole
    """,
    "Entity Identity": """
        IdentifiedEntity IdentifiedFacilityRole
        IdentifiedGeographicFeatureRole
        IdentifiedMedicinalProductPresentationRole
        IdentifiedMedicinalProductRole IdentifiedOrganizationRole
        IdentifiedPharmaceuticalSubstanceRole UsedIdentifierSchemeRole
    """,
    "Regulatory Policy": """
        GovernedEntity GovernedFacilityRole GovernedOrganizationRole
        MandateConferringOrganizationRole OversightAuthorityRole
        RegulatoryMandate
    """,
    "Supply Resilience": """
        DependentEntity DependentFacilityRole
        DependentMedicinalProductRole DependentOrganizationRole
        ProviderEntity ProviderFacilityRole ProviderMedicinalProductRole
        ProviderOrganizationRole ReferenceProductRole
    """,
    "Market Access": """
        InstitutionalFundingCommitment InstitutionallyFundedOrganizationRole
    """,
    "Business Architecture": """
        PartnerOrganizationRole
    """,
}


def display(e):
    raw = e["name"]["en"]
    if " " in raw:
        return raw
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", raw)


def main():
    registry = json.loads((HERE / "registry.json").read_text())
    model = json.loads(NATIVE.read_text())
    evidence = json.loads(EVIDENCE.read_text())
    native = {e["id"]: e for e in model["elements"] if e["type"] == "Class"}
    base_ids = [id for module in registry["modules"].values() for id, _ in module]
    assert len(base_ids) == len(set(base_ids)) == 87
    index = (HERE / "concept-index.md").read_text().split("## V2 concepts\n", 1)[1]
    rows = []
    for line in index.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if m and 1 <= int(m[1]) <= 87:
            rows.append((int(m[1]), m[2].strip(), m[3].strip()))
    assert len(rows) == 87 and [n for n, _, _ in rows] == list(range(1, 88))
    approved_domain_for = {base_ids[n - 1]: domain for n, _, domain in rows}
    assert set(approved_domain_for.values()) == set(CANONICAL_DOMAINS)
    deferred = {"AssetAtRisk": "S-04", "Vulnerability": "S-04", "ClinicalCareParticipant": "S-05"}
    assert set(base_ids) - set(native) == set(deferred)
    proposal_domain_for = {}
    for domain, names in ADDITIONS.items():
        assert domain in CANONICAL_DOMAINS
        for name in names.split():
            assert name not in proposal_domain_for
            proposal_domain_for[name] = domain
    assert len(proposal_domain_for) == 60
    assert set(native) - set(base_ids) == set(proposal_domain_for)
    isolated = set(evidence["native"]["isolates"])
    assert len(isolated) == 14 and isolated <= set(native)
    output = defaultdict(list)
    for id, e in native.items():
        domain = approved_domain_for.get(id, proposal_domain_for.get(id))
        assert domain
        output[domain].append({
            "id": id, "title": display(e), "stereotype": e["stereotype"],
            "isolated_in_named_class_graph": id in isolated,
            "domain_assignment": "GATE_D_APPROVED" if id in approved_domain_for else "CANDIDATE_ADDITION_EDITORIAL_REVIEW",
            "source": "W4 canonical 87-row index and registry" if id in approved_domain_for else "Candidate pattern, participants and conceptual anchor; primary domain requires author confirmation",
        })
    records = []
    for domain in CANONICAL_DOMAINS:
        items = sorted(output[domain], key=lambda x: (not x["isolated_in_named_class_graph"], x["title"]))
        records.append({"domain": domain, "count": len(items), "isolate_count": sum(x["isolated_in_named_class_graph"] for x in items), "concepts": items})
    assert sum(r["count"] for r in records) == len(native) == 144
    assert sum(r["isolate_count"] for r in records) == 14
    assert sum(x["stereotype"] == "datatype" for r in records for x in r["concepts"]) == 6
    assert sum(x["domain_assignment"] == "GATE_D_APPROVED" for r in records for x in r["concepts"]) == 84
    assert sum(x["domain_assignment"] == "CANDIDATE_ADDITION_EDITORIAL_REVIEW" for r in records for x in r["concepts"]) == 60
    result = {
        "scope": "Current 2.1 candidate B2 native overlay: 144 classes including 6 datatypes; one primary human-facing domain per element.",
        "domain_taxonomy": "17 W4 Gate-D canonical domain names; 87-row W4 index and native registry",
        "mapping_limit": "84 present baseline IDs retain approved primary domains. The 60 added role/relator primary-domain allocations are editorial proposals for author review. Three Gate-D concepts deferred from the active candidate are not silently counted.",
        "counts": {"canonical_domains": 17, "domains_with_active_concepts": sum(bool(r["count"]) for r in records), "active_elements": 144, "named_classes": 138, "datatypes": 6, "isolated_named_classes": 14, "gate_d_carryovers": 84, "candidate_additions_provisional_domain": 60, "gate_d_deferred": 3},
        "deferred_not_in_active_candidate": deferred,
        "domains": records,
    }
    (HERE / "domain-inventory.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"counts": result["counts"], "domains": [(r["domain"], r["count"], r["isolate_count"]) for r in records]}, indent=2))


if __name__ == "__main__":
    main()
