#!/usr/bin/env python3
"""Executable, bounded relational/RDF admission experiment; not domain validation."""
import copy, json, sqlite3
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, OWL, XSD
from pyshacl import validate
from g1_model import ROOT, OUT, CM, META, SH, PROFILES, ROLES, MIXINS, DEFERRED, write_json

LAB=Namespace('https://example.org/cm-pharme-lab/')
DEST=OUT/'lab'
SCHEMA='''PRAGMA foreign_keys=ON;
CREATE TABLE entity(id TEXT PRIMARY KEY, identity_kind TEXT NOT NULL);
CREATE TABLE source(id TEXT PRIMARY KEY, description TEXT NOT NULL);
CREATE TABLE context(id TEXT PRIMARY KEY, jurisdiction TEXT NOT NULL, scheme_version TEXT NOT NULL);
CREATE TABLE relator(id TEXT PRIMARY KEY, type TEXT NOT NULL, context_id TEXT REFERENCES context(id), source_id TEXT REFERENCES source(id), valid_from TEXT, valid_to TEXT, lexical_value TEXT);
CREATE TABLE participation(relator_id TEXT REFERENCES relator(id), slot TEXT NOT NULL, entity_id TEXT REFERENCES entity(id), PRIMARY KEY(relator_id,slot,entity_id));
CREATE TABLE alias(relator_id TEXT REFERENCES relator(id), property TEXT NOT NULL, entity_id TEXT REFERENCES entity(id), PRIMARY KEY(relator_id,property,entity_id));
CREATE TABLE containment(child TEXT REFERENCES entity(id), parent TEXT REFERENCES entity(id), PRIMARY KEY(child,parent));
CREATE TABLE explicit_role(entity_id TEXT REFERENCES entity(id), role TEXT NOT NULL);
CREATE TABLE slot_rule(profile TEXT, slot TEXT, property TEXT, target TEXT, minimum INTEGER, maximum INTEGER, PRIMARY KEY(profile,slot));
CREATE TABLE allowed_kind(profile TEXT, slot TEXT, identity_kind TEXT, role TEXT, PRIMARY KEY(profile,slot,identity_kind));
CREATE VIEW derived_role AS SELECT DISTINCT p.entity_id,a.role,r.context_id,r.valid_from,r.valid_to
 FROM participation p JOIN relator r ON r.id=p.relator_id JOIN entity e ON e.id=p.entity_id
 JOIN allowed_kind a ON a.profile=r.type AND a.slot=p.slot AND a.identity_kind=e.identity_kind;
-- Tables are staging-capable. validate_sql is the mandatory admission gate.
-- Null provenance is retained for review, but may not pass as a complete relator.
'''

def template(profile):
    entities={};parts=[]
    for slot,d in PROFILES[profile].items():
        kind=next(iter(d['kinds']))
        for i in range(d['min']):
            id=f'{slot}{i}';entities[id]=kind;parts.append(['r1',slot,id])
    return dict(entities=entities,relations=[dict(id='r1',type=profile,context='ctx1',source='src1',start='2026-01-01T00:00:00Z',end='2027-01-01T00:00:00Z',lexical='0012' if profile=='IdentifierAssignment' else None)],parts=parts,aliases=[],geo=[],roles=[])

def database(f):
    db=sqlite3.connect(':memory:');db.executescript(SCHEMA)
    db.executemany('INSERT INTO entity VALUES (?,?)',f['entities'].items())
    db.execute('INSERT INTO source VALUES (?,?)',('src1','Synthetic evidence only; no real-world assertion'))
    db.executemany('INSERT INTO context VALUES (?,?,?)',[('ctx1','synthetic-J1','v1'),('ctx2','synthetic-J2','v2')])
    for profile,slots in PROFILES.items():
        for slot,d in slots.items():
            db.execute('INSERT INTO slot_rule VALUES (?,?,?,?,?,?)',(profile,slot,d['property'],d['target'],d['min'],d['max']))
            db.executemany('INSERT INTO allowed_kind VALUES (?,?,?,?)',[(profile,slot,k,r) for k,r in d['kinds'].items()])
    db.executemany('INSERT INTO relator VALUES (?,?,?,?,?,?,?)',[(r['id'],r['type'],r['context'],r['source'],r['start'],r['end'],r['lexical']) for r in f['relations']])
    db.executemany('INSERT INTO participation VALUES (?,?,?)',f['parts']);db.executemany('INSERT INTO alias VALUES (?,?,?)',f['aliases']);db.executemany('INSERT INTO containment VALUES (?,?)',f['geo']);db.executemany('INSERT INTO explicit_role VALUES (?,?)',f['roles'])
    return db

