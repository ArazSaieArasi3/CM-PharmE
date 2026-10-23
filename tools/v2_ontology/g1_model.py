#!/usr/bin/env python3
"""Build the author-approved G1 implementation candidate; never edit frozen 2.0."""
from pathlib import Path
from collections import defaultdict
import json, hashlib, re
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, OWL, XSD
from rdflib.collection import Collection
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'v2/ontology/candidates/2.1.0-alpha.0-review'
OUT = ROOT / 'v2/ontology/candidates/2.1.0-alpha.1-candidate'
CM = Namespace('https://w3id.org/cm-pharme/2.1/')
META = Namespace(str(CM)+'meta/')
SH = Namespace('http://www.w3.org/ns/shacl#')
VERSION = '2.1.0-alpha.1-candidate'
DEFERRED = {'AssetAtRisk':'S-04', 'Vulnerability':'S-04', 'ClinicalCareParticipant':'S-05'}
ROLES = {}
MIXINS = defaultdict(list)

def role(name, identity, mixin=None, parent=None):
    ROLES[name] = {'identity':identity, 'parent':parent or identity}
    if mixin: MIXINS[mixin].append(name)
    return name

role('OperatingOrganizationRole','Organization')
role('OperatedFacilityRole','Facility')
for prefix,mixin in [('Registered','RegisteredParty'),('Authorized','AuthorizedParty'),('Governed','GovernedEntity')]:
    for kind in ['Organization','Facility']: role(prefix+kind+'Role',kind,mixin)
for prefix in ['Registering','Authorizing','Oversight']:
    role(prefix+'AuthorityRole','Organization',parent='RegulatoryAuthorityRole')
for kind in ['MedicinalProduct','PharmaceuticalSubstance']:
    role('Classified'+kind+'Role',kind,'ClassifiedEntity')
role('AppliedClassificationEntryRole','ClassificationEntry')
role('ListedPresentationRole','MedicinalProductPresentation')
role('ListingResponsibleOrganizationRole','Organization')
role('SupportedAssertionRole','Assertion')
role('EvidenceSourceRecordRole','SourceRecord','EvidenceItem')
role('EvidenceObservationResultRole','ObservationResult','EvidenceItem')
for kind in ['Organization','Facility','MedicinalProduct','PharmaceuticalSubstance','MedicinalProductPresentation','GeographicFeature']:
    role('Identified'+kind+'Role',kind,'IdentifiedEntity')
role('UsedIdentifierSchemeRole','IdentifierScheme')
role('ReferenceProductRole','MedicinalProduct')
for prefix,mixin in [('Dependent','DependentEntity'),('Provider','ProviderEntity')]:
    for kind in ['Organization','Facility','MedicinalProduct']: role(prefix+kind+'Role',kind,mixin)
role('PartnerOrganizationRole','Organization')

def slot(prop, target, kinds, minimum=1, maximum=1):
    if isinstance(kinds,str): kinds={kinds:target}
    return dict(property=prop,target=target,kinds=kinds,min=minimum,max=maximum)

