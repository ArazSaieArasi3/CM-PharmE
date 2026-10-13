"""Persistent bounded deployment declarations for the Explorer software product.

Pharmaceutical source records are read-only and are never deployment identities.
This ledger checks declared evidence; it does not execute or verify a deployment.
"""
import hashlib, json, re, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from identity_policy import assess

ROOT = Path(__file__).resolve().parent
VERSION = '0.25.0'
PRODUCT = 'urn:cm-pharme:software:ecosystem-explorer'
P = 'urn:productium:specification-profile:'
TYPE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
FIELDS = {'before_r','after_r','before_v','after_v','before_c','after_c','operation',
          'system_continuity','disposition_continuity','branching','evidence'}
ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$')
STAMP = lambda: datetime.now(timezone.utc).isoformat()

def build_identity():
    files = ['server.py','runtime.py','identity_policy.py','app.mjs','explorer.mjs','role-evidence.mjs',
             'workbench.mjs','explorer-template.html','generated/explorer-data.json']
    hashes = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}
    digest = hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    return dict(software_product=PRODUCT,application_version=VERSION,
                software_version_iri=PRODUCT+':build:'+digest,build_sha256=digest,
                source_files=hashes,ontology_contract_version='0.22.0',
                runtime_claim='Build identity only; no independently established realization identity.')

def connect(path):
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript('''
    CREATE TABLE IF NOT EXISTS workspace(id TEXT PRIMARY KEY, mode TEXT NOT NULL, product TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS realization(iri TEXT PRIMARY KEY, workspace TEXT NOT NULL REFERENCES workspace(id), version TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS capability(iri TEXT PRIMARY KEY, workspace TEXT NOT NULL REFERENCES workspace(id), bearer TEXT NOT NULL REFERENCES realization(iri));
    CREATE TABLE IF NOT EXISTS attempt(seq INTEGER PRIMARY KEY, request_id TEXT UNIQUE NOT NULL, workspace TEXT NOT NULL REFERENCES workspace(id), status TEXT NOT NULL, payload TEXT NOT NULL, decision TEXT NOT NULL, created_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS triple(workspace TEXT NOT NULL REFERENCES workspace(id), subject TEXT NOT NULL, predicate TEXT NOT NULL, object TEXT NOT NULL, PRIMARY KEY(workspace,subject,predicate,object));
    CREATE TRIGGER IF NOT EXISTS fixed_version BEFORE UPDATE OF version ON realization WHEN OLD.version != NEW.version BEGIN SELECT RAISE(ABORT,'IMMUTABLE_REALIZATION_VERSION'); END;
    CREATE TRIGGER IF NOT EXISTS fixed_bearer BEFORE UPDATE OF bearer ON capability WHEN OLD.bearer != NEW.bearer BEGIN SELECT RAISE(ABORT,'IMMUTABLE_CAPABILITY_BEARER'); END;
    ''')
    return db

def triples(workspace, t):
    rows = {(PRODUCT,TYPE,P+'Product')}
    for side in ['before','after']:
        r,v,c = [t[side+'_'+k] for k in ['r','v','c']]
        rows.update([(v,TYPE,P+'ProductVersion'),(r,TYPE,P+'ProductRealization'),
                     (c,TYPE,P+'ProductCapability'),(PRODUCT,P+'hasVersion',v),
                     (r,P+'realizesVersion',v),(r,P+'bearsCapability',c)])
    return [(workspace,*x) for x in sorted(rows)]

def malformed(message):
    return {'status':'REJECTED','errors':[message]}

