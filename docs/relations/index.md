# CM-PharmE Relations

The v1.0 diagram contains **41 labeled semantic relation occurrences**. The canonical registry contains **40 relations** after collapsing one exact duplicate caused by the duplicated `Enterprise Governance Relator` node. One unlabeled self-loop graphical artifact is excluded.

Relation stereotype counts in the canonical registry: **19 material**, **8 mediation**, **6 characterization**, **4 componentOf**, **2 association**, and **1 generalization**.

| ID | Label | Type | Source | Target | Review |
|---|---|---|---|---|---|
| [`CMPE-R0001`](cmpe-r0001.md) | governs | material | `CMPE-C0001` | `CMPE-C0003` | — |
| [`CMPE-R0002`](cmpe-r0002.md) | is mediated by | mediation | `CMPE-C0003` | `CMPE-C0025` | exact duplicate collapsed |
| [`CMPE-R0003`](cmpe-r0003.md) | is part of | componentOf | `CMPE-C0002` | `CMPE-C0001` | — |
| [`CMPE-R0004`](cmpe-r0004.md) | characterizes | characterization | `CMPE-C0005` | `CMPE-C0001` | — |
| [`CMPE-R0005`](cmpe-r0005.md) | characterizes | characterization | `CMPE-C0006` | `CMPE-C0002` | — |
| [`CMPE-R0006`](cmpe-r0006.md) | specializes | generalization | `CMPE-C0007` | `CMPE-C0003` | — |
| [`CMPE-R0007`](cmpe-r0007.md) | is mediated by | mediation | `CMPE-C0008` | `CMPE-C0009` | — |
| [`CMPE-R0008`](cmpe-r0008.md) | fulfills | material | `CMPE-C0039` | `CMPE-C0010` | — |
| [`CMPE-R0009`](cmpe-r0009.md) | characterizes | characterization | `CMPE-C0008` | `CMPE-C0011` | — |
| [`CMPE-R0010`](cmpe-r0010.md) | is part of | componentOf | `CMPE-C0012` | `CMPE-C0013` | source label: is part of a |
| [`CMPE-R0011`](cmpe-r0011.md) | mediates | mediation | `CMPE-C0008` | `CMPE-C0014` | direction semantics review |
| [`CMPE-R0012`](cmpe-r0012.md) | participates in | association | `CMPE-C0015` | `CMPE-C0003` | — |
| [`CMPE-R0013`](cmpe-r0013.md) | is part of | componentOf | `CMPE-C0016` | `CMPE-C0015` | — |
| [`CMPE-R0014`](cmpe-r0014.md) | is mediated by | mediation | `CMPE-C0017` | `CMPE-C0018` | — |
| [`CMPE-R0015`](cmpe-r0015.md) | is mediated by | mediation | `CMPE-C0019` | `CMPE-C0018` | — |
| [`CMPE-R0016`](cmpe-r0016.md) | assigns | material | `CMPE-C0020` | `CMPE-C0021` | — |
| [`CMPE-R0017`](cmpe-r0017.md) | participates in | association | `CMPE-C0022` | `CMPE-C0021` | — |
| [`CMPE-R0018`](cmpe-r0018.md) | material relation | material | `CMPE-C0023` | `CMPE-C0024` | generic label review recommended |
| [`CMPE-R0019`](cmpe-r0019.md) | is mediated by | mediation | `CMPE-C0024` | `CMPE-C0004` | — |
| [`CMPE-R0020`](cmpe-r0020.md) | characterizes | characterization | `CMPE-C0026` | `CMPE-C0004` | — |
| [`CMPE-R0021`](cmpe-r0021.md) | characterizes | characterization | `CMPE-C0027` | `CMPE-C0026` | — |
| [`CMPE-R0022`](cmpe-r0022.md) | mitigates | material | `CMPE-C0028` | `CMPE-C0027` | — |
| [`CMPE-R0023`](cmpe-r0023.md) | enables | material | `CMPE-C0029` | `CMPE-C0015` | — |
| [`CMPE-R0024`](cmpe-r0024.md) | mediates | mediation | `CMPE-C0032` | `CMPE-C0031` | semantic direction to validate |
| [`CMPE-R0025`](cmpe-r0025.md) | records | material | `CMPE-C0033` | `CMPE-C0034` | — |
| [`CMPE-R0026`](cmpe-r0026.md) | enables | material | `CMPE-C0035` | `CMPE-C0018` | — |
| [`CMPE-R0027`](cmpe-r0027.md) | is mediated by | mediation | `CMPE-C0008` | `CMPE-C0014` | direction semantics review |
| [`CMPE-R0028`](cmpe-r0028.md) | governs | material | `CMPE-C0032` | `CMPE-C0001` | — |
| [`CMPE-R0029`](cmpe-r0029.md) | is part of | componentOf | `CMPE-C0018` | `CMPE-C0015` | — |
| [`CMPE-R0030`](cmpe-r0030.md) | characterizes | characterization | `CMPE-C0034` | `CMPE-C0018` | — |
| [`CMPE-R0031`](cmpe-r0031.md) | constraints | material | `CMPE-C0036` | `CMPE-C0037` | wording review recommended |
| [`CMPE-R0032`](cmpe-r0032.md) | informs | material | `CMPE-C0038` | `CMPE-C0036` | — |
| [`CMPE-R0033`](cmpe-r0033.md) | informs | material | `CMPE-C0038` | `CMPE-C0001` | — |
| [`CMPE-R0034`](cmpe-r0034.md) | informs | material | `CMPE-C0038` | `CMPE-C0028` | — |
| [`CMPE-R0035`](cmpe-r0035.md) | follows | material | `CMPE-C0037` | `CMPE-C0022` | — |
| [`CMPE-R0036`](cmpe-r0036.md) | governs | material | `CMPE-C0009` | `CMPE-C0013` | — |
| [`CMPE-R0037`](cmpe-r0037.md) | records | material | `CMPE-C0033` | `CMPE-C0017` | — |
| [`CMPE-R0038`](cmpe-r0038.md) | assists | material | `CMPE-C0030` | `CMPE-C0016` | — |
| [`CMPE-R0039`](cmpe-r0039.md) | material relation | material | `CMPE-C0009` | `CMPE-C0039` | generic label review recommended |
| [`CMPE-R0040`](cmpe-r0040.md) | engages in | material | `CMPE-C0001` | `CMPE-C0014` | — |

Each relation has its own page under this directory. Cardinalities remain authoritative in the source diagram; a dedicated cardinality transcription/validation pass is intentionally separated from this semantic relation normalization so that values are not guessed from partial converter output.
