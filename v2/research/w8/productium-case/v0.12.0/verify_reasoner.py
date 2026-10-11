"""Validate a bounded native CM-PharmE logical population, with a negative control."""
import subprocess,os,json
from rdflib import Graph,RDF,OWL,URIRef
import integrate_case as m
jar=__import__('pathlib').Path(os.environ.get('ROBOT_JAR','/tmp/product-orsd-robot-1.9.11.jar'))
assert m.sha(jar)=='53cd275c8e4c0dad1fc2c1c34174876795cd7d6b6926e1444adcbb0cb3c7ab26'
ont=Graph().parse(m.I/'2.1.0-alpha.1-candidate/active.ttl')
population=Graph().parse(m.R/'generated/native-logical-population.nt',format='nt');out=[]
for name,negative in [('cm-source-population',False),('cm-product-organization-collision',True)]:
 g=Graph();g+=ont;g+=population
 if negative:g.add((m.Q['source-product-76162-741'],RDF.type,m.C.Organization))
 src=m.R/'results'/f'{name}.owl';dst=m.R/'results'/f'{name}-reasoned.owl';g.serialize(src,format='xml')
 cmd=['java','-jar',str(jar),'reason','--input',str(src),'--reasoner','HermiT','--output',str(dst)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
 (m.R/'results'/f'{name}-hermit.log').write_text(p.stdout+'\n'+p.stderr)
 text=p.stdout+p.stderr;passed=p.returncode==0 if not negative else p.returncode!=0 and 'inconsistent' in text.lower()
 out.append({'name':name,'exit_code':p.returncode,'expectation_met':passed,'expected_consistent':not negative,'command':cmd})
m.write('results/HermiT_Tests_v0_12_0.json',{'version':'0.12.0','reasoner':'HermiT via ROBOT 1.9.11','logical_population_triples':len(population),'excluded_metadata_triples':138,'ontology_sha256':m.sha(m.I/'2.1.0-alpha.1-candidate/active.ttl'),'tests':out,'scope':'Pinned native CM-PharmE G1 candidate and declared population; PROV/experimental document metadata is retained separately. Not full upstream PROV alignment acceptance or an independent validity assessment.'})
assert all(x['expectation_met'] for x in out),out
print('HermiT positive and identity-collision control passed')
