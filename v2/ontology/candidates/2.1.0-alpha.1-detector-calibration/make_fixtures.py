"""Hand-specified paired legacy witnesses. This is NOT a modern OntoUML converter."""
import copy,json,xml.etree.ElementTree as ET
from pathlib import Path
H=Path(__file__).resolve().parent
XMI='http://www.omg.org/XMI';XSI='http://www.w3.org/2001/XMLSchema-instance';REF='http://nemo.inf.ufes.br/ontouml/refontouml'
ET.register_namespace('xmi',XMI);ET.register_namespace('xsi',XSI);ET.register_namespace('RefOntoUML',REF)
def cls(n,t='Kind',abstract=False):return {'name':n,'type':t,'abstract':abstract}
def rel(n,a,b,t='Association',ca=(0,1),cb=(0,-1),whole=False):
 return {'name':n,'type':t,'ends':[{'name':n+'A','type':a,'lower':ca[0],'upper':ca[1],'aggregation':'shared' if whole else 'none','subset':[]},{'name':n+'B','type':b,'lower':cb[0],'upper':cb[1],'aggregation':'none','subset':[]}]}
def gen(s,g):return {'name':s+'To'+g,'specific':s,'general':g}
def gs(name,gens,disjoint=False,complete=False):return {'name':name,'generalizations':gens,'disjoint':disjoint,'complete':complete}
def model(cs,rs=[],gspec=[],sets=[]):return {'classes':cs,'relations':rs,'generalizations':gspec,'sets':sets}
CASES=[]
def add(family,name,m,expect,why,category='paired',docs=None):
 CASES.append({'family':family,'name':name,'model':copy.deepcopy(m),'expected_engine_occurrences':expect,'rationale':why,'category':category,'documentation_expected_occurrences':docs})
def pair(fam,pos,neg,whypos,whyneg):add(fam,'positive',pos,1,whypos);add(fam,'negative',neg,0,whyneg)
# Deceiving intersection: two concrete sortal parents versus one.
m=model([cls('Person'),cls('Employed','Role'),cls('Student','Role'),cls('WorkingStudent','Role')],[],[gen('Employed','Person'),gen('Student','Person'),gen('WorkingStudent','Employed'),gen('WorkingStudent','Student')]);n=copy.deepcopy(m);n['generalizations'].pop();pair('DecInt',m,n,'Concrete intersection role has two direct sortal parents.','Remove only one intersection-parent edge.')
# A phase is relationally mediated versus the same class being a role.
m=model([cls('Person'),cls('Dependent','Phase'),cls('Agreement','Relator')],[rel('med','Agreement','Dependent','Mediation',(1,1),(1,1))],[gen('Dependent','Person')]);n=copy.deepcopy(m);n['classes'][1]['type']='Role';pair('DepPhase',m,n,'A phase is directly mediated by a relator.','Only the mediated stereotype changes from Phase to Role.')
# Free role specialization; extra independent mediator defines the child.
m=model([cls('Person'),cls('Employee','Role'),cls('Manager','Role'),cls('Employment','Relator'),cls('Appointment','Relator')],[rel('employment','Employment','Employee','Mediation',(1,1),(1,1))],[gen('Employee','Person'),gen('Manager','Employee')]);n=copy.deepcopy(m);n['relations'].append(rel('appointment','Appointment','Manager','Mediation',(1,1),(1,1)));pair('FreeRole',m,n,'Child role has no additional direct mediation.','Additional direct mediation defines the child role.')
# Mixed rigidity in a generalization set versus all-rigid children.
gs0=[gen('A','Person'),gen('B','Person')];m=model([cls('Person'),cls('A','SubKind'),cls('B','Role')],[],gs0,[gs('Types',[x['name'] for x in gs0])]);n=copy.deepcopy(m);n['classes'][2]['type']='SubKind';pair('GSRig',m,n,'One rigid and one anti-rigid child in one generalization set.','Both children rigid; all other set properties preserved.')
# Collective member diversity versus one member type.
m=model([cls('Group','Collective'),cls('MemberA'),cls('MemberB')],[rel('membershipA','Group','MemberA','memberOf',(0,1),(1,-1),True),rel('membershipB','Group','MemberB','memberOf',(0,1),(1,-1),True)]);n=copy.deepcopy(m);n['relations'].pop();pair('HetColl',m,n,'Collective with two memberOf associations to distinct member types.','Exactly one memberOf association.')
# Functional complex with a single component kind versus two.
m=model([cls('Machine'),cls('PartA'),cls('PartB')],[rel('componentA','Machine','PartA','componentOf',(0,1),(1,-1),True)]);n=copy.deepcopy(m);n['relations'].append(rel('componentB','Machine','PartB','componentOf',(0,1),(1,-1),True));pair('HomoFunc',m,n,'Functional whole has exactly one componentOf association.','Second distinct part association removes homogeneous structure.')
# Non-sortal whose children share one kind versus different identity providers.
m=model([cls('Common','Category'),cls('Person'),cls('Organization'),cls('A','SubKind'),cls('B','SubKind')],[],[gen('A','Common'),gen('B','Common'),gen('A','Person'),gen('B','Person')]);n=copy.deepcopy(m);n['generalizations'][-1]=gen('B','Organization');pair('MixIden',m,n,'Two category children share one ultimate kind.','Second child inherits a different ultimate kind.')
# Mixin with all-rigid children versus a rigid/anti-rigid mix.
m=model([cls('Common','Mixin'),cls('Person'),cls('A','SubKind'),cls('B','SubKind')],[],[gen('A','Common'),gen('B','Common'),gen('A','Person'),gen('B','Person')]);n=copy.deepcopy(m);n['classes'][-1]['type']='Role';pair('MixRig',m,n,'Both direct mixin children are rigid.','One direct child is anti-rigid.')
# Two distinct relational dependencies versus one.
m=model([cls('Actor'),cls('R1','Relator'),cls('R2','Relator')],[rel('m1','R1','Actor','Mediation',(1,1),(1,1)),rel('m2','R2','Actor','Mediation',(1,1),(1,1))]);n=copy.deepcopy(m);n['relations'].pop();pair('MultiDep',m,n,'One object directly mediated by two distinct relators.','Only one mediation remains.')
# Shared identity plus optional disjoint generalization set supplies a sharp overlap mutation.
def overlap(fam):
 cs=[cls('Parent'),cls('A','SubKind'),cls('B','SubKind'),cls('Base','Relator' if fam=='RelOver' else 'Kind')];gens=[gen('A','Parent'),gen('B','Parent')];sets=[gs('Overlap',[g['name'] for g in gens])]
 if fam=='PartOver':rs=[rel('r1','A','Base','componentOf',(1,2),(1,1),True),rel('r2','B','Base','componentOf',(1,2),(1,1),True)]
 else:rs=[rel('r1','Base','A','Mediation' if fam=='RelOver' else 'componentOf',(0,1),(1,2),fam!='RelOver'),rel('r2','Base','B','Mediation' if fam=='RelOver' else 'componentOf',(0,1),(1,2),fam!='RelOver')]
 return model(cs,rs,gens,sets)
