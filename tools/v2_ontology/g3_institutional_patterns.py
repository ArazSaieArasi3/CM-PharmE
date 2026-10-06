#!/usr/bin/env python3
"""G3-1c bounded institutional-role design lab, without active ontology mutation."""
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'v2/research/w4/g3-1c-institutional-patterns'
BASE=ROOT/'v2/ontology/candidates/2.1.0-alpha.1-g3a-review'
PREVIOUS=ROOT/'v2/research/w4/g3-1b-operational-patterns'
PROFILES=[
 ('mandate','RegulatoryAuthorityRole','Organization','mandate_instrument','regulatory_mandate'),
 ('label_responsibility','ProductResponsibleLabelerRole','MedicinalProduct','responsibility_instrument','product_label_responsibility'),
 ('listing','ProductResponsibleLabelerRole','MedicinalProductPresentation','listing_responsibility_evidence','market_listing'),
 ('funding','PayerFundingOrganizationRole','Organization','funding_instrument','institutional_funding'),
]
SCHEMA='''PRAGMA foreign_keys=ON;
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
'''
QUERY='''SELECT DISTINCT p.role FROM episode e JOIN profile p ON p.id=e.profile
 WHERE e.holder=:holder AND e.scope=p.scope AND e.jurisdiction=:jurisdiction
 AND e.start_day<=:day AND (e.end_day IS NULL OR :day<e.end_day) ORDER BY p.role;'''

def dump(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def hashes(): return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.iterdir() if p.is_file()}
def db():
 c=sqlite3.connect(':memory:');c.executescript(SCHEMA)
 c.executemany('INSERT INTO entity VALUES (?,?)',[('org','Organization'),('org2','Organization'),('org3','Organization'),('site','Facility'),('product','MedicinalProduct'),('presentation','MedicinalProductPresentation')])
 c.executemany('INSERT INTO profile VALUES (?,?,?,?,?)',PROFILES)
 c.executemany('INSERT INTO evidence VALUES (?,?)',[(p[0],p[3]) for p in PROFILES]+[('aggregate','aggregate_observation'),('generic','source_label')])
 return c
def rec(profile,**kw):
 p=next(p for p in PROFILES if p[0]==profile)
 r=dict(id=profile,episode_key=profile,profile=profile,holder='org',counterpart={'Organization':'org2','MedicinalProduct':'product','MedicinalProductPresentation':'presentation'}[p[2]],evidence=profile,scope=p[4],jurisdiction='LAB',start_day=10,end_day=30)
 r.update(kw);return r
def insert(c,r):c.execute('INSERT INTO episode ('+','.join(r)+') VALUES ('+','.join('?' for _ in r)+')',list(r.values()))

