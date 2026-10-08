from pathlib import Path
import json
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD, BNode, Variable

CM = Namespace("https://w3id.org/cm-pharme/2.1/")
SH = Namespace("http://www.w3.org/ns/shacl#")
OWL_N = Namespace("http://www.w3.org/2002/07/owl#")
HERE = Path(__file__).resolve().parent
PREV = HERE.parent / "2.1.0-alpha.1-g3d-candidate"
BASE_OWL = PREV / "active.ttl" if (PREV / "active.ttl").exists() else HERE / "base.ttl"
BASE_SHAPES = PREV / "constraints.ttl" if (PREV / "constraints.ttl").exists() else HERE / "base-shapes.ttl"
OWL_FILE = HERE / "active.ttl" if (HERE / "active.ttl").exists() else HERE / "candidate.ttl"
SHAPES_FILE = HERE / "constraints.ttl" if (HERE / "constraints.ttl").exists() else HERE / "candidate-shapes.ttl"
base = Graph().parse(BASE_OWL, format="turtle")
owl = Graph().parse(OWL_FILE, format="turtle")
shapes = Graph().parse(SHAPES_FILE, format="turtle")
q = (HERE / "operates-snapshot.rq").read_text()
at = Literal("2026-10-08T12:00:00Z", datatype=XSD.dateTime)

def restriction(c, prop, target):
    for r in owl.objects(c, RDFS.subClassOf):
        if (r, OWL_N.onClass, target) not in owl:
            continue
        if (r, OWL_N.qualifiedCardinality, Literal(1, datatype=XSD.nonNegativeInteger)) not in owl:
            continue
        for x in owl.objects(r, OWL_N.onProperty):
            if (x, OWL_N.inverseOf, prop) in owl:
                return True
    return False

def obj(g,s,p,o):
    g.add((CM[s],CM[p],CM[o]))
def typ(g,s,t):
    g.add((CM[s],RDF.type,CM[t]))

def admission(g):
    problems=[]
    for s in g.subjects(CM.productHasActiveSubstance,None):
        if (s,RDF.type,CM.MedicinalProduct) not in g or (s,RDF.type,CM.MedicinalProductPresentation) in g:
            problems.append("PRODUCT_SCOPE")
        for v in g.objects(s,CM.productHasActiveSubstance):
            if (v,RDF.type,CM.PharmaceuticalSubstance) not in g:
                problems.append("SUBSTANCE_TYPE")
    for c in g.subjects(RDF.type,CM.EnterpriseCapability):
        bs=list(g.objects(c,CM.capabilityBearer))
        if len(bs)!=1 or any((b,RDF.type,CM.Organization) not in g for b in bs):
            problems.append("CAPABILITY_BEARER")
    for c in g.subjects(RDF.type,CM.MatchConfidence):
        bs=list(g.subjects(CM.hasMatchConfidence,c))
        if len(bs)!=1 or any((b,RDF.type,CM.EntityMatchAssertion) not in g for b in bs):
            problems.append("CONFIDENCE_BEARER")
    return sorted(set(problems))

def fixture():
    g=Graph()
    typ(g,"p","MedicinalProduct");typ(g,"s","PharmaceuticalSubstance");obj(g,"p","productHasActiveSubstance","s")
    typ(g,"p2","MedicinalProduct") # no mandatory substance
    typ(g,"org","Organization");typ(g,"org2","Organization")
    typ(g,"cap","EnterpriseCapability");obj(g,"cap","capabilityBearer","org")
    typ(g,"a","EntityMatchAssertion");typ(g,"a2","EntityMatchAssertion") # unscored
    typ(g,"conf","MatchConfidence");obj(g,"a","hasMatchConfidence","conf")
    return g

def operation_case(extra=None):
    g=Graph()
    typ(g,"r","FacilityOperation");typ(g,"o","OperatingOrganizationRole");typ(g,"o","Organization")
    typ(g,"f","OperatedFacilityRole");typ(g,"f","Facility")
    obj(g,"r","operationOrganization","o");obj(g,"r","operationFacility","f")
    g.add((CM.r,CM.validFrom,Literal("2026-10-01T00:00:00Z",datatype=XSD.dateTime)))
    if extra: extra(g)
    return g

def rows(g):
    return [(str(r.org),str(r.facility),str(r.operation)) for r in g.query(q,initBindings={"at":at})]

cases=[]
def check(name, condition):
    cases.append({"name":name,"pass":bool(condition)})

