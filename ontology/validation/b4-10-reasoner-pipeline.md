# B4.10 — Reproducible ROBOT/HermiT Validation Pipeline

## Purpose

This document describes the repository-controlled OWL logical-validation pipeline introduced in B4.10. It does not change CM-PharmE semantics.

## Toolchain

- ROBOT `v1.9.10`
- ROBOT JAR SHA-256: `16a73c074f3df359a7338a84b4e0788785fe06117f931bb9796e9619ea776105`
- HermiT reasoner through ROBOT
- Python 3.12
- RDFLib `7.5.0`
- Java 21 (Temurin)

The GitHub Actions implementation is `.github/workflows/ontology-reasoner.yml`.

## Input construction

The formal ontology is authored as Turtle modules under `ontology/source/modules/`. `tools/ontology/assemble_modules.py` parses every Turtle module recursively, unions the RDF graphs, removes duplicate triples by graph semantics, serializes a deterministic validation input, and records an assembly manifest with module and output checksums.

This generated validation input is an execution artifact. The modular authoring source remains authoritative.

## Logical validation

The workflow executes ROBOT `reason` with `--reasoner hermit`. ROBOT performs logical validation before classification and returns a non-zero exit code if logical inconsistency or unsatisfiable classes are detected. The workflow preserves the exit code, console log, reasoned ontology, unsatisfiable debug module when produced, source assembly manifest, and a machine-readable reasoner summary.

## Evidence boundary

A successful run is evidence for logical consistency and lack of HermiT-detected unsatisfiable named classes for the exact assembled ontology at that commit. It is not evidence of domain completeness, empirical validity, standards conformance, or correctness of every modeling decision.

A failed or unavailable run must remain visible as failure/unverified evidence; B4 structural checks must never be substituted for OWL DL reasoner evidence.
