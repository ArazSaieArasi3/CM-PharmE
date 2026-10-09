"""Isolated proposal laboratory; never mutates the native/baseline ontology."""
from pathlib import Path
import importlib.util, json, hashlib, tempfile, subprocess, re
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, OWL, XSD
from rdflib.collection import Collection
from pyshacl import validate
from owlready2.reasoning import _HERMIT_CLASSPATH
from rdflib.compare import isomorphic
H = Path(__file__).resolve().parent
REG = H.parent/'2.1.0-alpha.1-registry-policy-lab'
spec = importlib.util.spec_from_file_location('registry_lab', REG/'lab.py')
reg = importlib.util.module_from_spec(spec); spec.loader.exec_module(reg)
C,L,R,P,PROV,SH = reg.C,reg.L,reg.R,reg.P,reg.PROV,reg.SH
Q = Namespace('https://w3id.org/cm-pharme/experimental/prov-target/')
T = Namespace('urn:cmpe-prov-target:')
raw_prov = Graph().parse(H/'sources/prov-o-20130430.ttl')
# Explicit, reviewable DL-oriented projection. The downloaded source declares
# these two IRIs as BOTH object and annotation properties. Raw HermiT silently
# misses the revision -> derivation probe. Never overwrite that source or hide
# the initial failing result; retain every other triple including header metadata.
prov = raw_prov+Graph()
for prop in [PROV.wasRevisionOf,PROV.specializationOf]:
 assert (prop,RDF.type,OWL.ObjectProperty) in prov
 assert (prop,RDF.type,OWL.AnnotationProperty) in prov
 prov.remove((prop,RDF.type,OWL.AnnotationProperty))
assert len(raw_prov-prov)==2 and len(prov-raw_prov)==0
alignment = Graph().parse(H/'proposed-alignment.ttl')
base = reg.ontology
full = base+prov+alignment
def write(name,data):
 p=H/name;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def save(name,g):
 p=H/name;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(g.serialize(format='turtle').rstrip()+'\n')
def graph():
 g=reg.graph();g.bind('q',Q);g.bind('t',T);return g
def typ(g,n,c):g.add((n,RDF.type,c))
def not_type(g,n,c):
 b=BNode();typ(g,b,OWL.Class);g.add((b,OWL.complementOf,c));typ(g,n,b)
def not_edge(g,s,p,o):
 b=BNode();typ(g,b,OWL.NegativePropertyAssertion)
 g.add((b,OWL.sourceIndividual,s));g.add((b,OWL.assertionProperty,p));g.add((b,OWL.targetIndividual,o))
def hermit(g):
 with tempfile.TemporaryDirectory() as td:
  f=Path(td)/'model.rdf';g.serialize(f,format='xml')
  assert isomorphic(g,Graph().parse(f,format='xml'))
  run=subprocess.run(['java','-Xmx1600M','-cp',_HERMIT_CLASSPATH,
   'org.semanticweb.HermiT.cli.CommandLine','-U',f.as_uri()],capture_output=True,text=True,timeout=90)
  out=run.stdout+'\n'+run.stderr
  if run.returncode==0:
   ok=True;unsat=[x.strip().strip('<>') for x in run.stdout.splitlines() if x.startswith('\t') and x.strip()!='owl:Nothing']
   assert "Classes equivalent to 'owl:Nothing':" in run.stdout, out
  elif 'Inconsistent ontology' in out:ok=False;unsat=[]
  else:raise RuntimeError(out)
 return {'consistent':ok,'unsatisfiable_named_classes':unsat,'engine':'direct HermiT CLI/OWLAPI; RDF/XML graph-isomorphism checked','prov_profile':'two conflicting annotation-property declarations removed; raw source retained'}
def shacl(g,extra=None):
 hierarchy=reg.hierarchy+Graph()
 for a,b in alignment.subject_objects(RDFS.subClassOf):hierarchy.add((a,RDFS.subClassOf,b))
 ok,r,_=validate(g+hierarchy,shacl_graph=reg.base_shapes+reg.shapes()+(extra or Graph()),advanced=True,inference='none')
 return {'conforms':bool(ok),'violations':[{'path':str(r.value(x,SH.resultPath) or ''),'constraint':str(r.value(x,SH.sourceConstraint) or ''),'component':str(r.value(x,SH.sourceConstraintComponent) or '')} for x in r.subjects(RDF.type,SH.ValidationResult)]}
