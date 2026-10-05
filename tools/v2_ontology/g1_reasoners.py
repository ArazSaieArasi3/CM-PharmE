#!/usr/bin/env python3
"""Two independent reasoner engines and OWLAPI profile, with positive witnesses."""
import json, subprocess, tempfile, hashlib
from pathlib import Path
import owlready2
from rdflib import Graph, RDF, OWL
from g1_model import ROOT, OUT, write_json

def main():
    graph=Graph().parse(OUT/'active.ttl');graph.serialize(OUT/'lab/schema-only.rdf',format='xml')
    results=[]
    for name,fn in [('HermiT',owlready2.sync_reasoner)]:
        for artifact in ['schema-only.rdf','reasoner-input.rdf']:
            path=OUT/'lab'/artifact;world=owlready2.World()
            try:
                world.get_ontology(path.as_uri()).load()
                fn(world,debug=0)
                unsat=sorted(str(x.iri) for x in world.inconsistent_classes() if x!=owlready2.Nothing)
                result=dict(engine=name,input=artifact,consistent=True,unsatisfiable_named_classes=unsat,status='PASS' if not unsat else 'FAIL')
            except Exception as e:
                result=dict(engine=name,input=artifact,status='ERROR',error_type=type(e).__name__,message=str(e))
            results.append(result);print(json.dumps(result),flush=True);world.close()
    jars=list((Path(owlready2.__path__[0])/'pellet').glob('*.jar'));cp=':'.join(map(str,jars))
    for artifact in ['schema-only.rdf','reasoner-input.rdf']:
        run=subprocess.run(['java','-cp',cp,str(ROOT/'tools/v2_ontology/CheckOWL2DL.java'),str(OUT/'lab'/artifact)],capture_output=True,text=True)
        result=dict(engine='Pellet 2.3.1 through OWLAPIv3',input=artifact,status='PASS' if run.returncode==0 and 'CONSISTENT=true' in run.stdout and 'UNSAT_CLASSES=0' in run.stdout else 'FAIL',details=run.stdout,stderr=run.stderr)
        results.append(result);print(json.dumps(result),flush=True)
    profile=dict(status='PASS' if all('IN_OWL2_DL=true' in r.get('details','') for r in results if r['engine'].startswith('Pellet')) else 'FAIL',engine='OWLAPI 3.4.3 bundled with Owlready2 0.50',scope='schema and positive synthetic witnesses')
    report=dict(owlready2_version=owlready2.VERSION,java=subprocess.run(['java','-version'],capture_output=True,text=True).stderr,inputs={name:hashlib.sha256((OUT/'lab'/name).read_bytes()).hexdigest() for name in ['schema-only.rdf','reasoner-input.rdf']},reasoners=results,owl2_dl_profile=profile,execution_note='Owlready2 Pellet/Jena wrapper initially could not start on Java 17 because its bundled Jena parser requires Java 25. Re-run uses the supported Pellet OWLAPIv3 loader directly; no jar patch and no ignored ontology axiom.',scope='Schema and 12 synthetic profile witnesses. No claim about all possible instances, full source mappings, modal OntoUML semantics or complete catalogue conformance.')
    write_json(OUT/'reasoner-results.json',report);print(json.dumps(profile,indent=2))
    assert all(r['status']=='PASS' for r in results) and profile['status']=='PASS'

if __name__=='__main__':main()
