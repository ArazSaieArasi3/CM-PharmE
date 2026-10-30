#!/usr/bin/env python3
"""Render minimal review tables from checked JSON inventories."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
inv = json.loads((HERE / "domain-inventory.json").read_text())
defs = json.loads((HERE / "isolate-definitions.json").read_text())
iso_ids = {r["id"] for r in defs["rows"]}
assert len(iso_ids) == 14
lines = [
    "# 2.1 candidate — domains and concepts",
    "",
    "🟨 marks a named-class isolate; isolated titles appear first in each domain. This is the active 144-element candidate including six datatypes. The 60 added elements have provisional primary-domain allocations awaiting author review.",
    "",
    "| Domain | Concepts |",
    "|---|---|",
]
for d in inv["domains"]:
    names = ["🟨 **" + c["title"] + "**" if c["id"] in iso_ids else c["title"] for c in d["concepts"]]
    lines.append(f"| {d['domain']} | {', '.join(names) if names else '— (deferred S-05)'} |")
(HERE / "DOMAIN-TABLE.md").write_text("\n".join(lines) + "\n")

order = {d["domain"]: i for i, d in enumerate(inv["domains"])}
lines = [
    "# مفاهیم منزویِ کاندیدای ۲٫۱",
    "",
    "تعریف‌ها برگردان کوتاه تعریف‌های ویکی نسخهٔ ۲٫۰ هستند؛ این ۱۴ مفهوم هنوز در گراف محدود کلاس‌های نام‌دار منفردند و تصمیم اتصال آنها باز است.",
    "",
    "| دامنه | مفهوم منزوی | تعریف کوتاه |",
    "|---|---|---|",
]
for r in sorted(defs["rows"], key=lambda r: (order[r["domain"]], r["title"])):
    lines.append(f"| {r['domain']} | {r['title']} | {r['definition_fa']} |")
(HERE / "ISOLATES-FA.md").write_text("\n".join(lines) + "\n")
print(f"{len(inv['domains'])} domains; {sum(d['count'] for d in inv['domains'])} active elements; {len(defs['rows'])} isolate definitions")
