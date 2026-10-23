BEGIN TRANSACTION;
CREATE TABLE entity(id TEXT PRIMARY KEY, kind TEXT NOT NULL
 CHECK(kind IN ('Organization','Facility','MedicinalProduct','MedicinalProductPresentation')));
INSERT INTO "entity" VALUES('org','Organization');
INSERT INTO "entity" VALUES('org2','Organization');
INSERT INTO "entity" VALUES('org3','Organization');
INSERT INTO "entity" VALUES('site','Facility');
INSERT INTO "entity" VALUES('product','MedicinalProduct');
INSERT INTO "entity" VALUES('presentation','MedicinalProductPresentation');
CREATE TABLE episode(
 id TEXT PRIMARY KEY, episode_key TEXT NOT NULL, profile TEXT NOT NULL REFERENCES profile(id),
 holder TEXT NOT NULL REFERENCES entity(id), counterpart TEXT NOT NULL REFERENCES entity(id),
 evidence TEXT NOT NULL REFERENCES evidence(id),
 scope TEXT NOT NULL, jurisdiction TEXT NOT NULL CHECK(length(trim(jurisdiction))>0),
 start_day INTEGER NOT NULL CHECK(typeof(start_day)='integer'),
 end_day INTEGER CHECK(end_day IS NULL OR (typeof(end_day)='integer' AND end_day>start_day)),
 UNIQUE(profile,episode_key), CHECK(holder<>counterpart));
INSERT INTO "episode" VALUES('mandate','mandate','mandate','org','org2','mandate','regulatory_mandate','LAB',10,30);
INSERT INTO "episode" VALUES('label_responsibility','label_responsibility','label_responsibility','org','product','label_responsibility','product_label_responsibility','LAB',10,30);
INSERT INTO "episode" VALUES('funding','funding','funding','org','org2','funding','institutional_funding','LAB',10,30);
CREATE TABLE evidence(id TEXT PRIMARY KEY,kind TEXT NOT NULL);
INSERT INTO "evidence" VALUES('mandate','mandate_instrument');
INSERT INTO "evidence" VALUES('label_responsibility','responsibility_instrument');
INSERT INTO "evidence" VALUES('listing','listing_responsibility_evidence');
INSERT INTO "evidence" VALUES('funding','funding_instrument');
INSERT INTO "evidence" VALUES('aggregate','aggregate_observation');
INSERT INTO "evidence" VALUES('generic','source_label');
CREATE TABLE observed_claim(id TEXT PRIMARY KEY,holder TEXT NOT NULL REFERENCES entity(id),
 kind TEXT NOT NULL CHECK(kind IN ('authorization_issued','payment_observed','aggregate_published','label_string','manufacturing_observed')));
CREATE TABLE profile(id TEXT PRIMARY KEY,role TEXT NOT NULL,counterpart_kind TEXT NOT NULL,
 evidence_kind TEXT NOT NULL,scope TEXT NOT NULL);
INSERT INTO "profile" VALUES('mandate','RegulatoryAuthorityRole','Organization','mandate_instrument','regulatory_mandate');
INSERT INTO "profile" VALUES('label_responsibility','ProductResponsibleLabelerRole','MedicinalProduct','responsibility_instrument','product_label_responsibility');
INSERT INTO "profile" VALUES('listing','ProductResponsibleLabelerRole','MedicinalProductPresentation','listing_responsibility_evidence','market_listing');
INSERT INTO "profile" VALUES('funding','PayerFundingOrganizationRole','Organization','funding_instrument','institutional_funding');
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
COMMIT;
