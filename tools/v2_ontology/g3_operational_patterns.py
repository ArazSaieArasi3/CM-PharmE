#!/usr/bin/env python3
"""Executable, closed-world G3-1b design lab. Does not change the active ontology."""
import copy
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'v2/research/w4/g3-1b-operational-patterns'
BASE = ROOT / 'v2/ontology/candidates/2.1.0-alpha.1-g3a-review'
ROWS = [
 ('ManufacturerRole','Organization','manufacturing','MedicinalProduct','ManufacturingResponsibility','ManufacturingActivity','V2C-004; V2R-024/025'),
 ('ManufacturingSiteRole','Facility','manufacturing_site','Organization','ManufacturingSiteUse','ManufacturingActivity','V2C-011; V2R-003/024'),
 ('ImporterRole','Organization','import','MedicinalProduct','ImportResponsibility','ImportActivity (proposed; not active)','V2C-005; V2R-008'),
 ('WholesaleDistributorRole','Organization','wholesale','MedicinalProduct','WholesaleResponsibility','DistributionLogisticsActivity with wholesale scope','V2C-007; V2R-026'),
 ('ThirdPartyLogisticsProviderRole','Organization','third_party_logistics','Organization','LogisticsServiceCommitment','DistributionLogisticsActivity with 3PL scope','V2C-008; V2R-026'),
 ('DistributionSiteRole','Facility','distribution_site','Organization','DistributionSiteUse','DistributionLogisticsActivity','V2C-012; V2R-004/026'),
]

SCHEMA = '''PRAGMA foreign_keys=ON;
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
'''

QUERY = '''SELECT DISTINCT c.facet FROM context c JOIN role_profile r ON r.role=c.role
WHERE c.role=:role AND c.holder=:holder AND c.scope=r.scope
 AND c.jurisdiction=:jurisdiction AND c.start_day<=:day
 AND (c.end_day IS NULL OR :day<c.end_day)
 AND c.facet IN ('authorization','responsibility','activity') ORDER BY c.facet;'''

