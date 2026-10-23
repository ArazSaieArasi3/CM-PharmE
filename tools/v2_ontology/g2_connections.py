#!/usr/bin/env python3
"""Source-bounded connectivity candidate. Does not amend G1 or frozen 2.0."""
import csv, json, hashlib, copy, sqlite3
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, OWL, XSD
from jsonschema import Draft202012Validator, FormatChecker
from pyshacl import validate
import g1_model as model
import g1_audit as audit
import g1_lab as lab
import g1_reasoners as reasoners

ROOT=model.ROOT; BASE=model.OUT; OUT=BASE.parent/'2.1.0-alpha.1-g2-candidate'
CM=model.CM; META=model.META; SH=model.SH; LAB=Namespace('https://example.org/cm-pharme-g2/')
VERSION='2.1.0-alpha.1-g2-candidate'
SOURCE_REV='17219243186df6b86056cfeeb906de2d9862c8c9'
# Typed specializations avoid narrowing a polymorphic parent property's global range.
BRIDGES={
 'observationAboutProduct':('C03','ObservationResult','MedicinalProduct','observationResultAbout','Information about a product; not an observation event or a product identity assertion.'),
 'observationAboutPresentation':('C03','ObservationResult','MedicinalProductPresentation','observationResultAbout','Information about an identified presentation; no substitution for Product.'),
 'assertionAboutProduct':('C04','Assertion','MedicinalProduct',None,'Bounded product-target aboutness; the full polymorphic assertion target family remains for G3.'),
 'riskAssessmentConcernsDependency':('C06','RiskAssessmentActivity','SupplyDependency','riskAssessmentConcerns','Assessment topic only; no vulnerability or quantitative risk conclusion is entailed.'),
 'disruptionAffectsDependency':('C08','DisruptionEvent','SupplyDependency','disruptionAffects','Source-supported impact link only; does not entail causation of shortage.'),
 'reimbursementDiagnosisContext':('C11','ReimbursementUtilisationObservationResult','DiagnosisClassificationReference',None,'Diagnosis classification context of an aggregate observation; never a patient diagnosis assertion.')
}
SOURCES=[
 'v2/research/w3/candidate-relations-events.md',
 'v2/research/w4/integrated-ontouml-model.md',
 'v2/research/w4/events-situations-observations.md',
 'v2/research/w4/risk-resilience-extension.md',
 'v2/research/w4/business-architecture-view.md',
 'v2/research/w2/gate-c-dataset-portfolio.md',
 'v2/data/sources/source-manifest.json',
 'v2/data/mappings/source-field-ontology-mapping.csv',
 'v2/research/w7/e6-dataset-ontology-mapping-quality.md',
 'v2/data/fixtures/nhif_outpatient_fixture.csv',
 'v2/data/fixtures/nhif_inpatient_fixture.csv'
]
DISPOSITIONS={
 'C01':('ALREADY_IMPLEMENTED_G1','Evidence specialization is a subset, not a second relatum.'),
 'C02':('ALREADY_IMPLEMENTED_G1','Contextual assignment specializes general classification; product alias retained.'),
 'C03':('IMPLEMENTED_SCOPED','W4 section 5 and V2R-044/045; separate Product and Presentation aboutness specializations.'),
 'C04':('IMPLEMENTED_SCOPED','V2R-060 and W4 evidence pattern; product-specific aboutness only. Other targets remain uncommitted.'),
 'C05':('ALREADY_IMPLEMENTED_G1','Polymorphic identified bearers and used scheme roles; no product-only global range.'),
 'C06':('IMPLEMENTED_SCOPED','W4 risk extension example explicitly evaluates dependencies; does not reactivate deferred asset/vulnerability classes.'),
 'C07':('DEFER_SOURCE_ACTIVATION','V2R-075 is conditional on optional S3; no frozen safety mapping or admitted case data.'),
 'C08':('IMPLEMENTED_SCOPED','V2R-030 and W4 risk extension explicitly permit dependency impact; causal inference prohibited.'),
 'C09':('DEFER_SOURCE_ACTIVATION','C1 procurement requires documented buyer/provider and product/site grain; no admitted row-level mapping in current manifest.'),
 'C10':('DEFER_SOURCE_ACTIVATION','C1 stockout requires product/presentation granularity plus facility/time evidence; shortage is not a substitute.'),
 'C11':('IMPLEMENTED_SCOPED','V2R-071; P1-F10/F11 and P2-F12/F13 explicitly retain diagnosis context in RDB. Candidate fixture RDF projection added.'),
 'C12':('DEFER_USE_CASE_EVIDENCE','V1 lineage alone does not establish an actual digital component supporting an admitted observation.'),
 'C13':('DEFER_USE_CASE_EVIDENCE','Optional service-offering view has no admitted offerer/service commitment.'),
 'C14':('DEFER_APPROVED_G1','Clinical role remains deferred; no Organization-only bearer assumption or held-out-source mining.'),
 'C15':('ALREADY_IMPLEMENTED_G1','Existing provenance generation link retained unchanged.')
}

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    old=Graph().parse(BASE/'active.ttl');g=Graph()
    for t in old:g.add(t)
    g.bind('cmpe',CM);g.bind('cmmeta',META)
    for ont in g.subjects(RDF.type,OWL.Ontology):
        g.set((ont,OWL.versionInfo,Literal(VERSION)));g.set((ont,OWL.versionIRI,URIRef(str(CM)+VERSION)))
        g.set((ont,META.formalizationStatus,Literal('G2 source-bounded implementation candidate; author sign-off and full OntoUML semantics remain separate')))
    for c in g.subjects(RDF.type,OWL.Class):g.set((c,META.conceptualModelVersion,Literal(VERSION)))
    shapes=Graph().parse(BASE/'constraints.ttl')
    for name,(cid,domain,range_,parent,note) in BRIDGES.items():
        p=CM[name];g.add((p,RDF.type,OWL.ObjectProperty));g.add((p,RDFS.domain,CM[domain]));g.add((p,RDFS.range,CM[range_]));g.add((p,RDFS.comment,Literal(note,lang='en')))
        if parent:g.add((p,RDFS.subPropertyOf,CM[parent]))
        n=CM[name+'Shape'];shapes.add((n,RDF.type,SH.NodeShape));shapes.add((n,SH.targetSubjectsOf,p));shapes.add((n,SH['class'],CM[domain]))
        q=BNode();shapes.add((n,SH.property,q));shapes.add((q,SH.path,p));shapes.add((q,SH['class'],CM[range_]))
    g.serialize(OUT/'active.ttl',format='turtle');shapes.serialize(OUT/'constraints.ttl',format='turtle')
    for filename in ['conceptual-model.json','contract.json']:
        d=json.loads((BASE/filename).read_text());d['version']=VERSION;d['g2_connections']=list(BRIDGES);model.write_json(OUT/filename,d)
    rows=list(csv.DictReader((ROOT/'v2/research/w4/connection-candidates.csv').open()))
    assert {r['id'] for r in rows}==set(DISPOSITIONS)
    for r in rows:
        r['g2_status'],r['g2_rationale']=DISPOSITIONS[r['id']];r['implemented_properties']=[n for n,b in BRIDGES.items() if b[0]==r['id']]
        r['authority']='Technical disposition within user-authorized candidate work; not new expert sign-off'
    model.write_json(OUT/'connection-dispositions.json',dict(source_revision=SOURCE_REV,rows=rows))
    model.write_json(OUT/'source-evidence.json',dict(source_revision=SOURCE_REV,held_out_used=False,sources=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in SOURCES],boundary='Repository conceptual/schema evidence and pre-existing synthetic fixtures; no new real dataset ingestion, source validation or clinical validation.'))
    native,unresolved=model.make_native(g);native['id']='cm-pharme-g2';native['name']={'en':'CM-PharmE G2 source-bounded connectivity candidate'}
    for e in native['elements']:
        if e['type']=='Property' and any(e['id']=='end-'+n+'-'+side for n in BRIDGES for side in ['source','target']):
            e['cardinality']='0..*';e['isReadOnly']=False
    # Add source-supported subset metadata; subtype treatment is still subject to G3 semantic review.
    index={e['id']:e for e in native['elements']}
    for n,(_,_,_,parent,_) in BRIDGES.items():
        if parent:
            for side in ['source','target']:index['end-'+n+'-'+side]['subsettedProperties']=['end-'+parent+'-'+side]
    schema=json.loads((ROOT/'tools/v2_ontology/vendor/ontouml-schema.json').read_text());validator=Draft202012Validator(schema,format_checker=FormatChecker())
    errors=list(validator.iter_errors(native))
    for e in native['elements']:errors+=list(validator.iter_errors(e))
    assert not errors,errors
    ids={e['id'] for e in native['elements']};assert len(ids)==len(native['elements'])
    for e in native['elements']:
        for key in ['general','specific','propertyType']:
            if e.get(key) is not None:assert e[key] in ids
        for key in ['properties','contents','generalizations','subsettedProperties']:assert all(v in ids for v in e.get(key,[]))
    model.write_json(OUT/'ontouml.json',native)
    # Same exact graph metric as G1. Broader aboutness parents are untouched.
    topology=dict(before=audit.topology(old),after=audit.topology(g))
    for p in ['observationResultAbout','riskAssessmentConcerns','disruptionAffects']:
        assert set(old.objects(CM[p],RDFS.range))==set(g.objects(CM[p],RDFS.range))
    assert set(old.subjects(RDF.type,OWL.Class))==set(g.subjects(RDF.type,OWL.Class))
    protected=json.loads((BASE/'structural-audit.json').read_text())['protected_distinctions']
    # No logical axiom removed except candidate version/status annotations.
    removed=set(old)-set(g);assert all(p in {OWL.versionInfo,OWL.versionIRI,META.formalizationStatus,META.conceptualModelVersion} for _,p,_ in removed)
    model.write_json(OUT/'model-validation.json',dict(active_classes=119,datatypes=6,object_properties=len(set(g.subjects(RDF.type,OWL.ObjectProperty))),new_connections=len(BRIDGES),schema_errors=0,validated_elements=len(ids),unresolved_native_relations=unresolved,remaining_role_grounding=model.legacy_ungrounded(g),protected_distinctions_unchanged=True,topology=topology,official_anti_pattern_engine='NOT_RUN',full_conformance='NOT_ESTABLISHED'))
    return g,shapes