check("Turtle OWL parsed",len(owl)>len(base)>0)
check("Turtle SHACL parsed",len(shapes)>0)
check("Subproperty points to broad active substance",(CM.productHasActiveSubstance,RDFS.subPropertyOf,CM.hasActiveSubstance) in owl)
check("Product domain and substance range",(CM.productHasActiveSubstance,RDFS.domain,CM.MedicinalProduct) in owl and (CM.productHasActiveSubstance,RDFS.range,CM.PharmaceuticalSubstance) in owl)
check("Confidence exactly one assertion OWL restriction",restriction(CM.MatchConfidence,CM.hasMatchConfidence,CM.EntityMatchAssertion))
check("OWL preserves no universal confidence for assertions",not any((r,OWL_N.onProperty,CM.hasMatchConfidence) in owl and (CM.EntityMatchAssertion,RDFS.subClassOf,r) in owl for r in owl.subjects(OWL_N.onProperty,CM.hasMatchConfidence)))
check("Three new SHACL shapes",all((CM[n],RDF.type,SH.NodeShape) in shapes for n in ["ProductActiveSubstanceAdmissionShape","EnterpriseCapabilityBearerShape","MatchConfidenceBearerShape"]))

good=fixture()
check("Valid product, capacity and confidence; unscored assertion allowed",admission(good)==[])
g=fixture();typ(g,"pres","MedicinalProductPresentation");typ(g,"s2","PharmaceuticalSubstance");obj(g,"pres","productHasActiveSubstance","s2")
check("Presentation cannot use Product relation","PRODUCT_SCOPE" in admission(g))
g=fixture();obj(g,"p","productHasActiveSubstance","not_substance")
check("Untyped substance rejected","SUBSTANCE_TYPE" in admission(g))
g=fixture();obj(g,"cap","capabilityBearer","org2")
check("Capability with two bearers rejected","CAPABILITY_BEARER" in admission(g))
g=fixture();typ(g,"cap2","EnterpriseCapability")
check("Capability with no bearer rejected","CAPABILITY_BEARER" in admission(g))
g=fixture();obj(g,"a2","hasMatchConfidence","conf")
check("Confidence with two bearers rejected","CONFIDENCE_BEARER" in admission(g))
g=fixture();typ(g,"conf2","MatchConfidence")
check("Confidence with no bearer rejected","CONFIDENCE_BEARER" in admission(g))
check("Operation snapshot positive",len(rows(operation_case()))==1)
g=operation_case();g.add((CM.r,CM.validTo,Literal("2026-10-07T00:00:00Z",datatype=XSD.dateTime)))
check("Operation snapshot expired",len(rows(g))==0)
g=operation_case();g.set((CM.r,CM.validFrom,Literal("2026-10-09T00:00:00Z",datatype=XSD.dateTime)))
check("Operation snapshot future",len(rows(g))==0)
g=operation_case();g.remove((CM.r,CM.validFrom,None))
check("Operation snapshot absent start",len(rows(g))==0)
g=operation_case();g.add((CM.r,CM.validFrom,Literal("2026-10-02T00:00:00Z",datatype=XSD.dateTime)))
check("Operation snapshot ambiguous start rejected",len(rows(g))==0)
g=operation_case();g.add((CM.r,CM.validTo,Literal("2026-10-12T00:00:00Z",datatype=XSD.dateTime)))
g.add((CM.r,CM.validTo,Literal("2026-10-15T00:00:00Z",datatype=XSD.dateTime)))
check("Operation snapshot ambiguous end rejected",len(rows(g))==0)
g=operation_case();obj(g,"r","operationFacility","f2")
check("Operation snapshot second facility rejected",len(rows(g))==0)
g=operation_case();g.remove((CM.o,RDF.type,CM.OperatingOrganizationRole))
check("Operation snapshot role absent",len(rows(g))==0)
g=operation_case();g.remove((CM.r,CM.operationFacility,CM.f))
check("Operation snapshot different relators do not cross join",len(rows(g))==0)
out={"rdflib_version":__import__("rdflib").__version__,"owl_triples_base":len(base),"owl_triples_candidate":len(owl),"shacl_triples_base":len(Graph().parse(BASE_SHAPES,format="turtle")),"shacl_triples_candidate":len(shapes),"cases":cases,"pass_count":sum(x["pass"] for x in cases),"case_count":len(cases),"all_pass":all(x["pass"] for x in cases),"scope":"RDFLib Turtle parse, graph checks and manually evaluated constraints equivalent to the three new SHACL shapes; NOT pySHACL or OWL DL reasoner."}
(HERE / "test-results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"pass_count":out["pass_count"],"case_count":out["case_count"],"all_pass":out["all_pass"],"failures":[c for c in cases if not c["pass"]],"triples":[len(base),len(owl),out["shacl_triples_base"],len(shapes)]}))
if not out["all_pass"]:
    raise SystemExit(1)

