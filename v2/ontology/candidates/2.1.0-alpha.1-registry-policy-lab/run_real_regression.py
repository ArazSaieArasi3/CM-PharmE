"""Nonregression on the existing pinned real sample, not new-domain validation."""
import base64,gzip,hashlib,tempfile
from pyshacl import validate
from owlready2 import World,sync_reasoner
from owlready2.base import OwlReadyInconsistentOntologyError
from lab import *
encoded=H.parent/'2.1.0-alpha.1-g3-3-d-real-source-migration/real-source-abox.nt.gz.b64'
raw=gzip.decompress(base64.b64decode(encoded.read_text()));g=Graph().parse(data=raw.decode(),format='nt')
ok,report,_=validate(g+hierarchy,shacl_graph=base_shapes+shapes(),advanced=True,inference='none')
violations=[{'focus':str(report.value(x,SH.focusNode) or ''),'path':str(report.value(x,SH.resultPath) or ''),'constraint':str(report.value(x,SH.sourceConstraint) or '')} for x in report.subjects(RDF.type,SH.ValidationResult)]
with tempfile.TemporaryDirectory() as td:
 f=Path(td)/'model.rdf';(ontology+delta()+g).serialize(f,format='xml');w=World();w.get_ontology(f.as_uri()).load()
 try:sync_reasoner(w,debug=0);consistent=True;unsat=[x.iri for x in w.inconsistent_classes() if x.iri!=str(OWL.Nothing)]
 except OwlReadyInconsistentOntologyError:consistent=False;unsat=[]
 finally:w.close()
out={'source':str(encoded.relative_to(H.parent)),'source_sha256':hashlib.sha256(raw).hexdigest(),'rows':768,'triples':len(g),
 'new_profile_witnesses':len(list(g.triples((None,P.profile,None)))),'shacl_conforms':bool(ok),'violations':violations,
 'hermit_consistent':consistent,'unsatisfiable_named_classes':unsat,'pass':bool(ok) and consistent and not unsat,
 'claim_limit':'Previously migrated real sample, nonregression only. Zero new registry/ESMP/PROV profile witnesses; no new empirical dataset ingestion.'}
write('real-regression.json',out);print(json.dumps(out),flush=True);assert out['pass']
