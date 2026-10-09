#!/usr/bin/env python3
"""Integrate nine recommended definitions in a non-release candidate; final review stays open."""
import copy, json, hashlib, subprocess
from pathlib import Path
from rdflib import Graph, Namespace, BNode, URIRef, Literal, RDF, RDFS, OWL, XSD
from rdflib.collection import Collection
from jsonschema import Draft202012Validator, FormatChecker
from pyshacl import validate
import owlready2
import g1_model as m
import g1_audit as audit
import g1_lab as lab
import g1_reasoners as reasoners
import g2_connections as g2

ROOT=m.ROOT;CM=m.CM;META=m.META;SH=m.SH
BASE=ROOT/'v2/ontology/candidates/2.1.0-alpha.1-g3a-review'
OUT=BASE.parent/'2.1.0-alpha.1-g3d-candidate'
LAB=Namespace('https://example.org/cm-pharme-g3d/')
ROWS=[
 ('ManufacturingResponsibility','ManufacturerRole','Organization','ManufacturingResponsibilitySubjectRole','MedicinalProduct'),
 ('ManufacturingSiteUse','ManufacturingSiteRole','Facility','AssigningManufacturingSiteUseOrganizationRole','Organization'),
 ('ImportResponsibility','ImporterRole','Organization','ImportResponsibilitySubjectRole','MedicinalProduct'),
 ('WholesaleResponsibility','WholesaleDistributorRole','Organization','WholesaleResponsibilitySubjectRole','MedicinalProduct'),
 ('LogisticsServiceCommitment','ThirdPartyLogisticsProviderRole','Organization','CommissioningLogisticsClientRole','Organization'),
 ('DistributionSiteUse','DistributionSiteRole','Facility','AssigningDistributionSiteUseOrganizationRole','Organization'),
 ('RegulatoryMandate','RegulatoryAuthorityRole','Organization','MandateConferringOrganizationRole','Organization'),
 ('ProductLabelResponsibility','ProductLabelCommitmentOrganizationRole','Organization','ResponsibilitySubjectProductRole','MedicinalProduct'),
 ('InstitutionalFundingCommitment','PayerFundingOrganizationRole','Organization','InstitutionallyFundedOrganizationRole','Organization'),
]
def prop(name,slot):return name[0].lower()+name[1:]+slot.title()
def copygraph(g):
 n=Graph()
 for t in g:n.add(t)
 return n
