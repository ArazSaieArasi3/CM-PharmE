#!/usr/bin/env python3
"""Create a deterministic ZIP bundle of generated CM-PharmE ontology artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", default="ontology")
    parser.add_argument("--output", default="build/cm-pharme-ontology-artifacts.zip")
    args = parser.parse_args()
    artifact_root = Path(args.artifact_root)
    if not artifact_root.is_absolute():
        artifact_root = ROOT / artifact_root
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)

    paths = [
        artifact_root / "source/cm-pharme.ttl",
        artifact_root / "distributions/cm-pharme.ttl",
        artifact_root / "distributions/cm-pharme.owl",
        artifact_root / "distributions/cm-pharme.rdf",
        artifact_root / "distributions/cm-pharme.jsonld",
        artifact_root / "distributions/cm-pharme.nt",
        artifact_root / "shapes/cm-pharme.shacl.ttl",
        artifact_root / "validation/build-manifest.json",
        artifact_root / "validation/SHA256SUMS.txt",
        artifact_root / "validation/quality-report.json",
        artifact_root / "validation/cq-report.json",
    ]
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        raise SystemExit(f"Missing release artifacts: {missing}")

    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(paths, key=lambda p: p.relative_to(artifact_root).as_posix()):
            arcname = path.relative_to(artifact_root).as_posix()
            info = ZipInfo(arcname, date_time=FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)

    summary = {
        "bundle": output.relative_to(ROOT).as_posix() if output.is_relative_to(ROOT) else str(output),
        "sha256": sha256_file(output),
        "bytes": output.stat().st_size,
        "files": len(paths),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