def family(prefix,kinds): return {k:prefix+k+'Role' for k in kinds}
PROFILES = {
 'FacilityOperation': {'operator':slot('operationOrganization','OperatingOrganizationRole','Organization',1,None), 'facility':slot('operationFacility','OperatedFacilityRole','Facility')},
 'EstablishmentRegistration': {'authority':slot('registrationAuthority','RegisteringAuthorityRole','Organization'), 'subject':slot('registrationEntity','RegisteredParty',family('Registered',['Organization','Facility']))},
 'RegulatoryAuthorization': {'authority':slot('authorizationAuthority','AuthorizingAuthorityRole','Organization'), 'subject':slot('authorizationParty','AuthorizedParty',family('Authorized',['Organization','Facility']))},
 'ProductClassificationAssignment': {'subject':slot('classificationEntity','ClassifiedEntity',family('Classified',['MedicinalProduct','PharmaceuticalSubstance'])), 'entry':slot('classificationEntry','AppliedClassificationEntryRole','ClassificationEntry')},
 'MarketListing': {'presentation':slot('listingPresentation','ListedPresentationRole','MedicinalProductPresentation'), 'responsible':slot('listingResponsibleOrganization','ListingResponsibleOrganizationRole','Organization')},
 'EvidenceSupport': {'evidence':slot('evidenceItem','EvidenceItem',{'SourceRecord':'EvidenceSourceRecordRole','ObservationResult':'EvidenceObservationResultRole'}), 'claim':slot('evidenceAssertion','SupportedAssertionRole','Assertion')},
 'IdentifierAssignment': {'subject':slot('identifierEntity','IdentifiedEntity',family('Identified',['Organization','Facility','MedicinalProduct','PharmaceuticalSubstance','MedicinalProductPresentation','GeographicFeature'])), 'scheme':slot('identifierScheme','UsedIdentifierSchemeRole','IdentifierScheme')},
 'AlternativeMedicineAssignment': {'reference':slot('alternativeForProduct','ReferenceProductRole','MedicinalProduct'), 'alternative':slot('alternativeProduct','AlternativeMedicinalProductRole','MedicinalProduct')},
 'SupplyDependency': {'dependent':slot('dependencyDependent','DependentEntity',family('Dependent',['Organization','Facility','MedicinalProduct'])), 'provider':slot('dependencyProvider','ProviderEntity',family('Provider',['Organization','Facility','MedicinalProduct']))},
 'RegulatoryOversight': {'authority':slot('oversightAuthorityRole','OversightAuthorityRole','Organization'), 'subject':slot('oversightGovernedEntity','GovernedEntity',family('Governed',['Organization','Facility']))},
 'StrategicPartnershipAgreement': {'partner':slot('partnershipParticipant','PartnerOrganizationRole','Organization',2,None)}
}
PROFILES['ContextualMedicineClassificationAssignment'] = PROFILES['ProductClassificationAssignment']
DECISIONS = {
 'RR-01':('FacilityOperation','operator','Operating organization Role; one or more operators.'),
 'RR-02':('FacilityOperation','facility','Operated facility Role; exactly one facility per operation relation.'),
 'RR-03':('EstablishmentRegistration','subject','Separate registered Organization and Facility Roles.'),
 'RR-04':('ProductClassificationAssignment','subject','Separate classified Product and Substance Roles.'),
 'RR-05':('ProductClassificationAssignment','entry','Applied entry Role is a relatum; revise W4 reference wording.'),
 'RR-06':('MarketListing','responsible','Scoped listing requires presentation and documented responsible party.'),
 'RR-07':('EvidenceSupport','claim','Supported Assertion Role; support never implies truth.'),
 'RR-08':('IdentifierAssignment','scheme','Used scheme Role is a relatum; lexical value remains a literal.'),
 'RR-09':('AlternativeMedicineAssignment','reference','Reference and alternative are context-local product roles.'),
 'RR-10':('SupplyDependency','dependent','Dependent is an admitted endurant; events excluded from this RoleMixin.'),
 'RR-11':('SupplyDependency','provider','Provider is Organization, Facility or Product; no required Org-Facility pair.'),
 'RR-12':('StrategicPartnershipAgreement','partner','At least two distinct partner organizations; repeated independent agreements permitted.'),
 'RR-13':('EvidenceSupport','evidence','Record evidence is a specialization of generic evidence; no double counting.'),
 'RR-14':('ContextualMedicineClassificationAssignment','subject','Contextual classification reuses Product/Substance pattern.'),
 'RR-15':('ContextualMedicineClassificationAssignment','entry','Contextual entry link subsets the generic assignment pattern.'),
 'S-01':('IdentifierAssignment','subject','Identified bearer and used scheme, lexical value, provenance and validity.'),
 'S-02':('RegulatoryOversight','subject','Separate governed roles and authority; activity scope stays a reported target.'),
 'S-03':('EvidenceSupport','evidence','EvidenceItem has distinct SourceRecord and ObservationResult identities.'),
 'S-04':(None,None,'Defer AssetAtRisk and dependent Vulnerability bearer pattern; preserve declarations outside active import.'),
 'S-05':(None,None,'Defer ClinicalCareParticipant until admitted bearer and care-activity pattern.'),
 'S-06':(None,None,'Strict directed geographic containment: no self-loop or cycle; no universal transitivity axiom added.'),
 'S-07':('AlternativeMedicineAssignment','alternative','Distinct values within one assignment; roles may overlap across assignments.')
}