def build():
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'lab').mkdir(exist_ok=True)
 old=Graph().parse(BASE/'active.ttl');g=copygraph(old);oldclasses=set(g.subjects(RDF.type,OWL.Class))
 native=json.loads((BASE/'ontouml.json').read_text());elements=native['elements'];pack=next(e for e in elements if e['id']==native['root'])
 def add(e):elements.append(e);pack['contents'].append(e['id'])
 def cls(name,st,parent=None):
  if CM[name] in oldclasses:return
  g.add((CM[name],RDF.type,OWL.Class));g.add((CM[name],META.ontoumlStereotype,Literal(st)))
  e=m.named(name,'Class');e.update(stereotype=st.lower(),isDerived=False,isAbstract=False,properties=[],literals=[],restrictedTo=[],isPowertype=False,order='1');add(e)
  if parent:
   g.add((CM[name],RDFS.subClassOf,CM[parent]));e=m.named('gen-'+name+'-'+parent,'Generalization');e.update(general=parent,specific=name);add(e)
 profiles={}
 for rel,holder,kind,other,otherkind in ROWS:
  cls(rel,'Relator');cls(holder,'Role','ProductResponsibleLabelerRole' if holder=='ProductLabelCommitmentOrganizationRole' else kind);cls(other,'Role',otherkind)
  slots={}
  for slot,target,k in [('holder',holder,kind),('counterpart',other,otherkind)]:
   p=prop(rel,slot);slots[slot]=m.slot(p,target,k)
   g.add((CM[p],RDF.type,OWL.ObjectProperty));g.add((CM[p],RDFS.domain,CM[rel]));g.add((CM[p],RDFS.range,CM[target]))
   m.restriction(g,rel,p,OWL.qualifiedCardinality,1,target);m.restriction(g,target,p,OWL.minQualifiedCardinality,1,rel,inverse=True)
   e=m.named('rel-'+p,'BinaryRelation',p);e.update(stereotype='mediation',isDerived=False,isAbstract=False,properties=['end-'+p+'-source','end-'+p+'-target']);add(e)
   for side,typ,card in [('source',rel,'1..*'),('target',target,'1')]:
    e=m.named('end-'+p+'-'+side,'Property');e.update(stereotype=None,isDerived=False,subsettedProperties=[],redefinedProperties=[],aggregationKind='NONE',cardinality=card,isOrdered=False,isReadOnly=side=='target',propertyType=typ);add(e)
  g.add((CM[prop(rel,'holder')],OWL.propertyDisjointWith,CM[prop(rel,'counterpart')]))
  profiles[rel]=slots
 # Alternative dependencies for the broader product role: preserve existing listing route.
 union=BNode();members=BNode();g.add((union,RDF.type,OWL.Class));g.add((union,OWL.unionOf,members));Collection(g,members,[CM.ListingResponsibleOrganizationRole,CM.ProductLabelCommitmentOrganizationRole]);g.add((CM.ProductResponsibleLabelerRole,OWL.equivalentClass,union))
 e=m.named('gs-product-responsibility-routes','GeneralizationSet');e.update(isDisjoint=False,isComplete=True,generalizations=['gen-ListingResponsibleOrganizationRole-ProductResponsibleLabelerRole','gen-ProductLabelCommitmentOrganizationRole-ProductResponsibleLabelerRole'],categorizer=None);add(e)
 e=m.named('g3d-scope-note','Note');e['text']={'en':'Candidate implementation authorized by the user request to continue, 2026-10-07 Asia/Tehran. Final scientific sign-off pending. Funding is institutional-only; product responsibility has two overlapping routes. Temporal admission and evidence provenance are separate from OWL structural dependence.'};add(e)
 for c in g.subjects(RDF.type,OWL.Class):g.set((c,META.conceptualModelVersion,Literal(OUT.name)))
 for ont in g.subjects(RDF.type,OWL.Ontology):
  g.set((ont,OWL.versionInfo,Literal(OUT.name)));g.set((ont,OWL.versionIRI,URIRef(str(CM)+OUT.name)));g.set((ont,META.formalizationStatus,Literal('G3d nine recommended role definitions implemented in a review candidate; final scientific and release approval pending')))
 native['id']='cm-pharme-g3d';native['name']={'en':'CM-PharmE nine-role integrated review candidate'}
 for e in elements:
  if e['id'].startswith(('g3d-','gs-product-responsibility')) or e['id'] not in {x['id'] for x in json.loads((BASE/'ontouml.json').read_text())['elements']}:e['created']='2026-10-07'
 schema=json.loads((ROOT/'tools/v2_ontology/vendor/ontouml-schema.json').read_text());v=Draft202012Validator(schema,format_checker=FormatChecker());errors=list(v.iter_errors(native))
 for e in elements:errors+=list(v.iter_errors(e))
 assert not errors,[e.message for e in errors[:5]]
 ids={e['id'] for e in elements};assert len(ids)==len(elements)
 for e in elements:
  for k in ['general','specific','propertyType']:
   if e.get(k) is not None:assert e[k] in ids
  for k in ['properties','contents','generalizations','subsettedProperties']:assert all(x in ids for x in e.get(k,[]))
 g.bind('cmpe',CM);g.serialize(OUT/'active.ttl',format='turtle');m.write_json(OUT/'ontouml.json',native)
 registry=json.loads((BASE/'conceptual-model.json').read_text());registry['version']=OUT.name
 for c in sorted({x for x in g.subjects(RDF.type,OWL.Class) if isinstance(x,URIRef)}-oldclasses,key=str):registry['concepts'].append(dict(id=str(c).split('/')[-1],iri=str(c),stereotype=str(g.value(c,META.ontoumlStereotype)),parents=[str(x).split('/')[-1] for x in g.objects(c,RDFS.subClassOf) if isinstance(x,URIRef)],origin='G3d recommended implementation; final scientific review pending'))
 registry['g3_product_covering_set']=dict(complete=True,disjoint=False,scope='two admitted responsibility routes in this candidate')
 m.write_json(OUT/'conceptual-model.json',registry)
 contract=json.loads((BASE/'contract.json').read_text());contract['version']=OUT.name;contract['g3_profiles']=profiles;contract['g3_scope']='Institutional funding only; no person entitlement. Product role is inclusive union of two routes. No scope-only authorization implies responsibility.';m.write_json(OUT/'contract.json',contract)
 decisions=json.loads((ROOT/'v2/research/w4/g3-1c-institutional-patterns/nine-role-decisions.json').read_text())
 decisions.update(status='IMPLEMENTED_FOR_REVIEW',implementation_authorization='User instruction to proceed after the nine-decision table, 2026-10-07T00:45:47+03:30; not explicit final scientific approval',approved=0,integrated=9)
 for d in decisions['decisions']:d['integration']='IMPLEMENTED_IN_G3D_CANDIDATE';d['author_decision']='FINAL_SCIENTIFIC_REVIEW_PENDING'
 m.write_json(OUT/'decisions.json',decisions)
 s=Graph().parse(BASE/'constraints.ttl')
 original=m.PROFILES;m.PROFILES=profiles
 try:new=m.make_shapes(g)
 finally:m.PROFILES=original
 # Reuse only the new role/relator constraints; inherited shape definitions are kept intact.
 for t in new:s.add(t)
 # Explicit complete-instance OR: the parent must be supported by at least one route.
 node=CM.ProductResponsibleLabelerRoleGroundingShape;s.add((node,RDF.type,SH.NodeShape));s.add((node,SH.targetClass,CM.ProductResponsibleLabelerRole))
 options=[]
 for name,p,rel in [('listing','listingResponsibleOrganization','MarketListing'),('commitment',prop('ProductLabelResponsibility','holder'),'ProductLabelResponsibility')]:
  shape=BNode();pnode=BNode();path=BNode();s.add((shape,SH.property,pnode));s.add((pnode,SH.path,path));s.add((path,SH.inversePath,CM[p]));s.add((pnode,SH.minCount,Literal(1)));s.add((pnode,SH['class'],CM[rel]));options.append(shape)
 head=BNode();Collection(s,head,options);s.add((node,SH['or'],head));s.serialize(OUT/'constraints.ttl',format='turtle')
 kinds=set(g.subjects(META.ontoumlStereotype,Literal('Kind')));checks=[]
 for r in decisions['decisions']:
  found=audit.ancestors(g,CM[r['role']])&kinds;checks.append(dict(role=r['role'],identity_providers=[str(x).split('/')[-1] for x in found],passed=found=={CM[r['identity']]}))
 assert all(x['passed'] for x in checks)
 assert all(p in {OWL.versionInfo,OWL.versionIRI,META.formalizationStatus,META.conceptualModelVersion} for _,p,_ in set(old)-set(g))
 report=dict(classes=len({x for x in g.subjects(RDF.type,OWL.Class) if isinstance(x,URIRef)}),datatypes=6,concepts=len(registry['concepts']),object_properties=len(set(g.subjects(RDF.type,OWL.ObjectProperty))),added_relators=9,added_roles=10,added_mediations=18,schema_errors=0,native_elements=len(elements),identity_checks=checks,unresolved_prior_relation_records=42,new_mediations_typed=18,official_antipattern_engine='NOT_RUN',full_conformance='NOT_ESTABLISHED',topology_before=audit.topology(old),topology_after=audit.topology(g))
 m.write_json(OUT/'model-validation.json',report);return g,s,profiles

