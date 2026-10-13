"""HTTP integration tests against the actual local service, using controlled scenarios."""
import json,threading,tempfile,urllib.request,urllib.error,hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from server import make_server
from runtime import ROOT,connect,export_nt,PRODUCT,P
from rdflib import Graph,URIRef,RDF
from pyshacl import validate

checks=[]
def check(name,value):
    checks.append(dict(name=name,passed=bool(value)))
    assert value,name

with tempfile.TemporaryDirectory() as temp:
    dbpath=Path(temp)/'test.sqlite'
    server=make_server(0,dbpath);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base='http://127.0.0.1:'+str(server.server_port)
    def request(path,payload=None,extra=None):
        headers={'Content-Type':'application/json','X-Explorer-Token':token} if payload is not None else {}
        headers.update(extra or {})
        req=urllib.request.Request(base+path,data=json.dumps(payload).encode() if payload is not None else None,headers=headers)
        try:
            with urllib.request.urlopen(req) as res:
                content=res.read().decode();return res.status,json.loads(content) if 'application/json' in res.headers.get('Content-Type') else content
        except urllib.error.HTTPError as e:return e.code,json.loads(e.read())
    _,context=request('/api/context');token=context['token']
    check('runtime-build-is-the-explorer-software-product',context['build']['software_product']==PRODUCT)
    check('serves-integrated-explorer',request('/')[0]==200 and 'Validate and record' in request('/')[1])
    cases=json.loads((ROOT/'fixtures/transition-cases.json').read_text());shapes=Graph().parse(ROOT/'fixtures/identity-slice.shacl.ttl')
    for i,c in enumerate(cases):
        # Isolated named workspaces and referents prevent contamination between controls.
        t={k:v.replace('urn:v022:synthetic:',f'urn:test:{i}:') if isinstance(v,str) else v for k,v in c['input'].items()}
        env=dict(request_id='case-'+str(i),workspace='case-'+str(i),mode='SCENARIO',transition=t)
        status,out=request('/api/transitions',env)
        check('HTTP-'+c['name'],status==200 and out['status']==c['expected_status'])
        _,nt=request('/api/graph?workspace='+env['workspace'])
        g=Graph().parse(data=nt,format='nt')
        if out['status']=='ACCEPTED':
            ok,_,_=validate(g,shacl_graph=shapes,inference='none')
            check('accepted-graph-shacl-'+c['name'],ok and (URIRef(PRODUCT),RDF.type,URIRef(P+'Product')) in g)
        else:check('no-accepted-graph-'+c['name'],len(g)==0)
    original=dict(request_id='case-0',workspace='case-0',mode='SCENARIO',transition=cases[0]['input'])
    original['transition']={k:v.replace('urn:v022:synthetic:','urn:test:0:') if isinstance(v,str) else v for k,v in original['transition'].items()}
    before=request('/api/history')[1]
    replay=request('/api/transitions',original)[1]
    check('retry-idempotent-without-new-history',replay.get('idempotent_replay') and request('/api/history')[1]==before)
    conflict=json.loads(json.dumps(original));conflict['transition']['evidence']='urn:other:evidence'
    check('reused-request-id-conflict',request('/api/transitions',conflict)[1]['errors']==['REQUEST_ID_CONFLICT'])
    before_nt=request('/api/graph?workspace=case-0')[1]
    retarget=json.loads(json.dumps(original));retarget['request_id']='retarget';retarget['transition'].update(before_v='urn:test:0:v2',after_v='urn:test:0:v2')
    check('cross-snapshot-retarget-rejected',request('/api/transitions',retarget)[1]['status']=='REJECTED')
    check('failed-admission-leaves-accepted-graph-unchanged',request('/api/graph?workspace=case-0')[1]==before_nt)
    changed=json.loads(json.dumps(original));changed['request_id']='mode-change';changed['mode']='DECLARED_OPERATIONAL'
    check('scenario-cannot-be-relabeled-operational',request('/api/transitions',changed)[1]['errors']==['WORKSPACE_MODE_IMMUTABLE'])
    bad=json.loads(json.dumps(original));bad['request_id']='array-operation';bad['transition']['operation']=[]
    check('malformed-field-rejected-without-server-failure',request('/api/transitions',bad)[1]['errors']==['INVALID_FIELD_TYPES'])
    bad['transition']['operation']='restart';bad['transition']['before_r']='urn:bad:>injection'
    check('unsafe-rdf-iri-rejected',request('/api/transitions',bad)[1]['errors']==['UNSAFE_IRI'])
    bad['transition']=dict(original['transition']);bad['transition']['before_c']=bad['transition']['after_c']=bad['transition']['before_r']
    check('type-collision-rejected',request('/api/transitions',bad)[1]['errors']==['CROSS_TYPE_IDENTITY_COLLISION'])
    check('no-token-rejected',request('/api/transitions',original,{'X-Explorer-Token':'invalid'})[0]==403)
    check('foreign-origin-rejected',request('/api/transitions',original,{'Origin':'https://unrelated.example'})[0]==403)
    check('non-json-rejected',request('/api/transitions',original,{'Content-Type':'text/plain'})[0]==415)
    check('oversized-request-rejected',request('/api/transitions',{'padding':'x'*21000})[0]==413)
    check('private-database-not-served',request('/workspace.sqlite')[0]==404)
    check('unknown-record-rejected',request('/api/record?id=missing')[0]==404)
    parallel=json.loads(json.dumps(original));parallel['request_id']='parallel-idempotent'
    with ThreadPoolExecutor(max_workers=4) as pool:outs=list(pool.map(lambda _:request('/api/transitions',parallel)[1],range(4)))
    check('concurrent-retry-single-admission',sum(bool(o.get('idempotent_replay')) for o in outs)==3)
    check('review-and-rejection-retained-as-audit-only',{'REJECTED','REVIEW_REQUIRED','ACCEPTED'} <= {x['status'] for x in request('/api/history')[1]})
    prior=request('/api/history')[1];server.shutdown();server.server_close();thread.join()
    server=make_server(0,dbpath);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base='http://127.0.0.1:'+str(server.server_port)
    check('history-survives-service-restart',request('/api/history')[1]==prior)
    check('graph-survives-service-restart',request('/api/graph?workspace=case-0')[1]==before_nt)
    data=json.loads((ROOT/'generated/explorer-data.json').read_text())
    db=connect(dbpath);objects={x[0] for x in db.execute('SELECT subject FROM triple')};db.close()
    check('pharmaceutical-identities-not-used-as-deployments',all(p['id'] not in objects and p['organization_id'] not in objects for p in data['products']))
    check('historical-pharma-projection-preserved',len(data['products'])==5 and sum(len(x['packages']) for x in data['products'])==7)
    server.shutdown();server.server_close();thread.join()

report=dict(version='0.25.0',passed=len(checks),checks=checks,data_origin='25 controlled transition scenarios; retained historical pharmaceutical source projection',scope='Actual local HTTP service, SQLite persistence, concurrency controls and focused RDF validation. No empirical deployment or human effectiveness study.')
(ROOT/'results/Runtime_Integration_Tests_v0_25_0.json').write_text(json.dumps(report,indent=2))
print('HTTP integration checks:',len(checks),'passed')
