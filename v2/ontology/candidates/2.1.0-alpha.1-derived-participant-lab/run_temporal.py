"""Finite-trace monitor for a proposed participant immutability policy.

Relator keys are assumed to be established identities, not source record IDs.
Absence, different IRIs and equal external codes do not establish identity facts.
This monitor is neither a complete temporal logic engine nor UFO validation.
"""
import json
from pathlib import Path
H=Path(__file__).resolve().parent

def inspect(trace):
 parent={}
 def root(x):
  parent.setdefault(x,x)
  if parent[x]!=x:parent[x]=root(parent[x])
  return parent[x]
 for a,b in trace.get('same_as',[]):parent[root(a)]=root(b)
 different={frozenset([root(a),root(b)]) for a,b in trace.get('different_from',[])}
 if any(len(x)<2 for x in different):return 'INCONSISTENT_IDENTITY'
 previous={};unknown=False;comparisons=0
 for snapshot in trace['snapshots']:
  if not snapshot.get('complete',False):unknown=True
  for identity,slots in snapshot['relators'].items():
   for slot,value in slots.items():
    if value is None:unknown=True;continue
    key=(identity,slot)
    if key in previous:
     comparisons+=1;a,b=root(previous[key]),root(value)
     if a!=b:
      if frozenset([a,b]) in different:return 'VIOLATION'
      unknown=True
    previous[key]=value
 return 'UNKNOWN' if unknown else ('PRESERVED' if comparisons else 'NO_COMPARABLE_IDENTITY')

def trace(v1,v2,slot='classificationEntity',**kw):
 return {'snapshots':[{'complete':True,'relators':{'relator-1':{slot:v1}}},
                      {'complete':True,'relators':{'relator-1':{slot:v2}}}],**kw}

def main():
 cases=[]
 def add(name,data,expected):
  actual=inspect(data);cases.append({'name':name,'input':data,'expected':expected,'actual':actual,'pass':actual==expected})
 add('stable-product',trace('p1','p1'),'PRESERVED')
 add('known-distinct-product-replacement',trace('p1','p2',different_from=[['p1','p2']]),'VIOLATION')
 fresh=trace('p1','p2');fresh['snapshots'][1]['relators']={'relator-2':{'classificationEntity':'p2'}}
 add('new-established-relator-identity',fresh,'NO_COMPARABLE_IDENTITY')
 incomplete=trace(None,'p1');incomplete['snapshots'][0]['complete']=False
 add('incomplete-first-observation',incomplete,'UNKNOWN')
 add('explicit-sameAs-preserves-participant',trace('p1','alias',same_as=[['p1','alias']]),'PRESERVED')
 add('different-IRIs-alone-unknown',trace('p1','p2'),'UNKNOWN')
 codes=trace('p1','p2',different_from=[['p1','p2']]);codes['external_codes']={'p1':'code-1','p2':'code-1'}
 add('equal-registry-code-cannot-override-distinctness',codes,'VIOLATION')
 add('classification-entry-change',trace('entry1','entry2',slot='classificationEntry',different_from=[['entry1','entry2']]),'VIOLATION')
 add('evidence-record-alias-chain',trace('record1','record3',slot='evidenceItem',same_as=[['record1','record2'],['record2','record3']]),'PRESERVED')
 add('contradictory-identity-facts',trace('p1','p2',same_as=[['p1','p2']],different_from=[['p1','p2']]),'INCONSISTENT_IDENTITY')
 out={'policy_status':'EXPERIMENTAL_UNACCEPTED','identity_key_precondition':'Already established relator identity across time; external record ID alone is insufficient.',
      'scope':'Observed primitive participant slots, finite snapshots; no inference about unobserved times, relator creation, or modern nature.',
      'cases':cases,'pass':sum(c['pass'] for c in cases),'total':len(cases)}
 (H/'temporal-results.json').write_text(json.dumps(out,indent=2)+'\n')
 assert all(c['pass'] for c in cases)
 print(json.dumps({'temporal_pass':out['pass'],'temporal_total':out['total']}))

if __name__=='__main__':main()
