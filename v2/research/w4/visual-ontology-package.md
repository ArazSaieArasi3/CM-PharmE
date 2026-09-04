# CM-PharmE 2.0 Visual Ontology Package

Status: V2 human-review artifact.  
Scope: 17 canonical domains.  
Source: Gate-D 87-element conceptual model plus the approved V2 concept-label normalization.  
Boundary: visual review aid only; stable V2 IRIs and formal semantics remain unchanged.

## Rendering convention
These review diagrams intentionally use Mermaid `flowchart` rather than `classDiagram`.
Each concept is shown as one simple box containing only the OntoUML stereotype and the human-facing concept name. No attribute or operation compartments are displayed, and no HTML tags are used in labels.

## 1. Ecosystem Organization
```mermaid
flowchart TB
ORG["«Kind»
Organization"]
EP["«RoleMixin»
Ecosystem Participant"]
RA["«Role»
Regulatory Authority"]
MFR["«Role»
Manufacturer"]
IMP["«Role»
Importer"]
PRO["«Role»
Product Responsible Organization"]
WDD["«Role»
Wholesale Distributor"]
TPL["«Role»
Third-Party Logistics Provider"]
RA -->|specializes| ORG
MFR -->|specializes| ORG
IMP -->|specializes| ORG
PRO -->|specializes| ORG
WDD -->|specializes| ORG
TPL -->|specializes| ORG
RA -->|specializes| EP
MFR -->|specializes| EP
IMP -->|specializes| EP
PRO -->|specializes| EP
WDD -->|specializes| EP
TPL -->|specializes| EP
```

## 2. Facility Operations
```mermaid
flowchart TB
FAC["«Kind»
Facility"]
MS["«Role»
Manufacturing Site"]
DS["«Role»
Distribution Site"]
FO["«Relator»
Facility Operation"]
ORG["«Kind»
Organization"]
MS -->|specializes| FAC
DS -->|specializes| FAC
FO -->|mediates| ORG
FO -->|mediates| FAC
```

## 3. Regulatory Governance
```mermaid
flowchart TB
ER["«Relator»
Establishment Registration"]
AUTH["«Relator»
Regulatory Authorization"]
JUR["«Kind»
Regulatory Jurisdiction"]
RA["«Role»
Regulatory Authority"]
FAC["«Kind»
Facility"]
EP["«RoleMixin»
Ecosystem Participant"]
ER -->|mediates| RA
ER -->|mediates| FAC
ER -->|applies in| JUR
AUTH -->|mediates| RA
AUTH -->|mediates| EP
AUTH -->|applies in| JUR
```

## 4. Pharmaceutical Product
```mermaid
flowchart TB
MP["«Kind»
Medicinal Product"]
SUB["«Kind»
Pharmaceutical Substance"]
PRES["«Kind»
Medicinal Product Presentation"]
DFS["«Kind»
Dosage Form Specification"]
STR["«Quality»
Strength"]
PKG["«Kind»
Package Configuration"]
PCS["«Kind»
Product Classification Scheme"]
CE["«Kind»
Classification Entry"]
PCA["«Relator»
Product Classification Assignment"]
ML["«Relator»
Market Listing"]
PRES -->|presentation of| MP
PRES -->|active substance| SUB
PRES -->|dosage form| DFS
PRES -->|characterized by| STR
PRES -->|package| PKG
PCA -->|mediates| MP
PCA -->|mediates| CE
CE -->|in scheme| PCS
ML -->|mediates| PRES
```

## 5. Supply Operations
```mermaid
flowchart TB
MA["«Event»
Manufacturing Activity"]
PLA["«Event»
Pharmaceutical Logistics Activity"]
MSS["«Situation»
Medicine Shortage Situation"]
SC["«Mode»
Supply Capacity"]
ORG["«Kind»
Organization"]
FAC["«Kind»
Facility"]
PRES["«Kind»
Medicinal Product Presentation"]
JUR["«Kind»
Regulatory Jurisdiction"]
ORG -->|participates| MA
FAC -->|participates| MA
PRES -->|concerns| MA
ORG -->|participates| PLA
FAC -->|participates| PLA
MSS -->|involves| PRES
MSS -->|context| JUR
ORG -->|characterized by| SC
FAC -->|characterized by| SC
```

## 6. Ecosystem Observation
```mermaid
flowchart TB
OR["«Kind»
Observation Result"]
AOR["«Subkind»
Availability Observation Result"]
DOR["«Subkind»
Demand Observation Result"]
SCOR["«Subkind»
Supply Capacity Observation Result"]
AOR -->|specializes| OR
DOR -->|specializes| OR
SCOR -->|specializes| OR
```

## 7. Spatiotemporal Context
```mermaid
flowchart TB
GF["«Kind»
Geographic Feature"]
AR["«Subkind»
Administrative Region"]
CTRY["«Subkind»
Country"]
GP["«Datatype»
Geospatial Position"]
ADDR["«Datatype»
Address"]
TI["«Datatype»
Time Interval"]
RP["«Datatype»
Reporting Period"]
AR -->|specializes| GF
CTRY -->|specializes| GF
GF -->|position| GP
GF -->|address| ADDR
```

