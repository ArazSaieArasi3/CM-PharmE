import json,pathlib,hashlib,collections,tempfile,subprocess,platform
from rdflib import Graph,Namespace,RDF,RDFS,OWL,BNode,Literal,XSD
from pyshacl import validate
from owlready2.reasoning import _HERMIT_CLASSPATH
OUT=pathlib.Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'v2/ontology/candidates').exists())
d=json.loads((OUT/'requirements.json').read_text());checks=[]
def check(name,ok,detail=None):checks.append(dict(id=name,passed=bool(ok),detail=detail))
req=d['requirements'];ids={x['id'] for x in req};cs=d['acceptance_contracts']
check('unique-stable-83-IDs',len(req)==len(ids)==83)
check('one-contract-per-row',len(cs)==83 and {x['requirement_id'] for x in cs}==ids)
check('71-functional-12-quality',sum(x['kind']=='functional' for x in cs)==71 and sum(x['kind']=='nonfunctional' for x in cs)==12)
check('complete-contract-oracles',all(x['positive_oracle'] and x['negative_oracle'] and x['boundary_oracle'] and x['input'] and x['independence_rule'] for x in cs))
check('all-functional-questions',all(x['question'] for x in cs if x['kind']=='functional'))
check('decision-links-resolve',all(set(x['requirement_ids'])<=ids for x in d['overlap_decisions']))
check('all-retention-dispositions-recorded',all(x['specification_disposition'] in ['RETAIN_SCOPED_SPECIALIZATION','RETAIN_DISTINCT_OBLIGATION'] for x in req))
check('specialization-links-resolve',all(x['specializes_requirement_id'] is None or x['specializes_requirement_id'] in ids for x in req))
parents={x['id']:x['specializes_requirement_id'] for x in req};acyclic=True
for k in parents:
 seen=set();z=k
 while z:
  if z in seen:acyclic=False;break
  seen.add(z);z=parents[z]
