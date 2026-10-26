#!/usr/bin/env python3
"""Recheck the reviewed short extraction, optionally against the original PDF."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def verify(pdf=None):
    source = json.loads((HERE / "source-witness.json").read_text())
    excerpts = source["short_excerpts"]
    assert len(" ".join(excerpts).split()) <= 25
    assert hashlib.sha256(("\n".join(excerpts) + "\n").encode()).hexdigest() == source["excerpt_sha256"]
    assert source["manufacturer"]["name"] != source["manufactured_for"]["name"]
    assert excerpts[0] == "Manufactured by: " + source["manufacturer"]["name"]
    assert excerpts[1] == "Manufactured for: " + source["manufactured_for"]["name"]
    result = {"reviewed_extraction_checked": True, "live_download_performed": False,
              "original_pdf_rechecked": False, "source_pdf_sha256": source["pdf_sha256"]}
    if pdf:
        path = Path(pdf)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source["pdf_sha256"]
        assert path.stat().st_size == source["pdf_bytes"]
        text = subprocess.run(["pdftotext", "-layout", str(path), "-"], check=True,
                              capture_output=True, text=True).stdout
        pages = text.split("\f")
        for page in [source["pdf_page_1_based"], source["corroborating_medication_guide_page_1_based"]]:
            for quote in excerpts:
                assert quote in pages[page - 1], (page, quote)
        assert "KEYTRUDA" in pages[0] and "pembrolizumab" in pages[0]
        result["original_pdf_rechecked"] = True
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf")
    args = ap.parse_args()
    print(json.dumps(verify(args.pdf), indent=2))