def submit(db, envelope):
    if not isinstance(envelope,dict) or set(envelope) != {'request_id','workspace','mode','transition'}:
        return malformed('INVALID_ENVELOPE')
    key, ws, mode, t = [envelope[k] for k in ['request_id','workspace','mode','transition']]
    if not isinstance(key,str) or not ID.fullmatch(key) or not isinstance(ws,str) or not ID.fullmatch(ws):
        return malformed('INVALID_REQUEST_OR_WORKSPACE_ID')
    if mode not in ['SCENARIO','DECLARED_OPERATIONAL']:
        return malformed('INVALID_EVIDENCE_MODE')
    if not isinstance(t,dict) or set(t) != FIELDS:
        return malformed('INVALID_TRANSITION_FIELDS')
    if any(not isinstance(t[k],str) for k in FIELDS-{'branching'}) or type(t['branching']) is not bool:
        return malformed('INVALID_FIELD_TYPES')
    for k,v in t.items():
        if isinstance(v,str) and (len(v)>1200 or any(ord(c)<32 for c in v)):
            return malformed('INVALID_TEXT_FIELD')
    # NT export must remain parseable; IRI syntax stricter than the earlier local gate.
    for k in ['before_r','after_r','before_v','after_v','before_c','after_c','evidence']:
        if isinstance(t[k],str) and any(c in t[k] for c in '<>"{}|^`\\'):
            return malformed('UNSAFE_IRI')
    decision = assess(t)
    # Reject scalar aliases between distinct entity categories in this application profile.
    sets = [{t['before_'+k],t['after_'+k]} for k in ['r','v','c']] if all(isinstance(t.get(s+'_'+k),str) for k in ['r','v','c'] for s in ['before','after']) else []
    if sets and (any(sets[i]&sets[j] for i,j in [(0,1),(0,2),(1,2)]) or PRODUCT in set.union(*sets)):
        decision = malformed('CROSS_TYPE_IDENTITY_COLLISION')
    # Immediate transaction serializes competing admissions across server threads.
    db.execute('BEGIN IMMEDIATE')
    try:
        previous = db.execute('SELECT payload,decision FROM attempt WHERE request_id=?',(key,)).fetchone()
        packed = json.dumps(envelope,sort_keys=True)
        if previous:
            if previous['payload'] == packed:
                out = json.loads(previous['decision']);out['idempotent_replay']=True
            else: out = malformed('REQUEST_ID_CONFLICT')
            db.rollback();return out
        previous_ws = db.execute('SELECT mode FROM workspace WHERE id=?',(ws,)).fetchone()
        if previous_ws and previous_ws['mode'] != mode:
            db.rollback();return malformed('WORKSPACE_MODE_IMMUTABLE')
        db.execute('INSERT OR IGNORE INTO workspace VALUES(?,?,?)',(ws,mode,PRODUCT))
        if decision['status']=='ACCEPTED':
            db.execute('SAVEPOINT accepted_population')
            try:
                for category,table,field in [('r','realization','version'),('c','capability','bearer')]:
                    if decision['realization_identity' if category=='r' else 'capability_identity']=='DISTINCT' and db.execute('SELECT 1 FROM '+table+' WHERE iri=?',(t['after_'+category],)).fetchone():
                        raise ValueError('SUCCESSOR_'+table.upper()+'_ID_ALREADY_USED')
                for side in ['before','after']:
                    r,v,c = [t[side+'_'+k] for k in ['r','v','c']]
                    for table,iri,value,field in [('realization',r,v,'version'),('capability',c,r,'bearer')]:
                        old = db.execute('SELECT workspace,'+field+' FROM '+table+' WHERE iri=?',(iri,)).fetchone()
                        if old and (old['workspace'] != ws or old[field] != value):
                            raise ValueError('CROSS_SNAPSHOT_'+field.upper()+'_OR_WORKSPACE_CONFLICT')
                        db.execute('INSERT OR IGNORE INTO '+table+' VALUES(?,?,?)',(iri,ws,value))
                # Check against persisted category collisions, including version-only IRIs.
                type_rows = triples(ws,t)
                for _,iri,pred,typ in type_rows:
                    if pred==TYPE:
                        old = db.execute('SELECT object FROM triple WHERE subject=? AND predicate=?',(iri,TYPE)).fetchall()
                        if any(x[0]!=typ for x in old):raise ValueError('CROSS_SNAPSHOT_TYPE_COLLISION')
                db.executemany('INSERT OR IGNORE INTO triple VALUES(?,?,?,?)',type_rows)
                db.execute('RELEASE accepted_population')
            except (ValueError,sqlite3.IntegrityError) as exc:
                db.execute('ROLLBACK TO accepted_population');db.execute('RELEASE accepted_population')
                decision = malformed(str(exc))
        decision.update(workspace=ws,mode=mode,request_id=key,evidence_acceptance='DECLARATION_ONLY',
                        independent_acceptance='PENDING')
        db.execute('INSERT INTO attempt(request_id,workspace,status,payload,decision,created_at) VALUES(?,?,?,?,?,?)',
                   (key,ws,decision['status'],packed,json.dumps(decision,sort_keys=True),STAMP()))
        db.commit();return decision
    except Exception:
        db.rollback();raise

def history(db):
    return [dict(x) for x in db.execute('SELECT seq,request_id,workspace,status,decision,created_at FROM attempt ORDER BY seq DESC LIMIT 200')]

def export_nt(db, workspace):
    return ''.join(f'<{s}> <{p}> <{o}> .\n' for s,p,o in db.execute(
        'SELECT subject,predicate,object FROM triple WHERE workspace=? ORDER BY subject,predicate,object',(workspace,)))

def record(db, request_id):
    row = db.execute('SELECT payload,decision,created_at FROM attempt WHERE request_id=?',(request_id,)).fetchone()
    if not row:return None
    return dict(declaration=json.loads(row['payload']),decision=json.loads(row['decision']),recorded_at=row['created_at'])