QUERIES={
 'CARDINALITY':'''SELECT r.id,s.slot FROM relator r JOIN slot_rule s ON s.profile=r.type LEFT JOIN participation p ON p.relator_id=r.id AND p.slot=s.slot GROUP BY r.id,s.slot HAVING count(p.entity_id)<s.minimum OR (s.maximum IS NOT NULL AND count(p.entity_id)>s.maximum)''',
 'KIND':'''SELECT p.relator_id,p.slot FROM participation p JOIN relator r ON r.id=p.relator_id JOIN entity e ON e.id=p.entity_id LEFT JOIN allowed_kind a ON a.profile=r.type AND a.slot=p.slot AND a.identity_kind=e.identity_kind WHERE a.role IS NULL''',
 'DISTINCT':'''SELECT relator_id,entity_id FROM participation GROUP BY relator_id,entity_id HAVING count(DISTINCT slot)>1''',
 'PROVENANCE':'''SELECT id FROM relator WHERE source_id IS NULL OR context_id IS NULL''',
 'TIME':'''SELECT id FROM relator WHERE valid_from IS NULL OR valid_to IS NULL OR valid_from>=valid_to''',
 'LEXICAL':'''SELECT id FROM relator WHERE type='IdentifierAssignment' AND (lexical_value IS NULL OR lexical_value='')''',
 'DEFERRED':'''SELECT id FROM entity WHERE identity_kind IN ('AssetAtRisk','Vulnerability','ClinicalCareParticipant')''',
 'CYCLE':'''WITH RECURSIVE reach(child,parent) AS (SELECT child,parent FROM containment UNION SELECT r.child,c.parent FROM reach r JOIN containment c ON r.parent=c.child) SELECT child FROM reach WHERE child=parent''',
 'ALIAS':'''SELECT a.relator_id FROM alias a LEFT JOIN participation p ON p.relator_id=a.relator_id AND p.entity_id=a.entity_id AND p.slot=CASE a.property WHEN 'evidenceRecord' THEN 'evidence' WHEN 'contextClassificationProduct' THEN 'subject' WHEN 'contextClassificationEntry' THEN 'entry' END WHERE p.entity_id IS NULL''',
 'GROUNDING':'''SELECT e.entity_id,e.role FROM explicit_role e WHERE NOT EXISTS (SELECT 1 FROM derived_role d WHERE d.entity_id=e.entity_id AND d.role=e.role)'''
}

def validate_sql(db,disabled=None):return {rule:db.execute(query).fetchall() for rule,query in QUERIES.items() if rule!=disabled and db.execute(query).fetchone() is not None}

def rdf_export(db,ontology,snapshot=None):
    g=Graph();g.bind('lab',LAB);g.bind('cmpe',CM)
    for id,kind in db.execute('SELECT id,identity_kind FROM entity'):g.add((LAB[id],RDF.type,CM[kind]))
    for id, in db.execute('SELECT id FROM source'):g.add((LAB[id],RDF.type,LAB.Source))
    for id,j,v in db.execute('SELECT * FROM context'):
        g.add((LAB[id],RDF.type,LAB.Context));g.add((LAB[id],LAB.jurisdiction,Literal(j)));g.add((LAB[id],LAB.schemeVersion,Literal(v)))
    active=set()
    for id,profile,context,source,start,end,lex in db.execute('SELECT * FROM relator'):
        if snapshot is not None and not (start<=snapshot<end):continue
        active.add(id);r=LAB[id];g.add((r,RDF.type,CM[profile]));g.add((r,RDF.type,LAB.CompleteRelator))
        for p,value in [(LAB.context,context),(LAB.source,source)]:
            if value is not None:g.add((r,p,LAB[value]))
        for p,value in [(CM.validFrom,start),(CM.validTo,end)]:
            if value is not None:g.add((r,p,Literal(value,datatype=XSD.dateTime)))
        if lex is not None:g.add((r,CM.identifierLexicalValue,Literal(lex,datatype=XSD.string)))
    for id,slot,ent,profile,kind in db.execute('SELECT p.relator_id,p.slot,p.entity_id,r.type,e.identity_kind FROM participation p JOIN relator r ON r.id=p.relator_id JOIN entity e ON e.id=p.entity_id'):
        if id not in active:continue
        d=PROFILES[profile][slot];g.add((LAB[id],CM[d['property']],LAB[ent]))
        role=d['kinds'].get(kind)
        if role:g.add((LAB[ent],RDF.type,CM[role]))
    for id,prop,ent in db.execute('SELECT * FROM alias'):
        if id in active:g.add((LAB[id],CM[prop],LAB[ent]))
    for ent,role in db.execute('SELECT * FROM explicit_role'):g.add((LAB[ent],RDF.type,CM[role]))
    for child,parent in db.execute('SELECT * FROM containment'):g.add((LAB[child],CM.withinRegion,LAB[parent]))
    # Explicitly distinct identities in this finite fixture. OWL itself has no unique-name assumption.
    ids=[LAB[x[0]] for x in db.execute('SELECT id FROM entity')]
    for i,x in enumerate(ids):
        for y in ids[i+1:]:g.add((x,OWL.differentFrom,y))
    return g

