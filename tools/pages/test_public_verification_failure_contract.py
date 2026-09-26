#!/usr/bin/env python3
"""Intentional negative test for the public Pages verifier contract."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "tools/pages/verify_public_pages.py"

spec = importlib.util.spec_from_file_location("verify_public_pages", TARGET)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

# Deliberately corrupt the first public-surface response. The verifier must reject it
# before any browser work begins; accepting it would be a release-gate defect.
module.fetch = lambda url, attempts=8: b"INTENTIONAL_INVALID_PUBLIC_SURFACE"

try:
    module.verify("https://example.invalid/")
except AssertionError as exc:
    assert "portal entry missing" in str(exc), repr(exc)
    print("PASS: public verifier rejected intentional invalid surface")
else:
    raise AssertionError("public verifier incorrectly accepted intentional invalid surface")