def main():
 OUT.mkdir(parents=True,exist_ok=True);before=hashes();cases=[]
 def case(name,records,expected,day=20,jurisdiction='LAB',claims=(),reject=None):
  c=db();error=None
  try:
   for r in records:insert(c,r)
   for i,k in enumerate(claims):c.execute('INSERT INTO observed_claim VALUES (?,?,?)',(str(i),'org',k))
  except sqlite3.IntegrityError as ex:error=str(ex)
  actual=[] if error else [r[0] for r in c.execute(QUERY,dict(holder='org',jurisdiction=jurisdiction,day=day))]
  passed=(error is not None and reject in error) if reject else (error is None and actual==sorted(expected))
  cases.append(dict(id=name,records=records,observed_claims=list(claims),day=day,jurisdiction=jurisdiction,expected_roles=sorted(expected),expected_error_contains=reject,actual_roles=actual,error=error,passed=passed));c.close()
 for profile,role,other,ev,scope in PROFILES:
  r=rec(profile)
  case(profile+'/effective_without_any_exercise_or_payment',[r],[role])
  case(profile+'/before_start',[r],[],day=9)
  case(profile+'/inclusive_start',[r],[role],day=10)
  case(profile+'/exclusive_end',[r],[],day=30)
  case(profile+'/other_jurisdiction',[r],[],jurisdiction='OTHER')
  case(profile+'/other_scope',[rec(profile,scope='unrelated')],[])
  case(profile+'/open_ended',[rec(profile,end_day=None)],[role],day=99)
  case(profile+'/renewed',[r,rec(profile,id='renewal',episode_key='renewal',start_day=30,end_day=50)],[role],day=30)
  case(profile+'/one_context_ends_other_survives',[r,rec(profile,id='overlap',episode_key='overlap',start_day=25,end_day=50)],[role],day=30)
  case(profile+'/all_contexts_end',[r,rec(profile,id='overlap',episode_key='overlap',start_day=25,end_day=50)],[],day=50)
  case(profile+'/same_parties_independent_episode',[r,rec(profile,id='independent',episode_key='independent')],[role])
  case(profile+'/duplicate_episode',[r,rec(profile,id='copy')],[],reject='UNIQUE constraint failed')
  case(profile+'/wrong_bearer',[rec(profile,holder='site')],[],reject='holder_identity')
  case(profile+'/wrong_counterpart',[rec(profile,counterpart='site')],[],reject='counterpart_identity')
  case(profile+'/missing_counterpart',[rec(profile,counterpart=None)],[],reject='NOT NULL constraint failed')
  case(profile+'/self_relator',[rec(profile,counterpart='org')],[],reject='holder<>counterpart' if other=='Organization' else 'counterpart_identity')
  case(profile+'/aggregate_is_not_commitment',[rec(profile,evidence='aggregate')],[],reject='evidence_boundary')
  case(profile+'/label_is_not_commitment',[rec(profile,evidence='generic')],[],reject='evidence_boundary')
  case(profile+'/unknown_start',[rec(profile,start_day=None)],[],reject='NOT NULL constraint failed')
  case(profile+'/reversed_interval',[rec(profile,end_day=9)],[],reject='CHECK constraint failed')
  case(profile+'/missing_evidence',[rec(profile,evidence='missing')],[],reject='FOREIGN KEY constraint failed')
  case(profile+'/empty_jurisdiction',[rec(profile,jurisdiction=' ')],[],reject='CHECK constraint failed')
  case(profile+'/unrelated_observation_does_not_change_role',[r],[role],claims=['aggregate_published','payment_observed','authorization_issued'])
 # Integration traps: union is inclusive OR, not AND, and observations cannot create duties.
 product='ProductResponsibleLabelerRole'
 case('product/listing_and_commitment_overlap',[rec('listing'),rec('label_responsibility')],[product])
 case('product/expired_listing_but_live_responsibility',[rec('listing',end_day=20),rec('label_responsibility')],[product])
 case('product/expired_responsibility_but_live_listing',[rec('label_responsibility',end_day=20),rec('listing')],[product])
 case('product/neither_route',[],[])
 for k in ['authorization_issued','payment_observed','aggregate_published','label_string','manufacturing_observed']:
  case('observation_only/'+k,[],[],claims=[k])
 case('authority/grantor_need_not_hold_same_mandate',[rec('mandate')],['RegulatoryAuthorityRole'])
 case('all_three_roles_may_overlap',[rec('mandate'),rec('label_responsibility'),rec('funding')],['RegulatoryAuthorityRole',product,'PayerFundingOrganizationRole'])
 case('observations_do_not_revive_expired_mandate',[rec('mandate')],[],day=30,claims=['authorization_issued'])
 case('funding/commitment_not_license_or_label',[rec('funding')],['PayerFundingOrganizationRole'])
 case('listing/product_is_not_presentation',[rec('listing',counterpart='product')],[],reject='counterpart_identity')
 case('label/presentation_requires_explicit_mapping',[rec('label_responsibility',counterpart='presentation')],[],reject='counterpart_identity')
 (OUT/'schema.sql').write_text(SCHEMA);(OUT/'query.sql').write_text(QUERY)
 c=db()
 for p in ['mandate','label_responsibility','funding']:insert(c,rec(p))
 (OUT/'example.sql').write_text('\n'.join(c.iterdump())+'\n');c.close()
 dump('cases.json',cases)
 # Preserve the earlier six proposals verbatim as linked inputs; never mark approval by execution.
 previous=json.loads((PREVIOUS/'role-pattern-register.json').read_text())['roles']
 nine=[dict(id=f'G3-D{i+1:02}',role=r['role'],recommendation=r['recommendation'],definition=r['responsibility']['role_definition'],identity=r['identity_provider'],source_package='../g3-1b-operational-patterns/role-pattern-register.json',author_decision='PENDING',integration='NOT_APPLIED') for i,r in enumerate(previous)]
 remaining=[
  dict(role='RegulatoryAuthorityRole',relator='RegulatoryMandate',counterpart='MandateConferringOrganizationRole',counterpart_identity='Organization',definition='Organization bearing an effective regulatory mandate for a specified jurisdiction and functional scope.',recommendation='Ground authority in mandate, independently of whether it has already performed a regulatory act.',anchors=['V2C-003','W4 R2/R3/R13'],boundary='Conferring institution must be evidenced; do not invent a grantor or recursively require it to bear the same mandate.'),
  dict(role='ProductResponsibleLabelerRole',relator='ProductLabelResponsibility OR existing MarketListing',counterpart='ResponsibilitySubjectProductRole OR existing ListedPresentationRole',counterpart_identity='MedicinalProduct OR MedicinalProductPresentation, kept distinct',definition='Organization bearing product/label responsibility through an explicit responsibility episode or the already justified listing-responsibility context.',recommendation='Preserve ListingResponsibleOrganizationRole as one route; add ProductLabelCommitmentOrganizationRole as an alternative. Use an overlapping covering set only for the bounded proposed scope; never require both routes.',anchors=['V2C-006','W4 R6','G3a subtype repair'],boundary='Product-side subject roles do not make the product responsible. No inference of manufacturing, market approval or mandatory listing from label responsibility.'),
  dict(role='PayerFundingOrganizationRole',relator='InstitutionalFundingCommitment',counterpart='InstitutionallyFundedOrganizationRole',counterpart_identity='Organization',definition='Organization bearing an evidenced institutional funding/reimbursement commitment toward a distinct recipient/provider organization.',recommendation='Adopt this bounded institutional profile for the current candidate; defer direct-person entitlement until a Person identity and eligible-beneficiary pattern are justified.',anchors=['V2C-009','V2R-072','Market Access extension'],boundary='This proposed scope restriction needs author disposition. An aggregate NHIF publisher or observed remitter is not automatically a funder; no patient/payment/entitlement individuals invented.')
 ]
 for i,r in enumerate(remaining,7):
  r.update(id=f'G3-D{i:02}',identity='Organization',author_decision='PENDING',integration='NOT_APPLIED',per_relator_cardinality='1 holder + 1 distinct counterpart for each assignment route',relators_per_current_role='1..* on the defining route; inclusive OR across product routes',temporal_rule='[start,end); role lost only when final matching episode ends',relator_identity='Constituting institutional episode, not source-row identity or participant pair',source_package='README.md')
  nine.append(r)
 dump('nine-role-decisions.json',dict(status='READY_FOR_AUTHOR_REVIEW_WITH_EXPLICIT_SCOPE_LIMITS',decisions=nine,approved=0,integrated=0))
 assert len(nine)==9 and len({r['role'] for r in nine})==9
 assert before==hashes()
 summary=dict(status='PASS' if all(r['passed'] for r in cases) else 'FAIL',new_test_cases=len(cases),passed=sum(r['passed'] for r in cases),expected_rejections=sum(r['expected_error_contains'] is not None for r in cases),sqlite_version=sqlite3.sqlite_version,roles_in_review_package=9,new_role_definitions_integrated=0,human_approvals_recorded=0,active_ontology_unchanged=True,baseline_sha256=before,official_antipattern_engine_run=False,scope='Synthetic SQLite admission/query tests of bounded proposal profiles, not ontology completeness or formal OntoUML validation')
 dump('results.json',summary)
 print(json.dumps({k:v for k,v in summary.items() if k!='baseline_sha256'},indent=2))
 for r in cases:
  if not r['passed']:print('FAILED',r['id'],r['error'],r['actual_roles'])
 assert summary['status']=='PASS'

if __name__=='__main__':main()
