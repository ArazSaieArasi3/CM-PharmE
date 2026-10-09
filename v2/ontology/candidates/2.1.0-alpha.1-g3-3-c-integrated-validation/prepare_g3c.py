"""Align the G3-2e-F OWL projection with the approved B2 native hierarchy."""
import json
import shutil
import sys
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL
from rdflib.compare import isomorphic
from rdflib.term import URIRef

native_path, source_owl, source_shapes, out = map(Path, sys.argv[1:5])
out.mkdir(parents=True, exist_ok=True)
native = json.loads(native_path.read_text())
text = source_owl.read_text()
old = ("cmpe:ListingResponsibleOrganizationRole a owl:Class ;\n"
       "    rdfs:subClassOf [ a owl:Restriction ;")
assert text.count(old) == 1
start = text.index(old)
end = text.index("ns1:ontoumlStereotype \"Role\" .", start)
snippet = text[start:end]
assert snippet.count("        cmpe:Organization,\n") == 1
text = text[:start] + snippet.replace("        cmpe:Organization,\n", "", 1) + text[end:]
target = out / "active.ttl"
target.write_text(text)
shutil.copyfile(source_shapes, out / "constraints.ttl")

CM = Namespace("https://w3id.org/cm-pharme/2.1/")
before, after = [Graph().parse(path, format="turtle") for path in (source_owl, target)]
assert len(before) - len(after) == 1
removed = (CM.ListingResponsibleOrganizationRole, RDFS.subClassOf, CM.Organization)
assert removed in before and removed not in after
assert (CM.ListingResponsibleOrganizationRole, RDFS.subClassOf, CM.ProductResponsibleLabelerRole) in after
assert (CM.ProductResponsibleLabelerRole, RDFS.subClassOf, CM.Organization) in after
after.add(removed)
assert isomorphic(before, after)
after.remove(removed)
classes = {e["id"] for e in native["elements"] if e["type"] == "Class"}
datatype_names = {e["id"] for e in native["elements"] if e["type"] == "Class" and e["stereotype"] == "datatype"}
assert {str(x).split("/")[-1] for x in after.subjects(RDF.type, OWL.Class) if isinstance(x, URIRef) and str(x).startswith(str(CM))} == classes - datatype_names
assert {str(x).split("/")[-1] for x in after.subjects(RDF.type, RDFS.Datatype) if str(x).startswith(str(CM))} == datatype_names
native_edges = {(e["specific"], e["general"]) for e in native["elements"] if e["type"] == "Generalization" and e["specific"] in classes and e["general"] in classes}
owl_edges = {(str(s).split("/")[-1], str(o).split("/")[-1]) for s, o in after.subject_objects(RDFS.subClassOf) if isinstance(s, URIRef) and isinstance(o, URIRef) and str(s).startswith(str(CM)) and str(o).startswith(str(CM))}
assert native_edges == owl_edges, {"native_only": sorted(native_edges - owl_edges), "owl_only": sorted(owl_edges - native_edges)}
native_relations = {e["name"]["en"] for e in native["elements"] if e["type"] == "BinaryRelation"}
owl_object_properties = {str(x)[len(str(CM)):] for x in after.subjects(RDF.type, OWL.ObjectProperty) if str(x).startswith(str(CM))}
assert native_relations == owl_object_properties
print(json.dumps({"native_elements":len(native["elements"]),"native_classes":len(classes),
                  "native_class_generalizations":len(native_edges),"owl_named_classes":len(classes-datatype_names),
                  "owl_datatypes":len(datatype_names),"native_and_owl_relations":len(native_relations),
                  "owl_triples_before":len(before),"owl_triples_after":len(after),
                  "direct_hierarchy_aligned":True,"approved_removed_edge":"ListingResponsibleOrganizationRole -> Organization"}))
