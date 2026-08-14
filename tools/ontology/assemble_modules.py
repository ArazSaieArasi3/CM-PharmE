from __future__ import annotations

import hashlib
import json
from pathlib import Path

from rdflib import Graph

MODULE_ROOT = Path("ontology/source/modules")
OUTPUT_DIR = Path("build/ontology")
OUTPUT_TTL = OUTPUT_DIR / "cm-pharme.ttl"
MANIFEST = OUTPUT_DIR / "assembly-manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    modules = sorted(MODULE_ROOT.rglob("*.ttl"))
    if not modules:
        raise SystemExit("No Turtle modules found under ontology/source/modules")

    graph = Graph()
    module_records = []
    for module in modules:
        before = len(graph)
        graph.parse(module, format="turtle")
        module_records.append(
            {
                "path": module.as_posix(),
                "sha256": sha256(module),
                "graph_size_after_parse": len(graph),
                "new_triples_after_union": len(graph) - before,
            }
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=OUTPUT_TTL, format="turtle")

    manifest = {
        "schema_version": 1,
        "source_root": MODULE_ROOT.as_posix(),
        "module_count": len(modules),
        "canonical_union_triples": len(graph),
        "output": OUTPUT_TTL.as_posix(),
        "output_sha256": sha256(OUTPUT_TTL),
        "modules": module_records,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"Merged {len(modules)} Turtle modules into {len(graph)} unique RDF triples")
    print(f"Wrote {OUTPUT_TTL} ({manifest['output_sha256']})")


if __name__ == "__main__":
    main()