def write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def restriction(g,owner,prop,kind,value,filler=None,inverse=False):
    n=BNode(); p=CM[prop]
    if inverse:
        p=BNode(); g.add((p,OWL.inverseOf,CM[prop]))
    g.add((CM[owner],RDFS.subClassOf,n)); g.add((n,RDF.type,OWL.Restriction)); g.add((n,OWL.onProperty,p))
    if filler: g.add((n,OWL.onClass,CM[filler]))
    g.add((n,kind,Literal(value,datatype=XSD.nonNegativeInteger)))

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    g=Graph()
    for p in sorted((BASE/'modules').glob('*.ttl')): g.parse(p)
    # OWLAPI profile found 21 annotation assertions using an undeclared SKOS property.
    g.add((URIRef('http://www.w3.org/2004/02/skos/core#altLabel'),RDF.type,OWL.AnnotationProperty))
    base_classes=set(g.subjects(RDF.type,OWL.Class)); base_props=set(g.subjects(RDF.type,OWL.ObjectProperty))
    baseline=json.loads((BASE/'conceptual-model.json').read_text())
    deferred=Graph()
    # Remove deferred subjects and their restriction blank-node closure from active ontology.
    subjects={CM[x] for x in DEFERRED}|{CM.vulnerabilityBearer}
    todo=list(subjects)
    while todo:
        s=todo.pop()
        for triple in list(g.triples((s,None,None))):
            deferred.add(triple);g.remove(triple)
            if isinstance(triple[2],BNode) and triple[2] not in subjects:
                subjects.add(triple[2]);todo.append(triple[2])
    assert not any(o in {CM[x] for x in DEFERRED} for _,_,o in g)
    for graph in [g,deferred]: graph.bind('cmpe',CM);graph.bind('cmmeta',META)
    for old in list(g.triples((None,META.conceptualModelVersion,None))): g.remove(old)
    for n in list(g.subjects(RDF.type,OWL.Ontology)):
        g.remove((n,OWL.versionIRI,None));g.remove((n,OWL.versionInfo,None))
        g.add((n,OWL.versionIRI,URIRef(str(CM)+VERSION)));g.add((n,OWL.versionInfo,Literal(VERSION)))
        g.set((n,META.formalizationStatus,Literal('G1 author-approved implementation candidate; full validation and release gate pending')))
    for mixin in MIXINS:
        g.add((CM[mixin],RDF.type,OWL.Class));g.set((CM[mixin],META.ontoumlStereotype,Literal('RoleMixin')))
    for name,d in ROLES.items():
        g.add((CM[name],RDF.type,OWL.Class));g.add((CM[name],RDFS.subClassOf,CM[d['parent']]))
        g.set((CM[name],META.ontoumlStereotype,Literal('Role')))
        for mixin,children in MIXINS.items():
            if name in children:g.add((CM[name],RDFS.subClassOf,CM[mixin]))
    # A specialization of a Relator is Subkind, not another identity-providing Relator.
    g.set((CM.ContextualMedicineClassificationAssignment,META.ontoumlStereotype,Literal('Subkind')))
    g.add((CM.ContextualMedicineClassificationAssignment,RDFS.subClassOf,CM.ProductClassificationAssignment))
    # Context-scoped legacy aliases remain available, but are not new participant positions.
    for name,parent,target in [('contextClassificationProduct','classificationEntity','ClassifiedMedicinalProductRole'),('contextClassificationEntry','classificationEntry','AppliedClassificationEntryRole'),('evidenceRecord','evidenceItem','EvidenceSourceRecordRole')]:
        g.set((CM[name],RDFS.range,CM[target]));g.add((CM[name],RDFS.subPropertyOf,CM[parent]))
    for profile,slots in PROFILES.items():
        if profile=='ContextualMedicineClassificationAssignment':continue
        for d in slots.values():
            p=CM[d['property']];g.add((p,RDF.type,OWL.ObjectProperty));g.set((p,RDFS.domain,CM[profile]));g.set((p,RDFS.range,CM[d['target']]))
            restriction(g,profile,d['property'],OWL.minQualifiedCardinality,d['min'],d['target'])
            if d['max'] is not None:restriction(g,profile,d['property'],OWL.maxQualifiedCardinality,d['max'],d['target'])
            restriction(g,d['target'],d['property'],OWL.minQualifiedCardinality,1,profile,inverse=True)
        props=[CM[d['property']] for d in slots.values()]
        for i,p in enumerate(props):
            for q in props[i+1:]: g.add((p,OWL.propertyDisjointWith,q))
    # Do not assert global disjointness between contextual roles of the same bearer.
    for x in set(g.subjects(RDF.type,OWL.Class)):
        g.add((x,META.conceptualModelVersion,Literal(VERSION)))
    g.serialize(OUT/'active.ttl',format='turtle');deferred.serialize(OUT/'deferred-not-imported.ttl',format='turtle')
    registry=[]
    for c in sorted(set(g.subjects(RDF.type,OWL.Class))|set(g.subjects(RDF.type,RDFS.Datatype)),key=str):
        registry.append({'id':str(c).split('/')[-1], 'iri':str(c), 'stereotype':str(g.value(c,META.ontoumlStereotype)), 'parents':[str(x).split('/')[-1] for x in g.objects(c,RDFS.subClassOf) if isinstance(x,URIRef)], 'origin':'G1 approved refinement' if str(c).split('/')[-1] in ROLES or (str(c).split('/')[-1] in MIXINS and c not in base_classes) else 'inherited review candidate'})
    write_json(OUT/'conceptual-model.json',{'version':VERSION,'concepts':registry,'protected_distinctions':baseline['protected_distinctions'],'deferred':DEFERRED})
    approvals=[]
    for id,(profile,position,decision) in DECISIONS.items():
        approvals.append(dict(id=id,disposition='DEFER' if id in ['S-04','S-05'] else 'APPROVE',decision=decision,profile=profile,position=position,authority='Project author: explicit batch approval in this conversation',approved_at='2026-10-05T20:59:49+03:30',implementation_status='candidate implemented; validation is separate'))
    write_json(OUT/'decisions.json',{'approval_quote':'بسیار خوب انجام بده\nنتیجه را بگو بعد بگو چه کارهای دیگری باید انجام بدهیم','scope':'preceding 22-decision package; not release approval or independent expert validation','decisions':approvals,'deferred_dependency_closure':DEFERRED})
    write_json(OUT/'contract.json',{'version':VERSION,'profiles':PROFILES,'new_roles':ROLES,'role_mixins':MIXINS,'deferred':DEFERRED,'protected_distinctions':baseline['protected_distinctions'],'temporal_policy':'[valid_from,valid_to); RDF exports are explicit time snapshots; no claim of full modal semantics','identity_policy':'same participant identity in every Role; distinct relation IDs may represent independent agreements with same participants; source record IDs are provenance, not relation identity','closed_profile':'These complete-instance admission constraints do not mean missing source data is false.'})
    shapes=make_shapes(g);shapes.serialize(OUT/'constraints.ttl',format='turtle')
    native,unresolved=make_native(g)
    write_json(OUT/'ontouml.json',native)
    schema=json.loads((ROOT/'tools/v2_ontology/vendor/ontouml-schema.json').read_text())
    validator=Draft202012Validator(schema,format_checker=FormatChecker())
    errors=list(validator.iter_errors(native))
    for element in native['elements']: errors.extend(validator.iter_errors(element))
    if errors: raise ValueError('\n'.join(e.message[:500] for e in errors[:5]))
    # JSON Schema permits dangling identifiers and arbitrary stereotypes; check these independently.
    ids=[e['id'] for e in native['elements']];assert len(ids)==len(set(ids))
    for e in native['elements']:
        for key in ['general','specific','propertyType']:
            if e.get(key) is not None:assert e[key] in ids,(e['id'],key)
        for key in ['properties','contents','generalizations','subsettedProperties']:
            assert all(v in ids for v in e.get(key,[])),(e['id'],key)
    counts={'original_concepts':87,'deferred_concepts':len(DEFERRED),'added_roles':len(ROLES),'added_role_mixins':len([x for x in MIXINS if CM[x] not in base_classes]),'active_classes':len(set(g.subjects(RDF.type,OWL.Class))),'active_datatypes':len(set(g.subjects(RDF.type,RDFS.Datatype))),'active_object_properties':len(set(g.subjects(RDF.type,OWL.ObjectProperty))),'relator_types':len(set(g.subjects(META.ontoumlStereotype,Literal('Relator'))))}
    counts['active_concepts']=counts['active_classes']+counts['active_datatypes']
    report={'version':VERSION,'counts':counts,'native_schema':{'id':schema['$id'],'upstream_blob_sha':'7608e50f9e020fbadc782fd86d6b0c66e3b85b65','sha256':hashlib.sha256((ROOT/'tools/v2_ontology/vendor/ontouml-schema.json').read_bytes()).hexdigest(),'errors':0,'elements_validated_individually':len(ids),'reference_check':'PASS'},'unresolved_native_relations':unresolved,'official_anti_pattern_engine':'NOT_RUN','remaining_role_grounding':legacy_ungrounded(g),'status':'G1 implemented; full release conformance pending'}
    write_json(OUT/'model-validation.json',report)
    print(json.dumps(report,indent=2))

