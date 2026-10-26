-- Disposable copied-W6 prototype: intrinsic Mode and measurement stay separate.
CREATE TABLE cmpe.supply_capacity_21 (
  public_id TEXT PRIMARY KEY,
  projection_version TEXT NOT NULL DEFAULT '0.5.0' CHECK (projection_version='0.5.0'),
  organization_id BIGINT REFERENCES cmpe.organization(organization_id),
  facility_id BIGINT REFERENCES cmpe.facility(facility_id),
  claim_kind TEXT NOT NULL CHECK (claim_kind IN ('synthetic_fixture','documentary_attribution')),
  source_record_id BIGINT REFERENCES cmpe.source_record(source_record_id),
  assertion_id BIGINT REFERENCES cmpe.assertion(assertion_id),
  evidence_support_id BIGINT REFERENCES cmpe.evidence_support(evidence_support_id),
  CHECK (num_nonnulls(organization_id, facility_id)=1),
  CHECK (num_nonnulls(source_record_id, assertion_id, evidence_support_id) IN (0,3))
);

CREATE FUNCTION cmpe.check_supply_capacity_21() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM cmpe.observation_result WHERE public_id=NEW.public_id) THEN
    RAISE EXCEPTION 'Observation public ID cannot identify the capacity Mode' USING ERRCODE='23514';
  END IF;
  IF NEW.source_record_id IS NOT NULL AND NOT EXISTS (
    SELECT 1 FROM cmpe.evidence_support es
    JOIN cmpe.assertion a ON a.assertion_id=es.assertion_id
    LEFT JOIN cmpe.organization o ON o.organization_id=NEW.organization_id
    LEFT JOIN cmpe.facility f ON f.facility_id=NEW.facility_id
    WHERE es.evidence_support_id=NEW.evidence_support_id
      AND es.source_record_id=NEW.source_record_id AND es.assertion_id=NEW.assertion_id
      AND a.assertion_type=NEW.claim_kind
      AND a.object_public_id=NEW.public_id
      AND a.subject_public_id=COALESCE(o.public_id,f.public_id)
      AND a.predicate_key=CASE WHEN NEW.organization_id IS NOT NULL
                           THEN 'organizationHasSupplyCapacity' ELSE 'facilityHasSupplyCapacity' END
  ) THEN
    RAISE EXCEPTION 'M4 source/assertion/evidence/bearer mismatch' USING ERRCODE='23514';
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER supply_capacity_21_guard
AFTER INSERT OR UPDATE ON cmpe.supply_capacity_21
FOR EACH ROW EXECUTE FUNCTION cmpe.check_supply_capacity_21();
