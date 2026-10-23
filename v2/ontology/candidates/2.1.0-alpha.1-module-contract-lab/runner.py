"""Portable bounded module runner: this file requires only its own directory.

Run: python runner.py. Dependencies: rdflib 7.6.0, pyshacl 0.30.1,
owlready2 0.49 and Java 17. No network imports or sibling lab imports.
"""
from pathlib import Path
import json, tempfile, subprocess, platform
from rdflib import Graph, RDF, RDFS, OWL, Namespace
from rdflib.compare import isomorphic
from pyshacl import validate
from owlready2.reasoning import _HERMIT_CLASSPATH
H=Path(__file__).resolve().parent
SH=Namespace('http://www.w3.org/ns/shacl#')
def reason(g):
 with tempfile.TemporaryDirectory() as td:
  f=Path(td)/'input.rdf';g.serialize(f,format='xml')
  assert isomorphic(g,Graph().parse(f,format='xml'))
  p=subprocess.run(['java','-Xmx1200M','-cp',_HERMIT_CLASSPATH,'org.semanticweb.HermiT.cli.CommandLine','-U',f.as_uri()],capture_output=True,text=True,timeout=90)
  out=p.stdout+'\n'+p.stderr
  if p.returncode==0:
   assert "Classes equivalent to 'owl:Nothing':" in p.stdout,out
   return {'consistent':True,'unsatisfiable_named_classes':[s.strip().strip('<>') for s in p.stdout.splitlines() if s.startswith('\t') and s.strip()!='owl:Nothing']}
  if 'Inconsistent ontology' in out:return {'consistent':False,'unsatisfiable_named_classes':[]}
  raise RuntimeError(out)
def main():
 schema=Graph().parse(H/'ontology.ttl');shapes=Graph().parse(H/'shapes.ttl');hier=Graph().parse(H/'hierarchy.ttl')
 assert not list(schema.triples((None,OWL.imports,None)))
 contract=json.loads((H/'contract.json').read_text());results=[]
 for case in contract['admission_cases']:
  g=Graph().parse(H/case['fixture']);ok,report,_=validate(g+hier,shacl_graph=shapes,advanced=True,inference='none')
  violations=[{'path':str(report.value(x,SH.resultPath) or ''),'constraint':str(report.value(x,SH.sourceConstraint) or ''),'component':str(report.value(x,SH.sourceConstraintComponent) or '')} for x in report.subjects(RDF.type,SH.ValidationResult)]
  marker=case.get('marker');passed=bool(ok)==case['expected'] and (marker is None or any(marker in str(v) for v in violations))
  results.append({'id':case['id'],'conforms':bool(ok),'pass':passed,'violations':violations})
 queries=[]
 for q in contract['queries']:
  g=Graph().parse(H/q['fixture']);rows=sorted([[str(v) for v in row] for row in g.query(q['query'])])
  queries.append({'id':q['id'],'actual':rows,'pass':rows==q['expected']})
 logical=[]
 for case in contract['reasoner_cases']:
  g=schema+(Graph().parse(H/case['fixture']) if case.get('fixture') else Graph());r=reason(g)
  logical.append({'id':case['id'],**r,'pass':r['consistent']==case['expected'] and not r['unsatisfiable_named_classes']})
 lookups=[]
 if contract.get('source_scope_lookups'):
  from pv_group import lookup
  data=json.loads((H/'pv-group-source.json').read_text())
  for case in contract['source_scope_lookups']:
   actual=lookup(data,**case['input']);lookups.append({'id':case['id'],'actual':actual,'pass':actual==case['expected']})
 result={'module':contract['module'],'scope':'bounded regression; not full semantic acceptance or a formal locality module','admission':results,'queries':queries,'reasoner':logical,'source_scope_lookups':lookups,'counts':{'admission':[sum(x['pass'] for x in results),len(results)],'queries':[sum(x['pass'] for x in queries),len(queries)],'reasoner':[sum(x['pass'] for x in logical),len(logical)],'source_scope_lookups':[sum(x['pass'] for x in lookups),len(lookups)]},'runtime':{'python':platform.python_version(),'rdflib':__import__('rdflib').__version__,'pyshacl':__import__('pyshacl').__version__,'owlready2':__import__('owlready2').VERSION}}
 (H/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'module':contract['module'],'counts':result['counts']}),flush=True)
 assert all(x['pass'] for x in results+queries+logical+lookups)
if __name__=='__main__':main()
