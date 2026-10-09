PRAGMA foreign_keys=ON;
CREATE TABLE role_profile (
 role TEXT PRIMARY KEY, bearer_kind TEXT NOT NULL, scope TEXT UNIQUE NOT NULL,
 counterpart_kind TEXT NOT NULL, responsibility_type TEXT NOT NULL, event_type TEXT NOT NULL
);
CREATE TABLE entity (
 id TEXT PRIMARY KEY, kind TEXT NOT NULL CHECK(kind IN ('Organization','Facility','MedicinalProduct'))
);
CREATE TABLE evidence (
 id TEXT PRIMARY KEY,
 kind TEXT NOT NULL CHECK(kind IN ('authorization_decision','responsibility_instrument','occurrence_record','registration_record','operation_record'))
);
CREATE TABLE context (
 id TEXT PRIMARY KEY, episode_key TEXT NOT NULL,
 facet TEXT NOT NULL CHECK(facet IN ('authorization','responsibility','activity','registration','operation')),
 role TEXT NOT NULL REFERENCES role_profile(role), scope TEXT NOT NULL,
 holder TEXT NOT NULL REFERENCES entity(id), counterpart TEXT REFERENCES entity(id),
 jurisdiction TEXT NOT NULL CHECK(length(trim(jurisdiction))>0),
 start_day INTEGER NOT NULL CHECK(typeof(start_day)='integer'),
 end_day INTEGER CHECK(end_day IS NULL OR (typeof(end_day)='integer' AND end_day>start_day)),
 evidence_id TEXT NOT NULL REFERENCES evidence(id),
 UNIQUE(facet,episode_key),
 CHECK(counterpart IS NULL OR counterpart<>holder),
 CHECK(facet='activity' OR counterpart IS NOT NULL),
 CHECK(facet<>'activity' OR end_day IS NOT NULL)
);
CREATE TRIGGER context_types BEFORE INSERT ON context BEGIN
 SELECT CASE WHEN (SELECT kind FROM entity WHERE id=NEW.holder)<>
   (SELECT bearer_kind FROM role_profile WHERE role=NEW.role)
   THEN RAISE(ABORT,'wrong bearer identity') END;
 SELECT CASE WHEN NEW.facet='authorization' AND
   (SELECT kind FROM entity WHERE id=NEW.counterpart)<>'Organization'
   THEN RAISE(ABORT,'authority must be Organization') END;
 SELECT CASE WHEN NEW.facet='responsibility' AND
   (SELECT kind FROM entity WHERE id=NEW.counterpart)<>
   (SELECT counterpart_kind FROM role_profile WHERE role=NEW.role)
   THEN RAISE(ABORT,'wrong responsibility counterpart') END;
 SELECT CASE WHEN (SELECT kind FROM evidence WHERE id=NEW.evidence_id)<>
   CASE NEW.facet WHEN 'authorization' THEN 'authorization_decision'
   WHEN 'responsibility' THEN 'responsibility_instrument'
   WHEN 'activity' THEN 'occurrence_record' WHEN 'registration' THEN 'registration_record'
   WHEN 'operation' THEN 'operation_record' END
   THEN RAISE(ABORT,'evidence kind cannot support facet') END;
END;
-- Append-only lab records: corrected/renewed episodes are reloaded as new input.
CREATE TRIGGER no_context_update BEFORE UPDATE ON context BEGIN
 SELECT RAISE(ABORT,'append-only lab; rebuild corrected fixture');
END;