def witness(row,prefix):
 rel,role,kind,other,otherkind=row;g=Graph();r=LAB[prefix+'-r'];a=LAB[prefix+'-holder'];b=LAB[prefix+'-counterpart']
 for node,types in [(r,[rel]),(a,[role,kind]),(b,[other,otherkind])]:
  for typ in types:g.add((node,RDF.type,CM[typ]))
 g.add((r,CM[prop(rel,'holder')],a));g.add((r,CM[prop(rel,'counterpart')],b));g.add((a,OWL.differentFrom,b));return g,r,a,b

def run_tests(g,s):
 cases=[];positive=Graph()
 def check(id,data,expected):
  yes,_,detail=validate(data,shacl_graph=s,ont_graph=g,inference='none',advanced=True)
  cases.append(dict(id=id,expected=expected,conforms=bool(yes),passed=bool(yes)==expected))
  if bool(yes)!=expected:print(id,detail[:3000],flush=True)
 for row in ROWS:
  rel,role,kind,other,otherkind=row;f,r,a,b=witness(row,rel)
  check(rel+'/valid',f,True)
  for t in f:positive.add(t)
  for slot in ['holder','counterpart']:
   bad=copygraph(f);bad.remove((r,CM[prop(rel,slot)],None));check(rel+'/missing-'+slot,bad,False)
  bad=copygraph(f);bad.remove((r,CM[prop(rel,'counterpart')],None));bad.add((r,CM[prop(rel,'counterpart')],a));bad.add((a,RDF.type,CM[other]));check(rel+'/same-relatum',bad,False)
  bad=copygraph(f);bad.add((r,CM[prop(rel,'counterpart')],LAB['extra']));bad.add((LAB['extra'],RDF.type,CM[other]));check(rel+'/too-many-counterparts',bad,False)
  bad=copygraph(f);bad.remove((b,RDF.type,CM[other]));bad.remove((b,RDF.type,CM[otherkind]));bad.add((b,RDF.type,CM.SourceRecord));check(rel+'/wrong-counterpart',bad,False)
  bare=Graph();bare.add((a,RDF.type,CM[role]));bare.add((a,RDF.type,CM[kind]));check(rel+'/bare-role',bare,False)
 # The listing route must not acquire a mandatory separate product commitment.
 listing=Graph();r=LAB.listing;a=LAB.listingActor;b=LAB.presentation
 for x,typ in [(r,'MarketListing'),(a,'ListingResponsibleOrganizationRole'),(a,'Organization'),(b,'ListedPresentationRole'),(b,'MedicinalProductPresentation')]:listing.add((x,RDF.type,CM[typ]))
 listing.add((r,CM.listingResponsibleOrganization,a));listing.add((r,CM.listingPresentation,b));check('product/listing-only',listing,True)
 both=copygraph(listing);f,rr,aa,bb=witness(ROWS[7],'product-both')
 for x,p,y in f:both.add((a if x==aa else x,p,a if y==aa else y))
 check('product/both-routes',both,True)
 for t in listing:positive.add(t)
 bare=Graph();bare.add((LAB.bare,RDF.type,CM.ProductResponsibleLabelerRole));check('product/neither-route',bare,False)
 # Explicitly demonstrate the required migration of old complete-instance authority examples.
 migration=[]
 for oldprofile in ['RegulatoryAuthorization','EstablishmentRegistration','RegulatoryOversight']:
  db=lab.database(lab.template(oldprofile));f=lab.rdf_export(db,g);db.close()
  check('migration/'+oldprofile+'/missing-mandate',f,False)
  authority=lab.LAB.authority0
  extra,r,a,b=witness(ROWS[6],oldprofile+'-mandate')
  for x,p,y in extra:f.add((authority if x==a else x,p,authority if y==a else y))
  check('migration/'+oldprofile+'/explicit-synthetic-mandate',f,True)
  migration.append(dict(profile=oldprofile,old_fixture='Fails new mandate completeness requirement',candidate_fixture='Passes with an explicitly added synthetic mandate; not inferred from issuing an act'))
 # Counterexamples retained under new OWL: all twelve unwanted entailments remain testable.
 counters=Graph().parse(BASE/'lab/non-entailment-witnesses.ttl')
 data=copygraph(g)
 for source in [positive,counters]:
  for t in source:data.add(t)
 positive.serialize(OUT/'lab/new-positive-witnesses.ttl',format='turtle');data.serialize(OUT/'lab/reasoner-input.rdf',format='xml')
 m.write_json(OUT/'lab/integration-tests.json',cases);m.write_json(OUT/'lab/authority-migration.json',migration)
 assert all(x['passed'] for x in cases)
 return cases