def shapes():
    s=Graph().parse(OUT/'constraints.ttl');n=LAB.CompleteShape;s.add((n,RDF.type,SH.NodeShape));s.add((n,SH.targetClass,LAB.CompleteRelator))
    for prop,kind in [(LAB.source,LAB.Source),(LAB.context,LAB.Context),(CM.validFrom,XSD.dateTime),(CM.validTo,XSD.dateTime)]:
        p=BNode();s.add((n,SH.property,p));s.add((p,SH.path,prop));s.add((p,SH.minCount,Literal(1)));s.add((p,SH.maxCount,Literal(1)));s.add((p,SH.datatype if kind==XSD.dateTime else SH['class'],kind))
    p=BNode();s.add((n,SH.property,p));s.add((p,SH.path,CM.validFrom));s.add((p,SH.lessThan,CM.validTo))
    p=BNode();s.add((CM.IdentifierAssignmentShape,SH.property,p));s.add((p,SH.path,CM.identifierLexicalValue));s.add((p,SH.minLength,Literal(1)))
    for prop,parent in [('contextClassificationProduct','classificationEntity'),('contextClassificationEntry','classificationEntry')]:
        n=LAB[prop+'AliasShape'];s.add((n,RDF.type,SH.NodeShape));s.add((n,SH.targetSubjectsOf,CM[prop]));q=BNode();s.add((n,SH.sparql,q));s.add((q,SH.select,Literal(f'SELECT $this WHERE {{ $this <{CM[prop]}> ?x . FILTER NOT EXISTS {{ $this <{CM[parent]}> ?x }} }}')))
    return s

