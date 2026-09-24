# Data and Database Guide

> **Page scope:** V2 / Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Last synchronized:** 2026-09-24  
> **Related issues/PRs:** #228, #230  
> **Wiki baseline:** WB-2026.09.1

Use this section to understand the **data sources, provenance model, relational realization and database-related evidence** behind CM-PharmE 2.0.

## Data landscape and provenance
- [[V2 Dataset Landscape and Provenance]]
- [[V1 to V2 Evidence and Provenance]]
- [[Dataset and Source Index]]

## Reference data infrastructure
- [[V2 Data Infrastructure]]

The current implementation uses PostgreSQL/PostGIS and preserves mappings between ontology concepts, relational structures, evidence/provenance records and RDF/KG generation. A deeper table catalog and ERD package is planned under #236.

## Related references
- [[Repository Artifact Index]]
- [[Knowledge Graph and Queries Guide]]

### Suggested path for a data engineer
**V2 Dataset Landscape and Provenance → V2 Data Infrastructure → Dataset and Source Index → Knowledge Graph and Queries Guide**