def make_shapes(g):
    s=Graph();s.bind('sh',SH);s.bind('cmpe',CM)
    for profile,slots in PROFILES.items():
        node=URIRef(str(CM)+profile+'Shape');s.add((node,RDF.type,SH.NodeShape));s.add((node,SH.targetClass,CM[profile]))
        for d in slots.values():
            p=BNode();s.add((node,SH.property,p));s.add((p,SH.path,CM[d['property']]));s.add((p,SH.minCount,Literal(d['min'])));s.add((p,SH['class'],CM[d['target']]))
            if d['max'] is not None:s.add((p,SH.maxCount,Literal(d['max'])))
            for other in slots.values():
                if other is not d:s.add((p,SH.disjoint,CM[other['property']]))
        # Enforce complete canonical provenance/context and interval attributes only on lab instances.
        for d in slots.values():
            rn=CM[d['target']+'DependenceShape'];s.add((rn,RDF.type,SH.NodeShape));s.add((rn,SH.targetClass,CM[d['target']]))
            rp=BNode();path=BNode();s.add((rn,SH.property,rp));s.add((rp,SH.path,path));s.add((path,SH.inversePath,CM[d['property']]));s.add((rp,SH.minCount,Literal(1)))
            # The contextual subtype shares the general pattern; do not require every classified entity to have a contextual assignment.
            if profile!='ContextualMedicineClassificationAssignment':s.add((rp,SH['class'],CM[profile]))
    n=CM.IdentifierAssignmentShape;p=BNode();s.add((n,SH.property,p));s.add((p,SH.path,CM.identifierLexicalValue));s.add((p,SH.minCount,Literal(1)));s.add((p,SH.maxCount,Literal(1)));s.add((p,SH.datatype,XSD.string))
    # Alias cannot carry a second, unrelated participant; it must subset the generic evidence position.
    node=CM.EvidenceAliasShape;s.add((node,RDF.type,SH.NodeShape));s.add((node,SH.targetSubjectsOf,CM.evidenceRecord))
    q=BNode();s.add((node,SH.sparql,q));s.add((q,SH.message,Literal('evidenceRecord must subset evidenceItem')))
    s.add((q,SH.select,Literal('SELECT $this WHERE { $this <'+str(CM.evidenceRecord)+'> ?x . FILTER NOT EXISTS { $this <'+str(CM.evidenceItem)+'> ?x } }')))
    for name in DEFERRED:
        node=CM[name+'DeferredShape'];s.add((node,RDF.type,SH.NodeShape));s.add((node,SH.targetClass,CM[name]));s.add((node,SH['in'],RDF.nil))
    node=CM.GeographyShape;s.add((node,RDF.type,SH.NodeShape));s.add((node,SH.targetSubjectsOf,CM.withinRegion));s.add((node,SH.targetSubjectsOf,CM.withinCountry))
    q=BNode();s.add((node,SH.sparql,q));s.add((q,SH.message,Literal('Strict geographic containment cannot cycle')))
    s.add((q,SH.select,Literal('SELECT $this WHERE { $this (<'+str(CM.withinRegion)+'>|<'+str(CM.withinCountry)+'>)+ $this . }')))
    return s