## 8. Evidence Traceability
```mermaid
flowchart TB
DSR["«Kind»
Data Source"]
DS["«Kind»
Dataset"]
DR["«Kind»
Dataset Release"]
SR["«Kind»
Source Record"]
AS["«Kind»
Assertion"]
OA["«Event»
Observation Activity"]
OR["«Kind»
Observation Result"]
MV["«Datatype»
Measure Value"]
EI["«RoleMixin»
Evidence Item"]
ES["«Relator»
Evidence Support"]
MAP["«Subkind»
Mapping Assertion"]
PA["«Event»
Provenance Activity"]
DQ["«Subkind»
Data Quality Finding"]
MAP -->|specializes| AS
DQ -->|specializes| AS
DSR -->|maintains| DS
DS -->|has release| DR
DR -->|contains| SR
OA -->|produces| OR
OR -->|has value| MV
ES -->|mediates| EI
ES -->|mediates| AS
PA -->|uses| SR
PA -->|generates| AS
```

## 9. Entity Identity
```mermaid
flowchart TB
IV["«Datatype»
Identifier Value"]
IS["«Kind»
Identifier Scheme"]
IA["«Relator»
Identifier Assignment"]
AS["«Kind»
Assertion"]
EMA["«Subkind»
Entity Match Assertion"]
MC["«Quality»
Match Confidence"]
EMA -->|specializes| AS
IA -->|mediates| IV
IA -->|mediates| IS
EMA -->|characterized by| MC
```

## 10. Regulatory Policy
```mermaid
flowchart TB
RR["«Kind»
Regulatory Requirement"]
RO["«Relator»
Regulatory Oversight"]
RA["«Role»
Regulatory Authority"]
ORG["«Kind»
Organization"]
RO -->|mediates| RA
RO -->|supervises| ORG
RO -->|governed by| RR
```

## 11. Supply Resilience
```mermaid
flowchart TB
CMCA["«Relator»
Contextual Medicine Classification Assignment"]
EMCA["«Subkind»
Essential Medicine Classification Assignment"]
CRCA["«Subkind»
Critical Medicine Classification Assignment"]
AMP["«Role»
Alternative Medicinal Product"]
AMPA["«Relator»
Alternative Medicinal Product Assignment"]
SD["«Relator»
Supply Dependency"]
DE["«Event»
Disruption Event"]
IOR["«Subkind»
Inventory Observation Result"]
PA["«Event»
Procurement Activity"]
LTOR["«Subkind»
Lead Time Observation Result"]
SS["«Situation»
Stockout Situation"]
MP["«Kind»
Medicinal Product"]
OR["«Kind»
Observation Result"]
EMCA -->|specializes| CMCA
CRCA -->|specializes| CMCA
AMP -->|specializes| MP
AMPA -->|subject| MP
AMPA -->|alternative| AMP
IOR -->|specializes| OR
LTOR -->|specializes| OR
SD -->|exposed to| DE
IOR -->|evidences| SS
```

## 12. Market Access
```mermaid
flowchart TB
ORG["«Kind»
Organization"]
HFO["«Role»
Healthcare Financing Organization"]
OR["«Kind»
Observation Result"]
RUOR["«Subkind»
Reimbursement and Utilization Observation Result"]
DCR["«Kind»
Diagnosis Classification Reference"]
HFO -->|specializes| ORG
RUOR -->|specializes| OR
RUOR -->|contextualized by| DCR
```

## 13. Risk Management
```mermaid
flowchart TB
AAR["«RoleMixin»
Asset at Risk"]
RAA["«Event»
Risk Assessment Activity"]
VUL["«Mode»
Vulnerability"]
RTP["«Kind»
Risk Treatment Plan"]
RTA["«Event»
Risk Treatment Activity"]
AAR -->|characterized by| VUL
RAA -->|assesses| AAR
RAA -->|identifies| VUL
RTP -->|addresses| VUL
RTP -->|realized through| RTA
```

## 14. Pharmacovigilance
```mermaid
flowchart TB
PVR["«Kind»
Pharmacovigilance Requirement"]
AERA["«Event»
Adverse Event Reporting Activity"]
PMSA["«Event»
Post-Market Surveillance Activity"]
AERA -->|governed by| PVR
PMSA -->|governed by| PVR
```

## 15. Business Architecture
```mermaid
flowchart TB
BAV["«Kind»
Business Architecture View"]
EC["«Mode»
Enterprise Capability"]
SPA["«Relator»
Strategic Partnership Agreement"]
SOS["«Kind»
Service Offering Specification"]
ORG["«Kind»
Organization"]
ORG -->|characterized by| EC
SPA -->|mediates| ORG
BAV -->|represents| ORG
BAV -->|represents| EC
BAV -->|represents| SOS
```

## 16. Digital Systems
```mermaid
flowchart TB
DSC["«Kind»
Digital System Component"]
ORG["«Kind»
Organization"]
FAC["«Kind»
Facility"]
DSC -->|supports| ORG
DSC -->|supports| FAC
```

## 17. Clinical Care
```mermaid
flowchart TB
CCP["«RoleMixin»
Clinical Care Participant"]
```

## Review guidance
These diagrams are optimized for human conceptual review rather than exhaustive OWL inspection. Cross-domain relations are repeated only where they clarify the domain. Formal truth remains in the V2 OntoUML specification and OWL/SHACL artifacts. Any diagram-driven semantic change must be recorded as a separate V2 design decision before formalization is changed.
