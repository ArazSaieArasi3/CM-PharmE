#!/usr/bin/env python3
"""Bounded structural audit with explicit unresolved results."""
import json
from itertools import combinations
from rdflib import Graph, URIRef, Literal, RDF, RDFS, OWL
from rdflib.collection import Collection
from g1_model import BASE, OUT, CM, META, PROFILES, ROLES, MIXINS, DEFERRED, write_json

def ancestors(g,c):
    seen=set();todo=[c]
    while todo:
        x=todo.pop()
        for y in g.objects(x,RDFS.subClassOf):
            if isinstance(y,URIRef) and y not in seen:seen.add(y);todo.append(y)
    return seen

def topology(g):
    vertices={x for x in g.subjects(RDF.type,OWL.Class) if isinstance(x,URIRef)};edges=set()
    for a,b in g.subject_objects(RDFS.subClassOf):
        if a in vertices and b in vertices:edges.add((a,b))
    for p in g.subjects(RDF.type,OWL.ObjectProperty):
        a=g.value(p,RDFS.domain);b=g.value(p,RDFS.range)
        if a in vertices and b in vertices:edges.add((a,b))
    adj={x:set() for x in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    rest=set(vertices);components=[]
    while rest:
        todo=[rest.pop()];seen=set(todo)
        while todo:
            x=todo.pop()
            for y in adj[x]-seen:seen.add(y);rest.discard(y);todo.append(y)
        components.append(seen)
    return dict(metric='Named class graph: named subclass edges and named domain-range object-property edges; no datatypes, existential restrictions, anonymous unions or inferred semantics',classes=len(vertices),components=len(components),largest_component=max(map(len,components)),isolates=sorted(str(x).split('/')[-1] for x in vertices if not adj[x]))

def main():
    g=Graph().parse(OUT/'active.ttl');old=Graph()
    for p in (BASE/'modules').glob('*.ttl'):old.parse(p)
    kinds=set(g.subjects(META.ontoumlStereotype,Literal('Kind')))
    identity=[]
    for role,d in ROLES.items():
        found=ancestors(g,CM[role])&kinds;identity.append(dict(role=role,identity_providers=sorted(str(x).split('/')[-1] for x in found),pass_=found=={CM[d['identity']]}))
    mixins=[]
    for m,children in MIXINS.items():
        found=set().union(*(ancestors(g,CM[c])&kinds for c in children));mixins.append(dict(name=m,identity_provider_count=len(found),pass_=len(found)>=2))
    distinct=set()
    for a,b in g.subject_objects(OWL.disjointWith):distinct.add(frozenset([a,b]))
    for n in g.subjects(RDF.type,OWL.AllDisjointClasses):
        distinct.update(frozenset(x) for x in combinations(Collection(g,g.value(n,OWL.members)),2))
    pairs=json.loads((OUT/'contract.json').read_text())['protected_distinctions']
    protected=[dict(pair=p,pass_=frozenset(CM[x] for x in p) in distinct) for p in pairs]
    mediation=[]
    for profile,slots in PROFILES.items():
        if profile=='ContextualMedicineClassificationAssignment':continue
        mediation.append(dict(profile=profile,minimum_participants=sum(d['min'] for d in slots.values()),all_ends_anti_rigid=all(str(g.value(CM[d['target']],META.ontoumlStereotype)) in ['Role','RoleMixin'] for d in slots.values()),local_exclusion=all((CM[a['property']],OWL.propertyDisjointWith,CM[b['property']]) in g or (CM[b['property']],OWL.propertyDisjointWith,CM[a['property']]) in g for a,b in combinations(slots.values(),2))))
    statuses={
      'BinOver':('SCOPED_TESTS_PASS','Strict geographic containment rejects self and longer cycles. Other binary relations require G3 review.'),
      'DecInt':('REVIEW','No complete global intersection/generalization-set analysis.'),
      'DepPhase':('NOT_APPLICABLE_TO_DECLARED_MODEL','No Phase stereotype.'),
      'FreeRole':('PARTIAL','Approved role refinements have dependence; nine inherited role definitions still need disposition.'),
      'GSRig':('PARTIAL','New RoleMixin generalization sets contain anti-rigid roles; inherited sets incomplete.'),
      'HetColl':('NO_TYPED_OCCURRENCE','No memberOf stereotype in this projection; not a mereology certificate.'),
      'HomoFunc':('NO_TYPED_OCCURRENCE','No componentOf stereotype in this projection.'),
      'ImpAbs':('REVIEW','Native upper bounds remain unresolved outside approved mediations.'),
      'MixIden':('SCOPED_CHECKS_PASS','Eight refined RoleMixin families span multiple Kind identities; deferred families inactive.'),
      'MixRig':('SCOPED_CHECKS_PASS','New Role subtypes remain anti-rigid; no actor cast for Product.'),
      'MultDep':('REVIEW','Multiple-dependence intent needs global source/context review.'),
      'PartOver':('NO_TYPED_OCCURRENCE','No part-whole stereotypes; missing relation typing limits conclusion.'),
      'RelComp':('REVIEW','Composition constraints not exhaustively validated.'),
      'RelOver':('SCOPED_TESTS_PASS','Local participant exclusion and cross-context role overlap tested; global findings not certified.'),
      'RelRig':('APPROVED_PAIRS_REFACTORED','15 registered rigid-end questions addressed through anti-rigid participant patterns; no official detector run.'),
      'RelSpec':('SCOPED_TESTS_PASS','Evidence/context aliases subset generic participant positions; other relation specializations need review.'),
      'RepRel':('SCOPED_TESTS_PASS','Different agreements can share participants; identity is relation ID plus justified source/context, not a participant-pair unique key.'),
      'UndefFormal':('REVIEW','36 inherited/alias relations require stereotype and/or multiplicity disposition.'),
      'UndefPhase':('NOT_APPLICABLE_TO_DECLARED_MODEL','No Phase stereotype.'),
      'WholeOver':('NO_TYPED_OCCURRENCE','No whole-part stereotype; not an exhaustive semantic proof.')}
    report=dict(identity_checks=identity,role_mixin_checks=mixins,protected_distinctions=protected,mediation_checks=mediation,topology_before=topology(old),topology_after=topology(g),catalogue=[dict(name=k,status=v[0],rationale=v[1]) for k,v in statuses.items()],official_detector='NOT_RUN',full_conformance='NOT_ESTABLISHED')
    write_json(OUT/'structural-audit.json',report)
    assert all(x['pass_'] for x in identity+mixins+protected)
    assert all(x['minimum_participants']>=2 and x['all_ends_anti_rigid'] and x['local_exclusion'] for x in mediation)
    print(json.dumps({k:v for k,v in report.items() if k in ['topology_before','topology_after','full_conformance']},indent=2))

if __name__=='__main__':main()