def named(id,type,name=None):
    return dict(id=id,type=type,name={'en':name or id},created='2026-10-05',modified=None,alternativeNames=[],description=None,editorialNotes=[],creators=[],contributors=[],customProperties=None)

def make_native(g):
    elements=[];unresolved=[]
    classes=sorted(set(g.subjects(RDF.type,OWL.Class))|set(g.subjects(RDF.type,RDFS.Datatype)),key=str)
    names={x:str(x).split('/')[-1] for x in classes}
    for x in classes:
        st=str(g.value(x,META.ontoumlStereotype) or 'Datatype');st={'RoleMixin':'roleMixin','Subkind':'subkind'}.get(st,st.lower())
        e=named(names[x],'Class',str(g.value(x,RDFS.label) or names[x]));e.update(stereotype=st,isDerived=False,isAbstract=st=='roleMixin',properties=[],literals=[],restrictedTo=[],isPowertype=False,order='1');elements.append(e)
    generalizations=defaultdict(list)
    for a,b in sorted(g.subject_objects(RDFS.subClassOf),key=lambda ab:tuple(map(str,ab))):
        if a in names and b in names:
            e=named('gen-'+names[a]+'-'+names[b],'Generalization');e.update(general=names[b],specific=names[a]);elements.append(e);generalizations[names[b]].append(e['id'])
    contract={d['property']:(profile,d) for profile,slots in PROFILES.items() if profile!='ContextualMedicineClassificationAssignment' for d in slots.values()}
    for p in sorted(set(g.subjects(RDF.type,OWL.ObjectProperty)),key=str):
        name=str(p).split('/')[-1];domain=g.value(p,RDFS.domain);range_=g.value(p,RDFS.range)
        known=name in contract;st='mediation' if known else ('material' if name=='operates' else None)
        if not known: unresolved.append({'property':name,'missing':'association stereotype and/or bounds need G2/G3 disposition','typed_domain':domain in names,'typed_range':range_ in names})
        relation=named('rel-'+name,'BinaryRelation',name);relation.update(stereotype=st,isDerived=name=='operates',isAbstract=False,properties=['end-'+name+'-source','end-'+name+'-target']);elements.append(relation)
        for side,typ in [('source',domain),('target',range_)]:
            cardinality=None
            if known:
                d=contract[name][1];cardinality='1..*' if side=='source' else (str(d['min']) if d['min']==d['max'] else str(d['min'])+'..'+str(d['max'] if d['max'] is not None else '*'))
            e=named('end-'+name+'-'+side,'Property');e.update(stereotype=None,isDerived=False,subsettedProperties=[],redefinedProperties=[],aggregationKind='NONE',cardinality=cardinality,isOrdered=False,isReadOnly=False if known else None,propertyType=names.get(typ));elements.append(e)
    # Preserve specialization of relation ends in official subsetting metadata.
    index={e['id']:e for e in elements}
    for child,parent in [('evidenceRecord','evidenceItem'),('contextClassificationProduct','classificationEntity'),('contextClassificationEntry','classificationEntry')]:
        for side in ['source','target']:index['end-'+child+'-'+side]['subsettedProperties']=['end-'+parent+'-'+side]
    for mixin in MIXINS:
        e=named('gs-'+mixin,'GeneralizationSet');e.update(isDisjoint=False,isComplete=False,generalizations=generalizations[mixin],categorizer=None);elements.append(e)
    for id,(_,_,desc) in DECISIONS.items():
        e=named('decision-'+id,'Note');e['text']={'en':id+': '+desc};elements.append(e)
    pack=named('cm-pharme-root','Package');pack['contents']=[e['id'] for e in elements];elements.insert(0,pack)
    project=named('cm-pharme-g1','Project','CM-PharmE G1 author-approved candidate');project.update(elements=elements,root=pack['id'],publisher=None,designedForTasks=[],license=None,accessRights=[],themes=[],contexts=[],ontologyTypes=[],representationStyle=None,namespace=str(CM),landingPages=[],sources=[],bibliographicCitations=[],keywords=[],acronyms=[],languages=['en'])
    return project,unresolved

def legacy_ungrounded(g):
    used={d['target'] for slots in PROFILES.values() for d in slots.values()}
    grounded=used|{r for m in used for r in MIXINS.get(m,[])}
    # Parent authority and ecosystem participation inherit grounded specializations, but no complete covering assertion is invented.
    return sorted(str(c).split('/')[-1] for c in g.subjects(META.ontoumlStereotype,Literal('Role')) if str(c).split('/')[-1] not in grounded)

if __name__=='__main__':build()