def fixtures():
    cases=[]
    def add(name,f,valid,rule=None,decisions=None):cases.append(dict(id=name,fixture=f,expected_valid=valid,expected_rule=rule,decisions=decisions or []))
    for profile,slots in PROFILES.items():
        f=template(profile);add(profile+'-minimal',f,True)
        for slot,d in slots.items():
            n=copy.deepcopy(f);n['parts']=[p for p in n['parts'] if p[1]!=slot];add(profile+'-missing-'+slot,n,False,'CARDINALITY')
            n=copy.deepcopy(f);ent=next(p[2] for p in n['parts'] if p[1]==slot);n['entities'][ent]='ManufacturingActivity';add(profile+'-event-in-'+slot,n,False,'KIND')
            if d['max'] is not None:
                n=copy.deepcopy(f);n['entities']['extra']=next(iter(d['kinds']));n['parts'].append(['r1',slot,'extra']);add(profile+'-excess-'+slot,n,False,'CARDINALITY')
            # Each admitted alternative identity family gets a positive fixture.
            for kind in list(d['kinds'])[1:]:
                n=copy.deepcopy(f);ent=next(p[2] for p in n['parts'] if p[1]==slot);n['entities'][ent]=kind;add(profile+'-'+slot+'-'+kind,n,True)
    f=template('FacilityOperation');f['entities']['operator2']='Organization';f['parts'].append(['r1','operator','operator2']);add('joint-operation',f,True)
    f=template('StrategicPartnershipAgreement');f['entities']['partner2']='Organization';f['parts'].append(['r1','partner','partner2']);add('three-partners',f,True)
    for profile,slot in [('AlternativeMedicineAssignment','alternative'),('SupplyDependency','provider'),('RegulatoryOversight','subject')]:
        f=template(profile);first=f['parts'][0][2];f['parts'][-1][2]=first;add(profile+'-self',f,False,'DISTINCT')
    f=template('AlternativeMedicineAssignment');f['relations'].append(dict(f['relations'][0],id='r2',context='ctx2'));f['parts'] += [['r2','reference','alternative0'],['r2','alternative','reference0']];add('product-can-switch-contextual-roles',f,True)
    f=template('StrategicPartnershipAgreement');f['relations'].append(dict(f['relations'][0],id='r2'));f['parts'] += [[ 'r2',slot,ent] for _,slot,ent in f['parts'][:]];add('independent-agreements-same-partners',f,True)
    f=template('IdentifierAssignment');f['entities']['scheme2']='IdentifierScheme';f['relations'].append(dict(f['relations'][0],id='r2'));f['parts'] += [['r2','subject','subject0'],['r2','scheme','scheme2']];add('same-lexical-value-different-schemes',f,True)
    for key,rule in [('source','PROVENANCE'),('context','PROVENANCE'),('start','TIME'),('lexical','LEXICAL')]:
        f=template('IdentifierAssignment');f['relations'][0][key]=None;add('missing-'+key,f,False,rule)
    f=template('IdentifierAssignment');f['relations'][0]['end']=f['relations'][0]['start'];add('empty-validity-interval',f,False,'TIME')
    f=template('IdentifierAssignment');f['relations'][0]['start']='2028-01-01T00:00:00Z';add('reversed-validity-interval',f,False,'TIME')
    f=template('EvidenceSupport');f['aliases']=[['r1','evidenceRecord','evidence0']];add('evidence-alias-counts-once',f,True)
    f=copy.deepcopy(f);f['entities']['otherrecord']='SourceRecord';f['aliases']=[['r1','evidenceRecord','otherrecord']];add('evidence-alias-not-subset',f,False,'ALIAS')
    f=template('ContextualMedicineClassificationAssignment');f['aliases']=[['r1','contextClassificationProduct','subject0'],['r1','contextClassificationEntry','entry0']];add('contextual-aliases-subset',f,True)
    for name in DEFERRED:
        f=template('FacilityOperation');f['entities']['deferred']=name;add('deferred-'+name,f,False,'DEFERRED')
    for label,edges,valid in [('geo-chain',[['g1','g2'],['g2','g3']],True),('geo-self',[['g1','g1']],False),('geo-two-cycle',[['g1','g2'],['g2','g1']],False),('geo-three-cycle',[['g1','g2'],['g2','g3'],['g3','g1']],False)]:
        f=template('FacilityOperation');f['entities'].update({x:'AdministrativeRegion' for x in ['g1','g2','g3']});f['geo']=edges;add(label,f,valid,None if valid else 'CYCLE')
    f=template('FacilityOperation');f['entities']['idle']='Organization';add('organization-without-any-role-or-authorization',f,True)
    f=copy.deepcopy(f);f['roles']=[['idle','OperatingOrganizationRole']];add('role-without-grounding-relation',f,False,'GROUNDING')
    return cases

def run_cqs(db,g):
    checks=[]
    for profile,slots in PROFILES.items():
        for slot,d in slots.items():
            sql=set(db.execute('SELECT p.relator_id,p.entity_id FROM participation p JOIN relator r ON r.id=p.relator_id WHERE r.type=? AND p.slot=?',(profile,slot)))
            rdf={(str(r).removeprefix(str(LAB)),str(e).removeprefix(str(LAB))) for r,e in g.query(f'SELECT DISTINCT ?r ?e WHERE {{ ?r a <{CM[profile]}>; <{CM[d["property"]]}> ?e . }}')}
            checks.append(sql==rdf)
    return all(checks),len(checks)

