"""Run HermiT on the full mapped real-source ABox plus G3-P4a TBox."""
import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from rdflib import Graph, Namespace, RDF
from owlready2 import World, sync_reasoner
from owlready2.entity import OwlReadyInconsistentOntologyError

owl_path, abox_path, output = map(Path, sys.argv[1:4])
CM=Namespace('https://w3id.org/cm-pharme/2.1/')
tbox=Graph().parse(owl_path,format='turtle')
abox=Graph().parse(abox_path,format='nt')
assert len(tbox)>1598 and len(abox)==39272
assert not any(str(x).endswith('productHasActiveSubstance') for _,x,_ in abox)
named_subjects={s for s,p,o in abox.triples((None,RDF.type,None)) if str(o).startswith(str(CM))}

def run(data):
    with TemporaryDirectory() as d:
        path=Path(d)/'combined.rdf'
        (tbox+data).serialize(destination=path,format='xml')
        world=World();world.get_ontology(path.as_uri()).load()
        try:
            sync_reasoner(world,debug=0)
            inconsistent=False
        except OwlReadyInconsistentOntologyError:
            inconsistent=True
        unsats=[] if inconsistent else sorted(str(c.iri) for c in world.inconsistent_classes()
            if str(c.iri)!='http://www.w3.org/2002/07/owl#Nothing')
        return {"inconsistent":inconsistent,"unsatisfiable_named_classes":unsats,"imported_named_classes":len(list(world.classes()))}

positive=run(abox)
assert not positive['inconsistent'] and not positive['unsatisfiable_named_classes'] and positive['imported_named_classes']==138
product=next(s for s,p,o in abox.triples((None,RDF.type,CM.MedicinalProduct)))
mutated=Graph();mutated+=abox;mutated.add((product,RDF.type,CM.MedicinalProductPresentation))
negative=run(mutated)
assert negative['inconsistent']
result={"tool":"HermiT bundled with Owlready2 0.49","scope":"Full 768-row real-source ABox with G3-P4a OWL TBox; one injected contradiction checks sensitivity",
        "input":{"owl_triples":len(tbox),"abox_triples":len(abox),"typed_named_abox_subjects":len(named_subjects),
                 "owl_sha256":hashlib.sha256(owl_path.read_bytes()).hexdigest(),
                 "abox_sha256":hashlib.sha256(abox_path.read_bytes()).hexdigest()},
        "positive":{"expected_consistent":True,**positive,"pass":not positive['inconsistent'] and not positive['unsatisfiable_named_classes']},
        "negative":{"injection":"Assert one actual mapped MedicinalProduct also as disjoint MedicinalProductPresentation",
                    "expected_inconsistent":True,**negative,"pass":negative['inconsistent']},
        "limits":"Consistency does not establish correctness of source identity, classification, missing values, current uniqueness or complete dataset coverage."}
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({"full_abox_consistent":result['positive']['pass'],"contradiction_rejected":result['negative']['pass'],
                  "typed_subjects":len(named_subjects)}))
