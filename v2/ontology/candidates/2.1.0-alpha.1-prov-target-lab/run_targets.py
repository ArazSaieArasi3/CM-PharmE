"""Independently specified fictional target scenarios and alternative range policies.

These source-claim profiles check explicit scope/evidence, not real-world causality.
No scenario is presented as an observed pharmaceutical incident.
"""
from common import *
from datetime import datetime
scenarios=[
 {'id':'D1','family':'disruption','target':'Facility','text':'A fictional flood damage report names the sterile facility and its loss of operating capacity.'},
 {'id':'D2','family':'disruption','target':'ManufacturingActivity','text':'A fictional power outage report names the interrupted fill-finish occurrence.'},
 {'id':'D3','family':'disruption','target':'SupplyDependency','text':'A fictional supplier suspension report names the affected provider-dependent supply relation.'},
 {'id':'R1','family':'assessment','target':'SupplyDependency','text':'A preventive assessment scopes a sole-supplier dependency before any incident is asserted.'},
 {'id':'R2','family':'assessment','target':'Facility','text':'A prospective quality assessment scopes facility contamination controls.'},
 {'id':'R3','family':'assessment','target':'RiskTreatmentPlan','text':'A review evaluates a proposed alternative-supply plan without claiming its execution.'},
 {'id':'R4','family':'assessment','target':'ManufacturingActivity','text':'An assessment names the manufacturing occurrence being reviewed; its report is a separate output.'}
]
write('target-scenarios.json',{'status':'PREDECLARED_SYNTHETIC_SCENARIOS_NOT_AUTHOR_ACCEPTED','source_basis':['v2/research/w4/risk-resilience-extension.md','https://database.ich.org/sites/default/files/ICH_Q9%28R1%29_Guideline_Step4_2025_0115.pdf'],'cases':scenarios,'interpretation':'ICH supports considering diverse quality-risk contexts; it does not prescribe these classes, OWL ranges or fictional facts. Target lists are deliberately non-exhaustive.'})
def fixture(s):
 g=graph();case=Q[s['id']];source=Q[s['id']+'-event'];target=Q[s['id']+'-target'];claim=Q[s['id']+'-claim'];record=Q[s['id']+'-record']
 typ(g,case,Q.TargetCase);g.add((case,Q.family,Literal(s['family'])));g.add((case,Q.source,source));g.add((case,Q.target,target))
 typ(g,source,C.DisruptionEvent if s['family']=='disruption' else C.RiskAssessmentActivity)
 typ(g,target,C[s['target']]);typ(g,claim,C.Assertion);typ(g,record,C.SourceRecord)
 g.add((case,Q.claim,claim));g.add((case,Q.sourceRecord,record));g.add((record,R.carrierClaim,claim))
 g.add((case,Q.targetClass,C[s['target']]));g.add((case,Q.evidenceKind,Literal('explicit-effect-report' if s['family']=='disruption' else 'explicit-assessment-scope')))
 if s['family']=='disruption':
  g.add((case,Q.eventStart,Literal('2026-09-01T01:00:00Z',datatype=XSD.dateTime)))
  g.add((case,Q.effectObservedAt,Literal('2026-09-01T02:00:00Z',datatype=XSD.dateTime)))
 else:
  g.add((source,Q.assessmentOutput,claim))
 if s['target']=='SupplyDependency':
  # Named role players witness the existing relator's primitive dependencies.
  for prop,role,suffix in [(C.dependencyProvider,C.ProviderOrganizationRole,'provider'),(C.dependencyDependent,C.DependentOrganizationRole,'dependent')]:
   n=Q[s['id']+'-'+suffix];typ(g,n,C.Organization);typ(g,n,role);g.add((target,prop,n))
 return g,case,source,target
def admission(g,case):
 family=str(g.value(case,Q.family) or '');source=g.value(case,Q.source);target=g.value(case,Q.target)
 claim=g.value(case,Q.claim);record=g.value(case,Q.sourceRecord);declared=g.value(case,Q.targetClass)
 if None in [source,target,claim,record,declared]:return 'UNKNOWN'
 if (target,RDF.type,declared) not in g or (record,R.carrierClaim,claim) not in g:return 'UNKNOWN'
 if (record,RDF.type,C.SourceRecord) not in g or (claim,RDF.type,C.Assertion) not in g:return 'UNKNOWN'
 if family=='disruption':
  if (source,RDF.type,C.DisruptionEvent) not in g or str(g.value(case,Q.evidenceKind))!='explicit-effect-report':return 'UNKNOWN'
  a=g.value(case,Q.eventStart);b=g.value(case,Q.effectObservedAt)
  if a is None or b is None:return 'UNKNOWN'
  a,b=a.toPython(),b.toPython()
  if not isinstance(a,datetime) or not isinstance(b,datetime) or a.tzinfo is None or b.tzinfo is None:return 'UNKNOWN'
  if b<a:return 'REJECTED_TEMPORAL_ORDER'
  return 'SOURCE_REPORTED_EFFECT'
 if family=='assessment':
  if (source,RDF.type,C.RiskAssessmentActivity) not in g or str(g.value(case,Q.evidenceKind))!='explicit-assessment-scope':return 'UNKNOWN'
  return 'SOURCE_REPORTED_SCOPE'
 return 'UNKNOWN'
