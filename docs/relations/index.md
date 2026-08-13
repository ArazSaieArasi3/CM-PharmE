# CM-PharmE Relations

The v1.0 diagram contains **41 labeled semantic relation occurrences**. The canonical registry contains **40 relations** after collapsing one exact duplicate caused by the duplicated `Enterprise Governance Relator` node. One unlabeled self-loop graphical artifact is excluded.

Relation stereotype counts in the canonical registry: **19 material**, **8 mediation**, **6 characterization**, **4 componentOf**, **2 association**, and **1 generalization**.

| ID | Label | Type | Source | Target | Review |
|---|---|---|---|---|---|
| `CMPE-R0001` | governs | material | `CMPE-C0001` | `CMPE-C0003` | — |
| `CMPE-R0002` | is mediated by | mediation | `CMPE-C0003` | `CMPE-C0025` | exact duplicate collapsed |
| `CMPE-R0003` | is part of | componentOf | `CMPE-C0002` | `CMPE-C0001` | — |
| `CMPE-R0004` | characterizes | characterization | `CMPE-C0005` | `CMPE-C0001` | — |
| `CMPE-R0005` | characterizes | characterization | `CMPE-C0006` | `CMPE-C0002` | — |
| `CMPE-R0006` | specializes | generalization | `CMPE-C0007` | `CMPE-C0003` | — |
| `CMPE-R0007` | is mediated by | mediation | `CMPE-C0008` | `CMPE-C0009` | — |
| `CMPE-R0008` | fulfills | material | `CMPE-C0039` | `CMPE-C0010` | — |
| `CMPE-R0009` | characterizes | characterization | `CMPE-C0008` | `CMPE-C0011` | — |
| `CMPE-R0010` | is part of | componentOf | `CMPE-C0012` | `CMPE-C0013` | source label: is part of a |
| `CMPE-R0011` | mediates | mediation | `CMPE-C0008` | `CMPE-C0014` | direction semantics review |
| `CMPE-R0012` | participates in | association | `CMPE-C0015` | `CMPE-C0003` | — |
| `CMPE-R0013` | is part of | componentOf | `CMPE-C0016` | `CMPE-C0015` | — |
| `CMPE-R0014` | is mediated by | mediation | `CMPE-C0017` | `CMPE-C0018` | — |
| `CMPE-R0015` | is mediated by | mediation | `CMPE-C0019` | `CMPE-C0018` | — |
| `CMPE-R0016` | assigns | material | `CMPE-C0020` | `CMPE-C0021` | — |
| `CMPE-R0017` | participates in | association | `CMPE-C0022` | `CMPE-C0021` | — |
| `CMPE-R0018` | material relation | material | `CMPE-C0023` | `CMPE-C0024` | — |
| `CMPE-R0019` | is mediated by | mediation | `CMPE-C0024` | `CMPE-C0004` | — |
| `CMPE-R0020` | characterizes | characterization | `CMPE-C0026` | `CMPE-C0004` | — |
| `CMPE-R0021` | characterizes | characterization | `CMPE-C0027` | `CMPE-C0026` | — |
| `CMPE-R0022` | mitigates | material | `CMPE-C0028` | `CMPE-C0027` | — |
| `CMPE-R0023` | enables | material | `CMPE-C0029` | `CMPE-C0015` | — |
| `CMPE-R0024` | mediates | mediation | `CMPE-C0032` | `CMPE-C0031` | — |
| `CMPE-R0025` | records | material | `CMPE-C0033` | `CMPE-C0034` | — |
| `CMPE-R0026` | enables | material | `CMPE-C0035` | `CMPE-C0018` | — |
| `CMPE-R0027` | is mediated by | mediation | `CMPE-C0008` | `CMPE-C0014` | direction semantics review |
| `CMPE-R0028` | governs | material | `CMPE-C0032` | `CMPE-C0001` | — |
| `CMPE-R0029` | is part of | componentOf | `CMPE-C0018` | `CMPE-C0015` | — |
| `CMPE-R0030` | characterizes | characterization | `CMPE-C0034` | `CMPE-C0018` | — |
| `CMPE-R0031` | constraints | material | `CMPE-C0036` | `CMPE-C0037` | wording review recommended |
| `CMPE-R0032` | informs | material | `CMPE-C0038` | `CMPE-C0036` | — |
| `CMPE-R0033` | informs | material | `CMPE-C0038` | `CMPE-C0001` | — |
| `CMPE-R0034` | informs | material | `CMPE-C0038` | `CMPE-C0028` | — |
| `CMPE-R0035` | follows | material | `CMPE-C0037` | `CMPE-C0022` | — |
| `CMPE-R0036` | governs | material | `CMPE-C0009` | `CMPE-C0013` | — |
| `CMPE-R0037` | records | material | `CMPE-C0033` | `CMPE-C0017` | — |
| `CMPE-R0038` | assists | material | `CMPE-C0030` | `CMPE-C0016` | — |
| `CMPE-R0039` | material relation | material | `CMPE-C0009` | `CMPE-C0039` | generic label review recommended |
| `CMPE-R0040` | engages in | material | `CMPE-C0001` | `CMPE-C0014` | — |

Each relation has its own page under this directory. Cardinalities remain authoritative in the source diagram; a dedicated cardinality transcription/validation pass is intentionally separated from this semantic relation normalization so that values are not guessed from partial converter output.
