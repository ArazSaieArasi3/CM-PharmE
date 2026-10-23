PRAGMA foreign_keys=ON;
CREATE TABLE entity(id TEXT PRIMARY KEY, kind TEXT NOT NULL
 CHECK(kind IN ('Organization','Facility','MedicinalProduct','MedicinalProductPresentation')));
CREATE TABLE evidence(id TEXT PRIMARY KEY,kind TEXT NOT NULL);
CREATE TABLE profile(id TEXT PRIMARY KEY,role TEXT NOT NULL,counterpart_kind TEXT NOT NULL,
 evidence_kind TEXT NOT NULL,scope TEXT NOT NULL);
CREATE TABLE episode(
 id TEXT PRIMARY KEY, episode_key TEXT NOT NULL, profile TEXT NOT NULL REFERENCES profile(id),
 holder TEXT NOT NULL REFERENCES entity(id), counterpart TEXT NOT NULL REFERENCES entity(id),
 evidence TEXT NOT NULL REFERENCES evidence(id),
 scope TEXT NOT NULL, jurisdiction TEXT NOT NULL CHECK(length(trim(jurisdiction))>0),
 start_day INTEGER NOT NULL CHECK(typeof(start_day)='integer'),
 end_day INTEGER CHECK(end_day IS NULL OR (typeof(end_day)='integer' AND end_day>start_day)),
 UNIQUE(profile,episode_key), CHECK(holder<>counterpart));
CREATE TRIGGER validate_episode BEFORE INSERT ON episode BEGIN
 SELECT CASE WHEN (SELECT kind FROM entity WHERE id=NEW.holder)<>'Organization'
 THEN RAISE(ABORT,'holder_identity') END;
 SELECT CASE WHEN (SELECT kind FROM entity WHERE id=NEW.counterpart)<>
 (SELECT counterpart_kind FROM profile WHERE id=NEW.profile)
 THEN RAISE(ABORT,'counterpart_identity') END;
 SELECT CASE WHEN (SELECT kind FROM evidence WHERE id=NEW.evidence)<>
 (SELECT evidence_kind FROM profile WHERE id=NEW.profile)
 THEN RAISE(ABORT,'evidence_boundary') END;
END;
CREATE TRIGGER no_episode_update BEFORE UPDATE ON episode BEGIN
 SELECT RAISE(ABORT,'append_only_lab'); END;
-- These claims are evidence records, not institutional-role or entitlement assertions.
CREATE TABLE observed_claim(id TEXT PRIMARY KEY,holder TEXT NOT NULL REFERENCES entity(id),
 kind TEXT NOT NULL CHECK(kind IN ('authorization_issued','payment_observed','aggregate_published','label_string','manufacturing_observed')));