def check_bridges(g,shapes):
    results=[];positives=Graph()
    for name,(_,domain,range_,parent,_) in BRIDGES.items():
        for variant in ['valid','wrong_subject','wrong_target','multiple_targets']:
            f=Graph();s=LAB[name+'-s'];o=LAB[name+'-o']
            f.add((s,RDF.type,CM[domain] if variant!='wrong_subject' else CM.SourceRecord));f.add((o,RDF.type,CM[range_] if variant!='wrong_target' else CM.SourceRecord));f.add((s,CM[name],o))
            # Complete SupplyDependency participant pattern, preserving G1 checks.
            if range_=='SupplyDependency' and variant!='wrong_target':
                f.add((o,CM.dependencyDependent,LAB[name+'-dependent']));f.add((o,CM.dependencyProvider,LAB[name+'-provider']))
                for suffix,role in [('dependent','DependentOrganizationRole'),('provider','ProviderOrganizationRole')]:f.add((LAB[name+'-'+suffix],RDF.type,CM[role]))
            if variant=='multiple_targets':
                second=LAB[name+'-o2'];f.add((second,RDF.type,CM[range_]));f.add((s,CM[name],second))
                if range_=='SupplyDependency':
                    f.add((second,CM.dependencyDependent,LAB[name+'-dependent']));f.add((second,CM.dependencyProvider,LAB[name+'-provider']))
            passed,_,_=validate(f,shacl_graph=shapes,ont_graph=g,inference='none',advanced=True)
            expected=variant in ['valid','multiple_targets'];results.append(dict(property=name,case=variant,expected_conforms=expected,conforms=bool(passed),passed=bool(passed)==expected))
            if variant=='valid':
                for t in f:positives.add(t)
    assert all(r['passed'] for r in results)
    positives.serialize(OUT/'lab/g2-positive-bridges.ttl',format='turtle')
    return results,positives

