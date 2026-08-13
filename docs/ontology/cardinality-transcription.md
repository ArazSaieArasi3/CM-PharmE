# B3 Cardinality Transcription

## Scope

B3 transcribes relation endpoint multiplicities from the preserved CM-PharmE v1.0.0 Draw.io/XML model into a machine-readable cardinality registry under `mappings/cardinality/`.

The registry covers all **40 canonical relation IDs**. `CMPE-R0006` is a generalization and therefore has no association-end multiplicities; it is formalized as `rdfs:subClassOf` while its stable relation ID is retained for traceability.

## Authoritative B3 registry

The complete registry is partitioned into seven files for maintainability:

- `relation-cardinality-01.csv` — R0001–R0010
- `relation-cardinality-02a.csv` — R0011–R0015
- `relation-cardinality-02b.csv` — R0016–R0020
- `relation-cardinality-03a.csv` — R0021–R0025
- `relation-cardinality-03b.csv` — R0026–R0030
- `relation-cardinality-04a.csv` — R0031–R0035
- `relation-cardinality-04b.csv` — R0036–R0040

Each record carries source/target concepts, source/target multiplicities, lifecycle status, cardinality provenance/status, supersession information, and review notes.

## Curated resolutions

### R0001 — governs
The source contains duplicated graphical multiplicity-label objects. B3 retains the primary endpoint pair provisionally as source `1`, target `0..*` and explicitly marks the transcription as provisional.

### R0002 — is mediated by
The source contains two occurrences because `Enterprise Governance Relator` was duplicated as both `relator` and `mode`. B3 takes the occurrence connected to the canonical relator node as authoritative: source `1..*`, target `1`.

### R0011 / R0027 — Strategic Partnership Agreement mediation
The source has a semantic-direction conflict: `mediates` and `is mediated by` for the same concept pair. B3 preserves R0011 for provenance but marks it deprecated, and uses R0027 as the active canonical wording. R0027 retains the multi-actor evidence: source `2..*`, target `1..*`.

### R0031 — constrains
The source lexical label `constraints` is normalized to the grammatical relation label `constrains`; the raw source label is preserved in metadata.

### R0018 and R0039 — material relation
The generic source label is intentionally retained as provisional. B3 does not invent domain-specific predicates without evidence.

## Interpretation rule

The endpoint multiplicity stored in the registry is treated as a constraint on how instances at one end may participate in the relation. OWL restrictions and SHACL constraints derived from these values are generated views; the CSV registry plus the modular ontology source remain the traceable B3 authoring basis.
