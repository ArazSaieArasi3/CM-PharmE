"""Execute selected existing SHACL shapes with pySHACL; no new global axioms."""
import json
import sys
from pathlib import Path
from rdflib import BNode, Graph, Namespace, RDF, Literal, URIRef
from pyshacl import validate

CM=Namespace('https://w3id.org/cm-pharme/2.1/')
SH=Namespace('http://www.w3.org/ns/shacl#')
shapes_path,model_path,prefilter_path,result_path=map(Path,sys.argv[1:5])
all_shapes=Graph().parse(shapes_path,format='turtle')
model=json.loads(model_path.read_text())
byid={e['id']:e for e in model['elements']}
pref=json.loads(prefilter_path.read_text())['triggers']
def shape_for(name):
    shape=CM[name]
    assert (shape,RDF.type,SH.NodeShape) in all_shapes,name
    sub=Graph();queue=[shape];seen=set()
    while queue:
        subject=queue.pop()
        if subject in seen:continue
        seen.add(subject)
        for t in all_shapes.triples((subject,None,None)):
            sub.add(t)
            if isinstance(t[2],BNode):queue.append(t[2])
    return sub
def status(data,shapes):
    ok,report,_=validate(data_graph=data,shacl_graph=shapes,advanced=True,abort_on_first=False)
    paths=sorted(set(str(x) for x in report.objects(None,SH.resultPath)))
    return bool(ok),paths,len(list(report.subjects(RDF.type,SH.ValidationResult)))

geo=shape_for('GeographyShape')
geo_cases={}
def geo_case(name,triples,expected):
    g=Graph()
    for a,p,b in triples:g.add((CM[a],CM[p],CM[b]))
    result=status(g,geo)
    assert result[0]==expected,(name,result)
    geo_cases[name]={'conforms':result[0],'expected':expected,'validation_results':result[2]}
geo_case('valid_facility_country',[('facilityA','withinCountry','countryA')],True)
geo_case('valid_region_country',[('regionA','withinCountry','countryA')],True)
geo_case('self_country_rejected',[('countryA','withinCountry','countryA')],False)
geo_case('self_region_rejected',[('regionA','withinRegion','regionA')],False)
geo_case('two_step_cycle_rejected',[('regionA','withinRegion','regionB'),('regionB','withinRegion','regionA')],False)
geo_case('no_postal_label_inference',[],True)

relator_cases=[]
for item in pref['RepRel_direct']:
    rid=item['relator']
    s=shape_for(rid+'Shape')
    relations=[byid['rel-'+name] for name in item['mediations']]
    g=Graph()
    for x in ['r1','r2']:g.add((CM[x],RDF.type,CM[rid]))
    for index,r in enumerate(relations):
        target=byid[r['properties'][1]]['propertyType']
        assert target, rid
        party='party'+str(index)
        g.add((CM[party],RDF.type,CM[target]))
        for relator in ['r1','r2']:
            g.add((CM[relator],CM[r['name']['en']],CM[party]))
    for ps in s.objects(CM[rid+'Shape'],SH.property):
        path=s.value(ps,SH.path)
        if isinstance(path,URIRef) and s.value(ps,SH.datatype):
            for relator in ['r1','r2']:
                g.add((CM[relator],path,Literal('fixture-code',datatype=s.value(ps,SH.datatype))))
    pair=status(g,s)
    assert pair[0],(rid,pair)
    r=relations[0]
    g.remove((CM.r2,CM[r['name']['en']],CM.party0))
    missing=status(g,s)
    assert not missing[0],(rid,missing)
    relator_cases.append({'relator':rid,'mediation_names':item['mediations'],
                          'two_simultaneous_same_party_tuple_conforms_to_focal_shape':pair[0],
                          'missing_one_mediation_rejected_by_focal_shape':not missing[0],
                          'scope':'Focal relator SHACL shape only; no timing or full-graph uniqueness proof'})
out={'tool':'pySHACL','version':__import__('pyshacl').__version__,
     'shapes_source':'G3-2e-F candidate-shapes.ttl, selected existing NodeShapes only',
     'geography_cases':geo_cases,'repRel_cases':relator_cases,
     'counts':{'geo_passed':len(geo_cases),'relators_checked':len(relator_cases),
               'repeatable_tuple_allowed':sum(x['two_simultaneous_same_party_tuple_conforms_to_focal_shape'] for x in relator_cases),
               'missing_participant_rejected':sum(x['missing_one_mediation_rejected_by_focal_shape'] for x in relator_cases)},
     'qualification':'SHACL shape behavior under positive and negative synthetic fixtures; does not choose whether concurrent duplicates are domain-valid.'}
result_path.write_text(json.dumps(out,indent=2)+'\n')
print(out['counts'])