def write(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def db():
    c=sqlite3.connect(':memory:');c.executescript(SCHEMA)
    c.executemany('INSERT INTO role_profile VALUES (?,?,?,?,?,?)',[r[:6] for r in ROWS])
    c.executemany('INSERT INTO entity VALUES (?,?)', [('org','Organization'),('org2','Organization'),('org3','Organization'),('site','Facility'),('site2','Facility'),('product','MedicinalProduct')])
    c.executemany('INSERT INTO evidence VALUES (?,?)', [('auth','authorization_decision'),('resp','responsibility_instrument'),('event','occurrence_record'),('reg','registration_record'),('op','operation_record')])
    return c

def record(row, facet, **kw):
    role,kind,scope,other,*_=row
    holder='site' if kind=='Facility' else 'org'
    counterpart=None if facet=='activity' else ('product' if facet=='responsibility' and other=='MedicinalProduct' else 'org2')
    out=dict(id=facet,episode_key=facet,facet=facet,role=role,scope=scope,holder=holder,counterpart=counterpart,jurisdiction='LAB',start_day=10,end_day=30,evidence_id={'authorization':'auth','responsibility':'resp','activity':'event','registration':'reg','operation':'op'}[facet])
    out.update(kw);return out

def insert(c,r):
    c.execute('INSERT INTO context ('+','.join(r)+') VALUES ('+','.join('?' for _ in r)+')',list(r.values()))

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.iterdir() if p.is_file()}
    register=[]
    for role,kind,scope,other,relator,event,anchor in ROWS:
        counterpart_role = ('CommissioningLogisticsClientRole' if scope=='third_party_logistics' else
                            ('Assigning'+relator+'OrganizationRole' if kind=='Facility' else relator+'SubjectRole'))
        register.append(dict(role=role,identity_provider=kind,scope=scope,evidence_anchors=[anchor,'W4 R3/R4','W4 events-situations-observations.md'],
          authorization=dict(reuse='RegulatoryAuthorization',target_parent='Authorized'+kind+'Role',definition='Authorized bearer with an explicit matching activity/use scope, jurisdiction and effective interval.',implies_responsibility=False,implies_occurrence=False),
          responsibility=dict(proposed_relator=relator,stereotype='Relator',bearer_role=role,counterpart_role=counterpart_role,counterpart_identity=other,
            mediations=[dict(target=role,per_relator='1',relators_per_current_role='1..*'),dict(target=counterpart_role,per_relator='1',relators_per_current_role='1..*')],
            distinct_individuals=2,role_definition='Bearer participates in at least one effective, scope-matching responsibility/site-use context at t.',
            profile_boundary='One responsibility assignment per bearer-counterpart-scope episode; multi-party source instruments decompose into linked assignments only when independently evidenced.',
            role_loss='When the last effective matching responsibility episode ends; bearer identity survives.',
            relator_identity='Independent constituting responsibility episode, not the evidence row ID or only the pair of participants.'),
          occurrence=dict(event_type=event,relationship='participation; not mediation',requires='Specific occurrence evidence and bounded interval; event participation is a separate historical claim.',implies_license=False,implies_ongoing_responsibility=False),
          recommendation='Define the inherited role by responsibility/site use; use scoped Authorized roles for permission and event participation for occurrence. This refines the previous umbrella proposal.',
          temporal_policy='Half-open [start,end); null end only for explicitly open-ended responsibility/authorization. Unknown dates are quarantined, not invented.',
          human_approval='NOT_RECORDED',active_ontology_change=False,status='DESIGNED_AND_LAB_TESTED_NOT_INTEGRATED'))
    write('role-pattern-register.json',dict(scope='Six operational roles; proposed refinement, not approved ontology axioms',roles=register))
    (OUT/'schema.sql').write_text(SCHEMA);(OUT/'query.sql').write_text(QUERY)
    cases=[]
    def case(row,name,records,expected,day=20,jurisdiction='LAB',reject=False):
        c=db();error=None
        try:
            for r in records:insert(c,r)
        except sqlite3.IntegrityError as e:error=str(e)
        holder='site' if row[1]=='Facility' else 'org'
        actual=[] if error else [x[0] for x in c.execute(QUERY,dict(role=row[0],holder=holder,day=day,jurisdiction=jurisdiction))]
        passed=bool(error) if reject else (error is None and sorted(actual)==sorted(expected))
        cases.append(dict(id=row[0]+'/'+name,role=row[0],records=records,query_day=day,jurisdiction=jurisdiction,expected_rejection=reject,expected_facets=sorted(expected),actual_facets=actual,error=error,passed=passed))
        c.close()
    for row in ROWS:
        a=record(row,'authorization');r=record(row,'responsibility');e=record(row,'activity')
        case(row,'permission_without_responsibility_or_occurrence',[a],['authorization'])
        case(row,'responsibility_persists_while_idle',[r],['responsibility'])
        case(row,'occurrence_does_not_invent_permission_or_commitment',[e],['activity'])
        case(row,'three_facets_can_coexist',[a,r,e],['authorization','responsibility','activity'])
        case(row,'registration_is_insufficient',[record(row,'registration')],[])
        case(row,'generic_operation_is_insufficient',[record(row,'operation')],[])
        case(row,'generic_scope_is_insufficient',[record(row,'authorization',scope='generic')],[])
        case(row,'wrong_responsibility_scope',[record(row,'responsibility',scope='unrelated')],[])
        case(row,'wrong_jurisdiction',[r],[],jurisdiction='OTHER')
        case(row,'start_is_inclusive',[r],['responsibility'],day=10)
        case(row,'before_start',[r],[],day=9)
        case(row,'end_is_exclusive',[r],[],day=30)
        case(row,'ending_one_of_two_contexts_preserves_role',[r,record(row,'responsibility',id='r2',episode_key='r2',start_day=25,end_day=50)],['responsibility'],day=30)
        case(row,'renewal_can_follow_expiration',[r,record(row,'responsibility',id='r2',episode_key='r2',start_day=30,end_day=50)],['responsibility'],day=30)
        case(row,'open_ended_explicit_commitment',[record(row,'responsibility',end_day=None)],['responsibility'],day=99)
        case(row,'duplicate_constituting_episode_rejected',[r,record(row,'responsibility',id='copy',episode_key='responsibility')],[],reject=True)
        case(row,'same_parties_distinct_commitments_allowed',[r,record(row,'responsibility',id='other',episode_key='independent')],['responsibility'])
        case(row,'reversed_interval_rejected',[record(row,'responsibility',start_day=40)],[],reject=True)
        case(row,'missing_time_rejected',[record(row,'responsibility',start_day=None)],[],reject=True)
        case(row,'missing_counterpart_rejected',[record(row,'responsibility',counterpart=None)],[],reject=True)
        case(row,'self_mediation_rejected',[record(row,'responsibility',counterpart=r['holder'])],[],reject=True)
        case(row,'wrong_bearer_identity_rejected',[record(row,'responsibility',holder='product')],[],reject=True)
        wrong='site2' if row[3]=='Organization' else 'org3'
        case(row,'wrong_counterpart_identity_rejected',[record(row,'responsibility',counterpart=wrong)],[],reject=True)
        case(row,'source_registration_not_authorization_decision',[record(row,'authorization',evidence_id='reg')],[],reject=True)
        case(row,'permission_not_occurrence_evidence',[record(row,'activity',evidence_id='auth')],[],reject=True)
        case(row,'unbounded_occurrence_rejected',[record(row,'activity',end_day=None)],[],reject=True)
    # Readable SQL fixture for manufacturer and idle manufacturing site: neither needs a license/event.
    fixture=db()
    for i in [0,1]:insert(fixture,record(ROWS[i],'responsibility',id='example'+str(i),episode_key='example'+str(i)))
    (OUT/'example.sql').write_text('\n'.join(fixture.iterdump())+'\n');fixture.close()
    after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.iterdir() if p.is_file()}
    assert before==after
    write('cases.json',cases)
    results=dict(status='PASS' if all(c['passed'] for c in cases) else 'FAIL',roles_designed=6,facets_per_role=3,cases=len(cases),passed=sum(c['passed'] for c in cases),expected_rejections=sum(c['expected_rejection'] for c in cases),sqlite_version=sqlite3.sqlite_version,active_artifacts_unchanged=True,active_artifact_sha256=after,ontology_roles_integrated=0,official_antipattern_engine_run=False,scope='Closed-world input admission and facet queries on synthetic data; not OWL/Semantic OntoUML validation or real-data evaluation.')
    write('results.json',results);print(json.dumps({k:v for k,v in results.items() if k!='active_artifact_sha256'},indent=2))
    assert results['status']=='PASS'

if __name__=='__main__':main()