def negative_reasoner_tests(g):
 """Check actual inconsistent models, not SHACL failures interpreted as OWL failures."""
 negatives={}
 f=copygraph(g);a=LAB.noResponsibility;f.add((a,RDF.type,CM.ManufacturerRole))
 restriction=BNode();path=BNode();f.add((a,RDF.type,restriction));f.add((restriction,RDF.type,OWL.Restriction));f.add((restriction,OWL.onProperty,path));f.add((path,OWL.inverseOf,CM.manufacturingResponsibilityHolder));f.add((restriction,OWL.maxQualifiedCardinality,Literal(0,datatype=XSD.nonNegativeInteger)));f.add((restriction,OWL.onClass,CM.ManufacturingResponsibility));negatives['role-explicitly-without-dependence']=f
 f=copygraph(g);a=LAB.noProductRoute;f.add((a,RDF.type,CM.ProductResponsibleLabelerRole))
 for role in ['ListingResponsibleOrganizationRole','ProductLabelCommitmentOrganizationRole']:
  n=BNode();f.add((n,RDF.type,OWL.Class));f.add((n,OWL.complementOf,CM[role]));f.add((a,RDF.type,n))
 negatives['product-parent-outside-both-routes']=f
 f=copygraph(g);r=LAB.selfMandate;a=LAB.selfAuthority
 f.add((r,RDF.type,CM.RegulatoryMandate));f.add((r,CM.regulatoryMandateHolder,a));f.add((r,CM.regulatoryMandateCounterpart,a));negatives['self-mediation']=f
 f=copygraph(g);r=LAB.twoFundedOrganizations;a=LAB.fundedA;b=LAB.fundedB
 f.add((r,RDF.type,CM.InstitutionalFundingCommitment));f.add((r,CM.institutionalFundingCommitmentCounterpart,a));f.add((r,CM.institutionalFundingCommitmentCounterpart,b));f.add((a,OWL.differentFrom,b));negatives['two-distinct-counterparts-in-exact-one-assignment']=f
 results=[];jars=list((Path(owlready2.__path__[0])/'pellet').glob('*.jar'));cp=':'.join(map(str,jars))
 for name,f in negatives.items():
  path=OUT/'lab'/('negative-'+name+'.rdf');f.serialize(path,format='xml');world=owlready2.World();caught=False
  try:
   world.get_ontology(path.as_uri()).load();owlready2.sync_reasoner(world,debug=0)
  except owlready2.OwlReadyInconsistentOntologyError:caught=True
  finally:world.close()
  run=subprocess.run(['java','-cp',cp,str(ROOT/'tools/v2_ontology/CheckOWL2DL.java'),str(path)],capture_output=True,text=True)
  pellet=run.returncode==2 and 'CONSISTENT=false' in run.stdout and 'IN_OWL2_DL=true' in run.stdout
  results.append(dict(case=name,hermit_rejected=caught,pellet_rejected=pellet,pellet_details=run.stdout,passed=caught and pellet))
  print(json.dumps(results[-1]),flush=True)
 m.write_json(OUT/'lab/negative-reasoner-tests.json',results);assert all(r['passed'] for r in results)
 return results