for fam in ['PartOver','WholeOver','RelOver']:
 m=overlap(fam);n=copy.deepcopy(m);n['sets'][0]['disjoint']=True;pair(fam,m,n,'Two possibly overlapping sibling types share a kind. Upper bounds safely exceed the disputed boundary.','Explicit disjointness of the same siblings removes overlap.')
# Composition: inner association between subtypes of outer target.
m=model([cls('Container'),cls('Person'),cls('A','SubKind'),cls('B','SubKind')],[rel('outer','Container','Person',ca=(0,1),cb=(1,2)),rel('inner','A','B',ca=(0,1),cb=(0,1))],[gen('A','Person'),gen('B','Person')]);n=copy.deepcopy(m);n['relations'][0]['ends'][1]['upper']=1;pair('RelComp',m,n,'Outer target has plural upper bound and both inner ends specialize it.','Change only outer target upper bound to one.')
b=copy.deepcopy(m);b['relations'][0]['ends'][1]['lower']=0;add('RelComp','zero-lower-bound',b,1,'Implementation checks upper but omits the documented positive lower-bound condition.','documentation-discrepancy',0)
# Relator-to-rigid versus role.
m=model([cls('Person'),cls('ParticipatingPerson','SubKind'),cls('Agreement','Relator')],[rel('m','Agreement','ParticipatingPerson','Mediation',(1,1),(1,1))],[gen('ParticipatingPerson','Person')]);n=copy.deepcopy(m);n['classes'][1]['type']='Role';pair('RelRig',m,n,'Relator mediates a rigid subkind with mandatory relator end.','Same endpoint is anti-rigid Role.')
# Relation specialization versus explicitly declared subsetting.
m=model([cls('Person'),cls('Product'),cls('Worker','Role'),cls('Medicine','SubKind')],[rel('general','Person','Product'),rel('special','Worker','Medicine')],[gen('Worker','Person'),gen('Medicine','Product')]);n=copy.deepcopy(m)
for i in range(2):n['relations'][1]['ends'][i]['subset']=[n['relations'][0]['ends'][i]['name']]
pair('RelSpec',m,n,'Relation endpoints specialize the endpoints of a broader association.','Declare explicit subsetting on both specialized ends.')
# Formal relation without datatype support versus support on both endpoints.
m=model([cls('PersonA'),cls('PersonB'),cls('Value','DataType')],[rel('comparison','PersonA','PersonB','FormalAssociation')]);n=copy.deepcopy(m);n['relations'] += [rel('valueA','PersonA','Value'),rel('valueB','PersonB','Value')];pair('UndefFormal',m,n,'Neither formal relation endpoint has datatype support.','Both endpoints have explicit associations to DataType.')
# Undefined phase partition versus explicit discriminator datatype support.
gs0=[gen('PhaseA','Person'),gen('PhaseB','Person')];m=model([cls('Person'),cls('PhaseA','Phase'),cls('PhaseB','Phase'),cls('Value','DataType')],[],gs0,[gs('Partition',[x['name'] for x in gs0],True,True)]);n=copy.deepcopy(m);n['relations'].append(rel('discriminator','Person','Value'));pair('UndefPhase',m,n,'Complete disjoint phase partition with no discriminator.','Parent has datatype support for an intrinsic discriminator.')
# Published WholeOver prose says sum>=2, pinned implementation requires>=3.
b=overlap('WholeOver')
for r in b['relations']:r['ends'][1]['upper']=1
add('WholeOver','upper-sum-two',b,0,'Pinned occurrence constructor requires upper sum>=3; published catalogue says>=2.','documentation-discrepancy',1)
def serialize(m,name):
 root=ET.Element('{'+REF+'}Package',{'{'+XMI+'}version':'2.0','{'+XMI+'}id':'pkg','name':name,'visibility':'public'});by={}
 for c in m['classes']:
  by[c['name']]=ET.SubElement(root,'packagedElement',{'{'+XSI+'}type':'RefOntoUML:'+c['type'],'{'+XMI+'}id':c['name'],'name':c['name'],'visibility':'public','isAbstract':str(c['abstract']).lower()})
 for g in m['generalizations']:
  a={'{'+XMI+'}id':g['name'],'general':g['general']};ss=[s['name'] for s in m['sets'] if g['name'] in s['generalizations']]
  if ss:a['generalizationSet']=' '.join(ss)
  ET.SubElement(by[g['specific']],'generalization',a)
 for r in m['relations']:
  a={'{'+XSI+'}type':'RefOntoUML:'+r['type'],'{'+XMI+'}id':r['name'],'name':r['name'],'visibility':'public','memberEnd':' '.join(e['name'] for e in r['ends'])};rr=ET.SubElement(root,'packagedElement',a)
  for e in r['ends']:
   ea={'{'+XMI+'}id':e['name'],'name':e['name'],'type':e['type'],'association':r['name'],'aggregation':e['aggregation'],'visibility':'public'}
   if e['subset']:ea['subsettedProperty']=' '.join(e['subset'])
   ee=ET.SubElement(rr,'ownedEnd',ea)
   for which,kind in [('lower','LiteralInteger'),('upper','LiteralUnlimitedNatural')]:ET.SubElement(ee,which+'Value',{'{'+XSI+'}type':'RefOntoUML:'+kind,'{'+XMI+'}id':e['name']+which,'value':str(e[which])})
 for s in m['sets']:ET.SubElement(root,'packagedElement',{'{'+XSI+'}type':'RefOntoUML:GeneralizationSet','{'+XMI+'}id':s['name'],'name':s['name'],'generalization':' '.join(s['generalizations']),'isDisjoint':str(s['disjoint']).lower(),'isCovering':str(s['complete']).lower()})
 ET.indent(root,space='  ');return ET.tostring(root,encoding='utf-8',xml_declaration=True)
if __name__=='__main__':
 (H/'fixtures').mkdir(exist_ok=True)
 for c in CASES:
  stem=c['family']+'-'+c['name'];(H/'fixtures'/(stem+'.refontouml')).write_bytes(serialize(c['model'],stem))
 (H/'fixture-manifest.json').write_text(json.dumps({'format':'custom legacy witness specification, NOT native OntoUML JSON','cases':CASES},indent=2)+'\n')
 print('new cases',len(CASES),'families',len(set(c['family'] for c in CASES)))
