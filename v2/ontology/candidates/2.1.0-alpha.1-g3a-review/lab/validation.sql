-- CARDINALITY
SELECT r.id,s.slot FROM relator r JOIN slot_rule s ON s.profile=r.type LEFT JOIN participation p ON p.relator_id=r.id AND p.slot=s.slot GROUP BY r.id,s.slot HAVING count(p.entity_id)<s.minimum OR (s.maximum IS NOT NULL AND count(p.entity_id)>s.maximum);

-- KIND
SELECT p.relator_id,p.slot FROM participation p JOIN relator r ON r.id=p.relator_id JOIN entity e ON e.id=p.entity_id LEFT JOIN allowed_kind a ON a.profile=r.type AND a.slot=p.slot AND a.identity_kind=e.identity_kind WHERE a.role IS NULL;

-- DISTINCT
SELECT relator_id,entity_id FROM participation GROUP BY relator_id,entity_id HAVING count(DISTINCT slot)>1;

-- PROVENANCE
SELECT id FROM relator WHERE source_id IS NULL OR context_id IS NULL;

-- TIME
SELECT id FROM relator WHERE valid_from IS NULL OR valid_to IS NULL OR valid_from>=valid_to;

-- LEXICAL
SELECT id FROM relator WHERE type='IdentifierAssignment' AND (lexical_value IS NULL OR lexical_value='');

-- DEFERRED
SELECT id FROM entity WHERE identity_kind IN ('AssetAtRisk','Vulnerability','ClinicalCareParticipant');

-- CYCLE
WITH RECURSIVE reach(child,parent) AS (SELECT child,parent FROM containment UNION SELECT r.child,c.parent FROM reach r JOIN containment c ON r.parent=c.child) SELECT child FROM reach WHERE child=parent;

-- ALIAS
SELECT a.relator_id FROM alias a LEFT JOIN participation p ON p.relator_id=a.relator_id AND p.entity_id=a.entity_id AND p.slot=CASE a.property WHEN 'evidenceRecord' THEN 'evidence' WHEN 'contextClassificationProduct' THEN 'subject' WHEN 'contextClassificationEntry' THEN 'entry' END WHERE p.entity_id IS NULL;

-- GROUNDING
SELECT e.entity_id,e.role FROM explicit_role e WHERE NOT EXISTS (SELECT 1 FROM derived_role d WHERE d.entity_id=e.entity_id AND d.role=e.role);