check('specialization-acyclic',acyclic)
check('exact-normalized-statements-unique',len({' '.join(x['statement_fa'].split()) for x in req})==83,'No semantic uniqueness claim follows.')
check('no-unresolved-document-reference-row',not any(x['comparison_status']=='UNRESOLVED_MAPPING' for x in req))
check('historical-alias-preserved',next(x for x in req if x['id']=='R-DS-04')['source_row_ids']==['R-DS-04','B2-DS-07'] and 'B2-DS-07' not in ids)
check('13-refinements-separate',len(d['refinements'])==13 and not ids&{x['id'] for x in d['refinements']})
check('no-invented-semantic-acceptance',all(x['acceptance_status']=='PENDING_SEMANTIC_REVIEW' for x in req))
check('source-hashes-unchanged',all(hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256'] for s in d['sources']))
check('historical-inventories-separate',len(d['historical_source_inventories']['discovery'])==97 and len(d['historical_source_inventories']['held_out'])==51)

module=ROOT/'v2/ontology/candidates/2.1.0-alpha.1-module-contract-lab/modules'
BA=module/'BA'; contract=json.loads((BA/'contract.json').read_text());schema=Graph().parse(BA/'ontology.ttl');hier=Graph().parse(BA/'hierarchy.ttl');shapes=Graph().parse(BA/'shapes.ttl')
C=Namespace('https://w3id.org/cm-pharme/2.1/');D=Namespace('https://w3id.org/cm-pharme/experimental/coherence/');T=Namespace('urn:orsd-02:')
check('selected-relation-declared',(D.capabilityRealizedInLogistics,RDF.type,OWL.ObjectProperty) in schema)
check('selected-relation-signature',str(D.capabilityRealizedInLogistics) in contract['properties'])
zero=Graph();zero.add((T.org,RDF.type,C.Organization));zero.add((T.capZero,RDF.type,C.EnterpriseCapability));zero.add((T.capZero,C.capabilityBearer,T.org))
executed=Graph();executed.add((T.org,RDF.type,C.Organization));executed.add((T.capExecuted,RDF.type,C.EnterpriseCapability));executed.add((T.capExecuted,C.capabilityBearer,T.org));executed.add((T.activity,RDF.type,C.DistributionLogisticsActivity));executed.add((T.capExecuted,D.capabilityRealizedInLogistics,T.activity))
q=(OUT/'verification/ba02-corrected.rq').read_text();positive_q=(OUT/'verification/ba02-recorded_execution.rq').read_text()
def rows(g,query):return sorted([[str(v) for v in row] for row in g.query(query)])
query_results=[]
def qc(name,g,query,expected):
 actual=rows(g,query);query_results.append(dict(id=name,actual=actual,expected=expected,passed=actual==expected))
qc('BA02-zero-recorded',zero,q,[[str(T.capZero),str(T.org)]])
qc('BA02-executed',executed,q,[])
qc('BA02-mixed',zero+executed,q,[[str(T.capZero),str(T.org)]])
qc('BA02-positive-world',executed,positive_q,[[str(T.capExecuted),str(T.activity)]])
qc('BA02-empty-graph',Graph(),q,[])
legacy=Graph()+zero;legacy.add((T.capZero,Namespace('https://w3id.org/cm-pharme/experimental/four-domain/').capabilityRealizedIn,T.activity))
qc('BA02-legacy-name-not-aliased',legacy,q,[[str(T.capZero),str(T.org)]])
mutant_query=q.replace('d:capabilityRealizedInLogistics','<https://w3id.org/cm-pharme/experimental/four-domain/capabilityRealizedIn>')
mutant_actual=rows(executed,mutant_query)
query_results.append(dict(id='BA02-old-predicate-mutation-detected',actual=mutant_actual,expected_behavior='must differ from the empty expected answer on the executed graph',passed=mutant_actual!=[]))
zero.serialize(OUT/'verification/zero-recorded.ttl',format='turtle');executed.serialize(OUT/'verification/executed.ttl',format='turtle')

def reason(g):
 with tempfile.TemporaryDirectory() as td:
  f=pathlib.Path(td)/'input.rdf';g.serialize(f,format='xml')
  p=subprocess.run(['java','-Xmx1000M','-cp',_HERMIT_CLASSPATH,'org.semanticweb.HermiT.cli.CommandLine','-U',f.as_uri()],capture_output=True,text=True,timeout=55)
  output=p.stdout+'\n'+p.stderr
  if p.returncode==0:
   assert "Classes equivalent to 'owl:Nothing':" in output,output
   unsat=[s.strip().strip('<>') for s in p.stdout.splitlines() if s.startswith('\t') and s.strip()!='owl:Nothing']
   return dict(consistent=True,unsatisfiable_named_classes=unsat)
  if 'Inconsistent ontology' in output:return dict(consistent=False,unsatisfiable_named_classes=[])
  raise RuntimeError(output)
no_execution=Graph()+zero;r=BNode();no_execution.add((T.capZero,RDF.type,r));no_execution.add((r,RDF.type,OWL.Restriction));no_execution.add((r,OWL.onProperty,D.capabilityRealizedInLogistics));no_execution.add((r,OWL.maxCardinality,Literal(0,datatype=XSD.nonNegativeInteger)))
mutation=Graph();r2=BNode();mutation.add((C.EnterpriseCapability,RDFS.subClassOf,r2));mutation.add((r2,RDF.type,OWL.Restriction));mutation.add((r2,OWL.onProperty,D.capabilityRealizedInLogistics));mutation.add((r2,OWL.someValuesFrom,C.DistributionLogisticsActivity))
no_execution.serialize(OUT/'verification/zero-execution-countermodel.ttl',format='turtle');mutation.serialize(OUT/'verification/mandatory-execution-mutant.ttl',format='turtle')
logical=[]
for name,g,expected in [('BA02-countermodel',schema+no_execution,True),('BA02-execution-consistent',schema+executed,True),('BA02-mutant-countermodel',schema+mutation+no_execution,False)]:
 result=reason(g);logical.append(dict(id=name,expected_consistency=expected,**result,passed=result['consistent']==expected and not result['unsatisfiable_named_classes']))

admission=[]
for case in contract['admission_cases']:
 ok,report,_=validate(Graph().parse(BA/case['fixture'])+hier,shacl_graph=shapes,advanced=True,inference='none')
 marker=case.get('marker');blob=report.serialize(format='turtle')
 admission.append(dict(id=case['id'],expected=case['expected'],actual=bool(ok),marker=marker,passed=bool(ok)==case['expected'] and (marker is None or marker in blob)))
replays=[]
for m in ['RM','PV','BA','DS']:
 h=module/m;co=json.loads((h/'contract.json').read_text())
 for x in co['queries']:
  actual=rows(Graph().parse(h/x['fixture']),x['query']);replays.append(dict(module=m,id=x['id'],passed=actual==x['expected']))
check('query-oracle-sensitivity',all(x['passed'] for x in query_results))
check('countermodel-and-mutation',all(x['passed'] for x in logical))
check('BA-admission-regression',all(x['passed'] for x in admission))
check('historical-query-regression',all(x['passed'] for x in replays))
result=dict(document_version='0.2.0',model_baseline_commit=d['model_baseline_commit'],checks=checks,query_cases=query_results,reasoner_cases=logical,BA_admission_cases=admission,historical_query_replays=replays,summary={k:[sum(z['passed'] for z in v),len(v)] for k,v in [('document_checks',checks),('new_query_cases',query_results),('new_reasoner_cases',logical),('BA_admission',admission),('historical_query_replays',replays)]},runtime=dict(python=platform.python_version(),rdflib=__import__('rdflib').__version__,pyshacl=__import__('pyshacl').__version__,owlready2=__import__('owlready2').VERSION,reasoner='HermiT CLI OWLAPI on Java 17'),limits=['Seven query cases and three logical cases test one scoped requirement; counts are not ten distinct requirements.','The old-predicate query mutation and mandatory-execution ontology mutation are expected to fail their respective correctness/consistency conditions. Detecting them passes the sensitivity checks.','Independent synthetic witnesses are tests of requirements, not empirical domain evidence.','The 23 historical query replays are regression only and still include the archived stale BA query. It is superseded as evidence for R-BA-02 by the new scoped query.','The other 47 functional acceptance contracts are specified but have no new standalone acceptance execution in this package.','No native ontology semantics, archived fixtures or historical results were modified.'])
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result['summary']))
assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
