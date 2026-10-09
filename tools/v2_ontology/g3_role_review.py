#!/usr/bin/env python3
"""Audit inherited role grounding; apply only the evidenced hierarchy repair.
Do not manufacture existential dependencies to turn open decisions into passes.
"""
import json, copy, subprocess, hashlib
from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL, URIRef
from jsonschema import Draft202012Validator, FormatChecker
from pyshacl import validate
import owlready2
import g1_model as model
import g1_audit as audit
import g1_lab as lab
import g1_reasoners as reasoners
import g2_connections as g2

ROOT=model.ROOT;CM=model.CM;META=model.META
BASE=ROOT/'v2/ontology/candidates/2.1.0-alpha.1-g2-candidate'
OUT=BASE.parent/'2.1.0-alpha.1-g3a-review'
VERSION=OUT.name
REVIEW={
 'ManufacturerRole':('Organization','V2C-004; V2R-006/024/025; W4 R4','Keep umbrella meaning; distinguish authorized manufacturing, contractual manufacturing responsibility and performed manufacturing participation.','A registration, license, operation or source label alone must not assert a particular manufacturing occurrence.','Does the umbrella include commissioned/contract manufacturing without operating the physical site? Recommended: yes, if an explicit responsibility commitment is evidenced.'),
 'ManufacturingSiteRole':('Facility','V2C-011; V2R-003/024; W4 R4','Separate authorized use, assigned manufacturing function and participation in a concrete manufacturing event.','A currently registered site may have no evidenced production event in the observation interval.','May a site retain its assigned function while idle? Recommended: yes; do not require an event at every snapshot.'),
 'ImporterRole':('Organization','V2C-005; V2R-006/008; W4 R3/R4','Distinguish import authorization from responsibility in a documented import context.','Generic authorization does not establish import scope, and import permission does not establish a shipment.','Recommended: preserve a broad umbrella with separate permission/responsibility contexts, not a universal licensing axiom.'),
 'WholesaleDistributorRole':('Organization','V2C-007; V2R-004/008/026; W4 R3/R4','Use explicit wholesale scope and separate actual distribution responsibility.','Neither establishment registration nor a generic logistics activity proves wholesale distribution.','Recommended: explicit wholesale scope; do not infer ownership transfer or a shipment from licensure reporting.'),
 'ThirdPartyLogisticsProviderRole':('Organization','V2C-008; V2R-004/008/026; W4 R3/R4','Model service responsibility separately from wholesale ownership/distribution and permission.','Logistics services do not by themselves imply title to the pharmaceutical product.','Recommended: distinguish the service commitment from license evidence and from individual activities.'),
 'DistributionSiteRole':('Facility','V2C-012; V2R-004/026; W4 R4','A site function/use role; distinguish assigned distribution/storage use, authorization and activity occurrence.','Facility operation alone does not make a site a distribution site; an idle distribution site need not lose its assigned function.','Recommended: a documented site-use context without asserting an actual shipment.'),
 'RegulatoryAuthorityRole':('Organization','V2C-003; V2R-005/011/055; W4 R2/R3/R13','Distinguish institutional mandate from exercising registration, authorization or oversight.','An authority may hold its mandate before issuing any registration or license.','Recommended: a mandate context; do not define the parent as exactly the union of the three exercised-authority subroles.'),
 'ProductResponsibleLabelerRole':('Organization','V2C-006; V2R-019/020; W4 R6','ListingResponsibleOrganizationRole is a subtype; the broader label/product responsibility may have additional contexts.','A private labeler need not perform manufacturing; a broader responsibility role must not automatically create a market listing.','Recommended: retain the broad parent and the one-way listing subtype. Additional label-only contexts require their own definition.'),
 'PayerFundingOrganizationRole':('Organization','V2C-009; V2R-072; Market Access extension','Distinguish reimbursement/funding commitment from publication of aggregate utilization observations.','Publishing reimbursement counts does not establish the publisher as payer, patient identity, coverage entitlement or payment occurrence.','Recommended: an explicit funding/reimbursement commitment context; aggregate NHIF rows alone do not establish its full parties/cardinalities.')
}