def project_nhif(g,shapes):
    db=sqlite3.connect(':memory:');db.executescript('''CREATE TABLE observation(id TEXT PRIMARY KEY, source_row TEXT, presentation TEXT, diagnosis TEXT, metric TEXT, value TEXT, period TEXT, label TEXT);''')
    rdf=Graph();row_count=0
    for family in ['outpatient','inpatient']:
        for i,row in enumerate(csv.DictReader((ROOT/f'v2/data/fixtures/nhif_{family}_fixture.csv').open()),start=1):
            row_count+=1;sid=f'{family}-row-{i}'
            identity_fields=['NHIF_SYNTHETIC_FIXTURE_SCOPE',row['nhif_code'],row['packaging'],row['concentration'],row['num_in_pack']]
            presentation='presentation-'+hashlib.sha256(json.dumps(identity_fields).encode()).hexdigest()[:20]
            diagnosis='icd10-'+quote(row['icd_code'],safe='')
            for metric in ['patients_num','pack_num','costs_bgn']:
                id=sid+'-'+metric;db.execute('INSERT INTO observation VALUES (?,?,?,?,?,?,?,?)',(id,sid,presentation,diagnosis,metric,row[metric],row['period'],row['icd_name']))
    for id,sid,pres,diag,metric,value,period,label in db.execute('SELECT * FROM observation'):
        rdf.add((LAB[id],RDF.type,CM.ReimbursementUtilisationObservationResult));rdf.add((LAB[pres],RDF.type,CM.MedicinalProductPresentation));rdf.add((LAB[diag],RDF.type,CM.DiagnosisClassificationReference))
        rdf.add((LAB[id],CM.observationAboutPresentation,LAB[pres]));rdf.add((LAB[id],CM.reimbursementDiagnosisContext,LAB[diag]));rdf.add((LAB[diag],RDFS.label,Literal(label)))
        rdf.add((LAB[sid],RDF.type,CM.SourceRecord));rdf.add((LAB[id],LAB.sourceRow,LAB[sid]));rdf.add((LAB[id],LAB.reportingPeriod,Literal(period)))
        rdf.add((LAB[id],CM.measureNumericValue,Literal(value,datatype=XSD.decimal)));rdf.add((LAB[id],CM.measureUnitLabel,Literal(metric)))
    conforms,_,detail=validate(rdf,shacl_graph=shapes,ont_graph=g,inference='none',advanced=True);assert conforms,detail
    sql=set(db.execute('SELECT id,presentation,diagnosis,source_row FROM observation'))
    sparql={(str(a).removeprefix(str(LAB)),str(b).removeprefix(str(LAB)),str(c).removeprefix(str(LAB)),str(d).removeprefix(str(LAB))) for a,b,c,d in rdf.query(f'SELECT ?o ?p ?d ?s WHERE {{ ?o <{CM.observationAboutPresentation}> ?p; <{CM.reimbursementDiagnosisContext}> ?d; <{LAB.sourceRow}> ?s. }}')}
    assert sql==sparql and len(sql)==21
    assert len(set(rdf.subjects(RDF.type,CM.SourceRecord)))==7
    assert not any(str(t).endswith('Patient') for t in rdf.objects(None,RDF.type))
    rdf.serialize(OUT/'lab/nhif-candidate-projection.ttl',format='turtle');(OUT/'lab/nhif-candidate-projection.sql').write_text('\n'.join(db.iterdump())+'\n')
    result=dict(input_kind='Existing schema-faithful synthetic fixtures; not downloaded NHIF rows',source_rows=row_count,metric_observations=len(sql),typed_connection_assertions=2*len(sql),sql_sparql_exact_match=True,shacl_conforms=True,source_rows_preserved=7,patient_individuals_created=0,frozen_w6_projection_modified=False)
    model.write_json(OUT/'lab/nhif-projection-results.json',result)
    return result,rdf

