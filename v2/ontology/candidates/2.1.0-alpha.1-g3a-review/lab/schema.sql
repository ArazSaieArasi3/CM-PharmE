PRAGMA foreign_keys=ON;
CREATE TABLE entity(id TEXT PRIMARY KEY, identity_kind TEXT NOT NULL);
CREATE TABLE source(id TEXT PRIMARY KEY, description TEXT NOT NULL);
CREATE TABLE context(id TEXT PRIMARY KEY, jurisdiction TEXT NOT NULL, scheme_version TEXT NOT NULL);
CREATE TABLE relator(id TEXT PRIMARY KEY, type TEXT NOT NULL, context_id TEXT REFERENCES context(id), source_id TEXT REFERENCES source(id), valid_from TEXT, valid_to TEXT, lexical_value TEXT);
CREATE TABLE participation(relator_id TEXT REFERENCES relator(id), slot TEXT NOT NULL, entity_id TEXT REFERENCES entity(id), PRIMARY KEY(relator_id,slot,entity_id));
CREATE TABLE alias(relator_id TEXT REFERENCES relator(id), property TEXT NOT NULL, entity_id TEXT REFERENCES entity(id), PRIMARY KEY(relator_id,property,entity_id));
CREATE TABLE containment(child TEXT REFERENCES entity(id), parent TEXT REFERENCES entity(id), PRIMARY KEY(child,parent));
CREATE TABLE explicit_role(entity_id TEXT REFERENCES entity(id), role TEXT NOT NULL);
CREATE TABLE slot_rule(profile TEXT, slot TEXT, property TEXT, target TEXT, minimum INTEGER, maximum INTEGER, PRIMARY KEY(profile,slot));
CREATE TABLE allowed_kind(profile TEXT, slot TEXT, identity_kind TEXT, role TEXT, PRIMARY KEY(profile,slot,identity_kind));
CREATE VIEW derived_role AS SELECT DISTINCT p.entity_id,a.role,r.context_id,r.valid_from,r.valid_to
 FROM participation p JOIN relator r ON r.id=p.relator_id JOIN entity e ON e.id=p.entity_id
 JOIN allowed_kind a ON a.profile=r.type AND a.slot=p.slot AND a.identity_kind=e.identity_kind;
-- Tables are staging-capable. validate_sql is the mandatory admission gate.
-- Null provenance is retained for review, but may not pass as a complete relator.