def main():
 baseline={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.iterdir() if p.is_file()}
 g,s,profiles=build();cases=run_tests(g,s)
 # Preserve the old 120-case contract regression as a separately labeled gate.
 # Its old shapes are intentional: new authority migration is tested above.
 old_out=lab.OUT;old_dest=lab.DEST
 lab.OUT=OUT;lab.DEST=OUT/'lab/legacy-contract';lab.DEST.mkdir(exist_ok=True)
 # shapes() reads OUT/constraints.ttl, so replay with explicit legacy shape monkey-patch.
 original_shapes=lab.shapes
 lab.shapes=lambda: Graph().parse(BASE/'lab/admission-shapes.ttl')
 try:lab.main()
 finally:lab.OUT=old_out;lab.DEST=old_dest;lab.shapes=original_shapes
 g2.OUT=OUT;bridges,_=g2.check_bridges(g,s)
 nhif=Graph().parse(BASE.parent/'2.1.0-alpha.1-g2-candidate/lab/nhif-candidate-projection.ttl');ok,_,_=validate(nhif,shacl_graph=s,ont_graph=g,inference='none',advanced=True);assert ok
 reasoners.OUT=OUT;reasoners.main()
 r=json.loads((OUT/'reasoner-results.json').read_text());r['scope']='G3d schema and nine new Relator witnesses, existing listing alternative, and twelve retained non-entailment countermodels; not official OntoUML validation.';m.write_json(OUT/'reasoner-results.json',r)
 negative=negative_reasoner_tests(g)
 assert baseline=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.iterdir() if p.is_file()}
 result=dict(new_integration_cases=len(cases),new_integration_passed=sum(x['passed'] for x in cases),negative_owl_cases_rejected_by_both_engines=len(negative),legacy_contract_cases=120,legacy_contract_scope='old completeness contract under new ontology; mandate migration is a separate six-case test',g2_bridge_passed=sum(x['passed'] for x in bridges),existing_nhif_shacl_passed=True,retained_non_entailment_countermodels=12,implemented_inherited_definitions=9,final_scientific_approval=False,prior_snapshot_unchanged=True,official_antipattern_engine='NOT_RUN')
 m.write_json(OUT/'results.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
