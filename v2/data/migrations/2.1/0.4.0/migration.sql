-- Experimental M3-only addition in a disposable W6 database.
-- Existing base tables, views, defaults and exporter are unchanged.
CREATE TABLE cmpe.manufacturing_responsibility_21 (
  public_id TEXT PRIMARY KEY,
  organization_id BIGINT NOT NULL REFERENCES cmpe.organization(organization_id),
  medicinal_product_id BIGINT NOT NULL REFERENCES cmpe.medicinal_product(medicinal_product_id),
  source_record_id BIGINT NOT NULL REFERENCES cmpe.source_record(source_record_id),
  assertion_id BIGINT NOT NULL REFERENCES cmpe.assertion(assertion_id),
  evidence_support_id BIGINT NOT NULL REFERENCES cmpe.evidence_support(evidence_support_id),
  claim_kind TEXT NOT NULL CHECK (claim_kind IN ('documentary_attribution','synthetic_fixture')),
  valid_from DATE,
  valid_to DATE,
  UNIQUE(source_record_id, assertion_id),
  CHECK (valid_from IS NULL OR valid_to IS NULL OR valid_to >= valid_from)
);

CREATE FUNCTION cmpe.check_manufacturing_responsibility_21() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM cmpe.evidence_support es
    JOIN cmpe.assertion a ON a.assertion_id=es.assertion_id
    JOIN cmpe.organization o ON o.organization_id=NEW.organization_id
    JOIN cmpe.medicinal_product p ON p.medicinal_product_id=NEW.medicinal_product_id
    WHERE es.evidence_support_id=NEW.evidence_support_id
      AND es.source_record_id=NEW.source_record_id
      AND es.assertion_id=NEW.assertion_id
      AND a.subject_public_id=o.public_id AND a.object_public_id=p.public_id
      AND a.predicate_key='documented_manufacturer'
      AND a.assertion_type=NEW.claim_kind
  ) THEN
    RAISE EXCEPTION 'M3 source/assertion/evidence/participant mismatch' USING ERRCODE='23514';
  END IF;
  RETURN NEW;
END;
$$;

-- AFTER allows immediate NOT NULL/FK constraints to retain their standard errors.
CREATE TRIGGER manufacturing_responsibility_21_evidence_guard
AFTER INSERT OR UPDATE ON cmpe.manufacturing_responsibility_21
FOR EACH ROW EXECUTE FUNCTION cmpe.check_manufacturing_responsibility_21();