def main():
    DEST.mkdir(parents=True,exist_ok=True);ontology=Graph().parse(OUT/'active.ttl');s=shapes();s.serialize(DEST/'admission-shapes.ttl',format='turtle')
    (DEST/'schema.sql').write_text(SCHEMA);(DEST/'validation.sql').write_text('\n\n'.join('-- '+k+'\n'+v+';' for k,v in QUERIES.items()))
    cases=fixtures();write_json(DEST/'fixtures.json',cases);results=[];positive_cqs=0;positive=Graph()
    for case in cases:
        db=database(case['fixture']);errs=validate_sql(db);g=rdf_export(db,ontology)
        conforms,report,detail=validate(g,shacl_graph=s,ont_graph=ontology,inference='none',advanced=True)
        ok=(not errs)==case['expected_valid'] and conforms==case['expected_valid']
        if case['expected_rule']:ok=ok and case['expected_rule'] in errs
        if case['expected_valid']:
            cq_ok,n=run_cqs(db,g);ok=ok and cq_ok;positive_cqs+=n
        results.append(dict(id=case['id'],expected_valid=case['expected_valid'],sql_errors=sorted(errs),shacl_conforms=bool(conforms),passed=bool(ok)))
        if not ok:
            print(case['id'],errs,detail[:2500])
        db.close()
    # A bounded temporal check: the role ends, while the bearer identity persists.
    f=template('FacilityOperation');db=database(f)
    before=rdf_export(db,ontology,'2026-12-31T23:59:59Z');after=rdf_export(db,ontology,'2027-01-01T00:00:00Z')
    temporal=(LAB.operator0,RDF.type,CM.OperatingOrganizationRole) in before and (LAB.operator0,RDF.type,CM.OperatingOrganizationRole) not in after and (LAB.operator0,RDF.type,CM.Organization) in after
    # Deliberately switch off each gate and check whether a sole-rule counterexample escapes.
    mutations=[]
    for rule in QUERIES:
        escaped=[]
        for c in cases:
            if c['expected_valid']:continue
            db=database(c['fixture'])
            if not validate_sql(db,disabled=rule):escaped.append(c['id'])
            db.close()
        mutations.append(dict(disabled_rule=rule,caught_by_suite=bool(escaped),escaped_invalid_cases=len(escaped),witness=escaped[0] if escaped else None))
    # One consistent synthetic witness per profile for external reasoners; prefix identities per fixture.
    for profile in PROFILES:
        db=database(template(profile));g=rdf_export(db,ontology)
        # Keep one directly inspectable/loadable relational witness alongside the larger JSON fixture suite.
        if profile=='FacilityOperation':
            (DEST/'example-facility-operation.sql').write_text('\n'.join(db.iterdump())+'\n')
        for a,b,c in g:
            rename=lambda x: URIRef(str(LAB)+profile+'/'+str(x)[len(str(LAB)):]) if isinstance(x,URIRef) and str(x).startswith(str(LAB)) and x not in {LAB.Source,LAB.Context,LAB.CompleteRelator} else x
            # Properties and lab vocabulary remain unchanged.
            positive.add((rename(a),b,rename(c) if isinstance(c,URIRef) and str(c).startswith(str(LAB)) and c not in {LAB.Source,LAB.Context,LAB.CompleteRelator} else c))
    positive.serialize(DEST/'positive-witnesses.ttl',format='turtle')
    # Exclude lab annotation vocabulary from OWL reasoning, preserving ontology assertions.
    reasoner_data=Graph()
    for a,b,c in positive:
        if str(b).startswith(str(LAB)) or (b==RDF.type and str(c).startswith(str(LAB))):continue
        reasoner_data.add((a,b,c))
    for t in ontology:reasoner_data.add(t)
    reasoner_data.serialize(DEST/'reasoner-input.rdf',format='xml')
    out=dict(scope='Synthetic complete-instance admission under the approved G1 contract; not held-out validation or full OntoUML semantics',case_count=len(cases),valid_cases=sum(c['expected_valid'] for c in cases),invalid_cases=sum(not c['expected_valid'] for c in cases),passed=sum(r['passed'] for r in results),failed=sum(not r['passed'] for r in results),sql_rdf_answer_comparisons=positive_cqs,temporal_boundary_passed=temporal,mutation_checks=mutations,results=results)
    write_json(DEST/'results.json',out)
    print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
    assert out['failed']==0 and temporal and all(m['caught_by_suite'] for m in mutations)

if __name__=='__main__':main()