def build():
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'lab').mkdir(exist_ok=True)
    old=Graph().parse(BASE/'active.ttl');g=Graph()
    for t in old:g.add(t)
    edge=(CM.ListingResponsibleOrganizationRole,RDFS.subClassOf,CM.ProductResponsibleLabelerRole)
    assert edge not in old;g.add(edge)
    for ont in g.subjects(RDF.type,OWL.Ontology):
        g.set((ont,OWL.versionInfo,Literal(VERSION)));g.set((ont,OWL.versionIRI,URIRef(str(CM)+VERSION)));g.set((ont,META.formalizationStatus,Literal('G3-1 role diagnosis and conservative hierarchy repair; nine complete role definitions still require design decisions')))
    for c in list(g.subjects(RDF.type,OWL.Class)):g.set((c,META.conceptualModelVersion,Literal(VERSION)))
    g.bind('cmpe',CM);g.serialize(OUT/'active.ttl',format='turtle')
    (OUT/'constraints.ttl').write_bytes((BASE/'constraints.ttl').read_bytes())
    for name in ['contract.json','conceptual-model.json']:
        d=json.loads((BASE/name).read_text());d['version']=VERSION
        if name=='conceptual-model.json':
            for row in d['concepts']:
                if row['id']=='ListingResponsibleOrganizationRole':row['parents'].append('ProductResponsibleLabelerRole')
        model.write_json(OUT/name,d)
    native=json.loads((BASE/'ontouml.json').read_text());native['id']='cm-pharme-g3a';native['name']={'en':'CM-PharmE inherited Role review candidate'}
    n=model.named('gen-ListingResponsibleOrganizationRole-ProductResponsibleLabelerRole','Generalization');n.update(general='ProductResponsibleLabelerRole',specific='ListingResponsibleOrganizationRole',created='2026-10-06')
    native['elements'].append(n)
    next(e for e in native['elements'] if e['id']==native['root'])['contents'].append(n['id'])
    schema=json.loads((ROOT/'tools/v2_ontology/vendor/ontouml-schema.json').read_text());v=Draft202012Validator(schema,format_checker=FormatChecker());errors=list(v.iter_errors(native))
    for e in native['elements']:errors.extend(v.iter_errors(e))
    assert not errors
    ids={e['id'] for e in native['elements']};assert len(ids)==len(native['elements'])
    for e in native['elements']:
        for key in ['general','specific','propertyType']:
            if e.get(key) is not None:assert e[key] in ids
        for key in ['contents','properties','generalizations','subsettedProperties']:assert all(x in ids for x in e.get(key,[]))
    model.write_json(OUT/'ontouml.json',native)
    kinds=set(g.subjects(META.ontoumlStereotype,Literal('Kind')))
    rows=[]
    for role,(identity,evidence,recommendation,counterexample,question) in REVIEW.items():
        providers=audit.ancestors(g,CM[role])&kinds;assert providers=={CM[identity]}
        rows.append(dict(role=role,identity_provider=identity,identity_check='PASS',evidence=evidence,recommended_design=recommendation,rejection_example=counterexample,decision=question,complete_grounding='OPEN',human_approval='NOT_RECORDED_FOR_THIS_NEW_DECISION'))
    # Preserve every old logical triple. Only candidate version/status annotations change.
    assert all(p in {OWL.versionInfo,OWL.versionIRI,META.formalizationStatus,META.conceptualModelVersion} for _,p,_ in set(old)-set(g))
    added=[t for t in set(g)-set(old) if t[1] not in {OWL.versionInfo,OWL.versionIRI,META.formalizationStatus,META.conceptualModelVersion}];assert added==[edge]
    model.write_json(OUT/'role-decision-register.json',dict(scope='All nine inherited role definitions. Recommendations are not author/expert approval and not implemented existential axioms.',roles=rows))
    model.write_json(OUT/'model-validation.json',dict(classes=len(set(g.subjects(RDF.type,OWL.Class))),datatypes=len(set(g.subjects(RDF.type,RDFS.Datatype))),object_properties=len(set(g.subjects(RDF.type,OWL.ObjectProperty))),schema_errors=0,validated_elements=len(ids),identity_checks_passed=9,logical_axioms_added=1,logical_axioms_removed=0,full_grounding_open=9,unresolved_relation_records=42,topology_before=audit.topology(old),topology_after=audit.topology(g),official_anti_pattern_engine='NOT_RUN',free_role_warning='The previous nine-item list is a grounding review queue, not nine proven occurrences of the catalogue FreeRole pattern.'))
    return g

def complement(g,subject,class_):
    c=BNode();g.add((c,RDF.type,OWL.Class));g.add((c,OWL.complementOf,CM[class_]));g.add((subject,RDF.type,c))