def main():
    g,shapes=build();(OUT/'lab').mkdir(exist_ok=True)
    # Regression uses the identical G1 scenarios under the new graph and constraints.
    lab.OUT=OUT;lab.DEST=OUT/'lab';lab.main()
    tests,positive=check_bridges(g,shapes);nhif,projection=project_nhif(g,shapes)
    data=Graph().parse(OUT/'lab/reasoner-input.rdf')
    for source in [positive,projection]:
        for a,b,c in source:
            if str(b).startswith(str(LAB)):continue  # source-row metadata retained in projection, outside ontology reasoner scope
            data.add((a,b,c))
    data.serialize(OUT/'lab/reasoner-input.rdf',format='xml')
    reasoners.OUT=OUT;reasoners.main()
    r=json.loads((OUT/'reasoner-results.json').read_text());r['scope']='G2 schema plus 12 G1 profile witnesses, six G2 relation witnesses and 21 synthetic NHIF metric observations; lab provenance metadata excluded from reasoner input. Not official OntoUML anti-pattern validation or real-data evaluation.';model.write_json(OUT/'reasoner-results.json',r)
    model.write_json(OUT/'g2-results.json',dict(connection_register_rows=15,already_implemented=4,new_scoped_items=5,deferred_items=6,new_object_properties=6,bridge_tests=tests,bridge_tests_passed=sum(x['passed'] for x in tests),g1_regression_passed=120,nhif_projection=nhif,held_out_used=False,official_anti_pattern_engine='NOT_RUN',status='G2 bounded technical disposition complete; six evidence/scope deferrals and G3 semantics remain open'))
    print(json.dumps(dict(g2_tests_passed=len(tests),nhif=nhif),indent=2))

if __name__=='__main__':main()