cases=[];logic=[]
def observe(name,g,case,want):
 actual=admission(g,case);save('target-fixtures/'+name+'.ttl',g)
 cases.append({'name':name,'expected':want,'actual':actual,'pass':actual==want})
def reason(name,g,want):
 result=hermit(full+g);save('target-fixtures/'+name+'.ttl',g)
 logic.append({'name':name,'expected_consistent':want,**result,'pass':result['consistent']==want and not result['unsatisfiable_named_classes']})
for s in scenarios:
 g,case,source,target=fixture(s)
 observe(s['id']+'-positive',g,case,'SOURCE_REPORTED_EFFECT' if s['family']=='disruption' else 'SOURCE_REPORTED_SCOPE')
 missing=g+Graph();missing.remove((case,Q.sourceRecord,None));observe(s['id']+'-missing-record',missing,case,'UNKNOWN')
 weak=g+Graph();weak.set((case,Q.evidenceKind,Literal('co-report-only')));observe(s['id']+'-mere-co-report',weak,case,'UNKNOWN')
 parent=C.disruptionAffects if s['family']=='disruption' else C.riskAssessmentConcerns
 # A declared scope/effect claim is not automatically a world-level parent edge.
 no_edge=g+Graph();not_edge(no_edge,source,parent,target)
 reason(s['id']+'-profile-does-not-assert-world-edge',no_edge,True)
 # Compare parent range policies on an explicitly asserted hypothetical edge.
 edge=g+Graph();edge.add((source,parent,target))
 if s['target']!='SupplyDependency':not_type(edge,target,C.SupplyDependency)
 reason(s['id']+'-broad-parent-alternative-A',edge,True)
 narrow=edge+Graph();narrow.add((parent,RDFS.range,C.SupplyDependency))
 reason(s['id']+'-dependency-only-alternative-B',narrow,s['target']=='SupplyDependency')
 if s['family']=='disruption':
  reverse=g+Graph();reverse.set((case,Q.effectObservedAt,Literal('2026-08-01T02:00:00Z',datatype=XSD.dateTime)))
  observe(s['id']+'-effect-before-event',reverse,case,'REJECTED_TEMPORAL_ORDER')
  nozone=g+Graph();nozone.set((case,Q.eventStart,Literal('2026-09-01T01:00:00',datatype=XSD.dateTime)))
  observe(s['id']+'-timezone-missing',nozone,case,'UNKNOWN')
for source_cls,child,parent in [(C.DisruptionEvent,C.disruptionAffectsDependency,C.disruptionAffects),(C.RiskAssessmentActivity,C.riskAssessmentConcernsDependency,C.riskAssessmentConcerns)]:
 g=graph();g.add((T.x,child,T.y));not_edge(g,T.x,parent,T.y)
 reason(str(child).split('/')[-1]+'-entails-parent',g,False)
 g=graph();g.add((T.x,parent,T.y));not_edge(g,T.x,child,T.y)
 reason(str(child).split('/')[-1]+'-parent-does-not-entail-child',g,True)
out={'scenario_families':len(scenarios),'admission_cases':cases,'admission_pass':sum(x['pass'] for x in cases),'admission_total':len(cases),
 'reasoner_cases':logic,'reasoner_pass':sum(x['pass'] for x in logic),'reasoner_total':len(logic),
 'native_endpoints_changed':0,'real_incident_witnesses':0,'author_accepted':False,
 'recommendation':'Keep parent target/cardinality unresolved; use source-qualified scope/effect profiles and typed dependency children. Reject a universal SupplyDependency-only range. Do not freeze an exhaustive union or invent Entity merely for the converter.',
 'alternatives':{'A':'Current broad parent plus evidence-qualified admission; preferred interim research policy, native conversion still blocked.',
 'B':'Universal SupplyDependency range rejects the five explicit non-dependency counterexamples; do not select.',
 'C':'Split by target family into typed predicates, preserving parent only as an OWL/query umbrella. Viable proposal but needs native subsetting/stereotype and complete target-universe review; not implemented here.'},
 'limit':'These seven scenarios exercise bounded semantics and countermodels, not independent empirical causal validation. Passing admission means the source claim has required fields; it never materializes a world-level causal edge.'}
write('target-results.json',out);print(json.dumps({k:out[k] for k in ['scenario_families','admission_pass','admission_total','reasoner_pass','reasoner_total']}),flush=True)
assert all(x['pass'] for x in cases+logic)