def counterexamples():
    ns=Namespace('https://example.org/g3-role-counterexample/');g=Graph();rows=[]
    tests=[
      ('registration-not-manufacture','Organization','EstablishmentRegistration','registrationEntity','ManufacturerRole'),
      ('registered-site-not-manufacturing-site','Facility','EstablishmentRegistration','registrationEntity','ManufacturingSiteRole'),
      ('operator-not-manufacturer','Organization','FacilityOperation','operationOrganization','ManufacturerRole'),
      ('operated-site-not-manufacturing-site','Facility','FacilityOperation','operationFacility','ManufacturingSiteRole'),
      ('generic-license-not-import-scope','Organization','RegulatoryAuthorization','authorizationParty','ImporterRole'),
      ('generic-license-not-wholesale','Organization','RegulatoryAuthorization','authorizationParty','WholesaleDistributorRole'),
      ('generic-license-not-3pl','Organization','RegulatoryAuthorization','authorizationParty','ThirdPartyLogisticsProviderRole'),
      ('generic-site-license-not-distribution-use','Facility','RegulatoryAuthorization','authorizationParty','DistributionSiteRole'),
      ('labeler-not-manufacturer','ListingResponsibleOrganizationRole',None,None,'ManufacturerRole'),
      ('listing-responsibility-not-payment','ListingResponsibleOrganizationRole',None,None,'PayerFundingOrganizationRole'),
      ('organization-not-authority','Organization',None,None,'RegulatoryAuthorityRole'),
      ('broad-responsibility-not-necessarily-listed','ProductResponsibleLabelerRole',None,None,'ListingResponsibleOrganizationRole')
    ]
    for id,kind,profile,prop,forbidden in tests:
        s=ns[id];g.add((s,RDF.type,CM[kind]));complement(g,s,forbidden)
        if profile:
            r=ns[id+'-context'];g.add((r,RDF.type,CM[profile]));g.add((r,CM[prop],s))
        rows.append(dict(id=id,asserted_type=kind,context=profile,not_entailed=forbidden))
    g.serialize(OUT/'lab/non-entailment-witnesses.ttl',format='turtle')
    model.write_json(OUT/'lab/non-entailment-cases.json',dict(method='Joint consistency with explicit class complements supplies countermodels for these twelve particular unwanted entailments. This is not a complete modal/temporal role test.',cases=rows))
    return g

def contradiction_check(g):
    bad=Graph()
    for t in g:bad.add(t)
    x=URIRef('https://example.org/g3-role-counterexample/listing-without-product-responsibility');bad.add((x,RDF.type,CM.ListingResponsibleOrganizationRole));complement(bad,x,'ProductResponsibleLabelerRole')
    path=OUT/'lab/negative-subtype.rdf';bad.serialize(path,format='xml')
    world=owlready2.World();world.get_ontology(path.as_uri()).load();hermit=False
    try:owlready2.sync_reasoner(world,debug=0)
    except owlready2.OwlReadyInconsistentOntologyError:hermit=True
    finally:world.close()
    cp=':'.join(map(str,(Path(owlready2.__path__[0])/'pellet').glob('*.jar')))
    run=subprocess.run(['java','-cp',cp,str(ROOT/'tools/v2_ontology/CheckOWL2DL.java'),str(path)],capture_output=True,text=True)
    pellet=run.returncode==2 and 'CONSISTENT=false' in run.stdout and 'IN_OWL2_DL=true' in run.stdout
    assert hermit and pellet,(run.stdout,run.stderr)
    return dict(expected='INCONSISTENT',HermiT_rejected=hermit,Pellet_rejected=pellet,reason='A listing-responsible organization cannot be outside the broader product-responsibility role after the repaired subtype axiom.')

def main():
    g=build();shapes=Graph().parse(OUT/'constraints.ttl')
    lab.OUT=OUT;lab.DEST=OUT/'lab';lab.main()
    g2.OUT=OUT;bridge_results,positive=g2.check_bridges(g,shapes)
    nhif=Graph().parse(BASE/'lab/nhif-candidate-projection.ttl');ok,_,_=validate(nhif,shacl_graph=shapes,ont_graph=g,inference='none',advanced=True);assert ok
    # Preserve the previously tested ABox without accidentally copying the old TBox.
    previous=Graph().parse(BASE/'lab/reasoner-input.rdf');known=set(g.subjects(RDF.type,OWL.Class));individuals={s for s,_,o in previous.triples((None,RDF.type,None)) if o in known}
    data=Graph()
    for t in g:data.add(t)
    for s in individuals:
        for t in previous.triples((s,None,None)):data.add(t)
    for t in counterexamples():data.add(t)
    data.serialize(OUT/'lab/reasoner-input.rdf',format='xml')
    reasoners.OUT=OUT;reasoners.main()
    result=json.loads((OUT/'reasoner-results.json').read_text());result['scope']='G3a schema plus retained G2 ABox and twelve explicit non-entailment countermodels; not full role grounding or official OntoUML detection.';model.write_json(OUT/'reasoner-results.json',result)
    neg=contradiction_check(g)
    model.write_json(OUT/'results.json',dict(g1_regression_passed=120,g2_bridge_tests_passed=sum(r['passed'] for r in bridge_results),nhif_projection_shacl_pass=True,non_entailment_witnesses_consistent=12,negative_subtype_test=neg,role_identity_checks=9,roles_fully_grounded_by_this_change=0,complete_role_definitions_still_open=9,status='Review and conservative repair complete; G3-1 full grounding remains OPEN.'))
    print(json.dumps(json.loads((OUT/'results.json').read_text()),indent=2))

if __name__=='__main__':main()
