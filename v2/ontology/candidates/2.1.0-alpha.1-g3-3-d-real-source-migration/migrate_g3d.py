"""Bounded real NHIF source-row projection and full candidate SHACL admission."""
import collections
import base64
import csv
import gzip
import hashlib
import io
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from rdflib.namespace import DCTERMS, PROV, SKOS, XSD
from pyshacl import validate

manifest_path, shape_path, out = map(Path, sys.argv[1:4])
out.mkdir(parents=True,exist_ok=True)
manifest=json.loads(manifest_path.read_text())
CM=Namespace('https://w3id.org/cm-pharme/2.1/')
S=Namespace('https://w3id.org/cm-pharme/2.1/data/g3d/p1-19160825/')
SH=Namespace('http://www.w3.org/ns/shacl#')
shapes=Graph().parse(shape_path,format='turtle')
graph=Graph()
for prefix,ns in [('cmpe',CM),('g3d',S),('dct',DCTERMS),('prov',PROV),('skos',SKOS)]:graph.bind(prefix,ns)

def iri(category,*parts):
    token='|'.join(str(p).strip().casefold() for p in parts)
    return S[category+'/'+hashlib.sha256(token.encode('utf-8')).hexdigest()[:20]]

def typed(subject,*names):
    for name in names:graph.add((subject,RDF.type,CM[name]))

def label(subject,text):
    graph.add((subject,RDFS.label,Literal(text)))

dataset=S['dataset/nhif-outpatient']; release=S['release/zenodo-19160825']
typed(dataset,'Dataset');typed(release,'DatasetRelease')
graph.add((dataset,CM.hasDatasetRelease,release))
graph.add((release,DCTERMS.identifier,Literal('10.5281/zenodo.19160825')))
graph.add((release,DCTERMS.source,URIRef(manifest['record_url'])))
atc_scheme=S['scheme/atc-source-19160825']
nhif_scheme=S['scheme/nhif-product-code-19160825']
typed(atc_scheme,'ProductClassificationScheme'); typed(nhif_scheme,'IdentifierScheme','UsedIdentifierSchemeRole')
label(atc_scheme,'ATC classification reference as given by NHIF source')
label(nhif_scheme,'NHIF reimbursement product code (source-scoped)')

required=manifest['columns']
rows=[];rejects=[]
missing=collections.Counter()
for entry in manifest['strata']:
    b=(manifest_path.parent / entry['selected_file']).read_bytes()
    assert hashlib.sha256(b).hexdigest()==entry['selected_file_sha256']
    lines=b.splitlines(keepends=True)
    assert lines[0].decode('utf-8').strip().split(',')==required
    position=entry['first_selected_source_byte_offset']
    assert len(lines)-1==entry['selected_rows']
    for index,line in enumerate(lines[1:]):
        raw=line.decode('utf-8')
        row=next(csv.DictReader(io.StringIO(lines[0].decode('utf-8')+raw)))
        assert len(row)==19 and None not in row
        for k in required:
            if not row[k].strip():missing[k]+=1
        reason=[]
        essentials=['region_num','region_name','atc_code','atc_name','nhif_code','market_name',
                    'packaging','concentration','num_in_pack','icd_code','icd_name','period','part']
        reason.extend('MISSING:'+x for x in essentials if not row[x].strip())
        for key in ['patients_num','pack_num','costs_bgn','costs_eur']:
            try:
                amount=Decimal(row[key])
                if not amount.is_finite():raise ValueError('nonfinite')
            except (InvalidOperation,ValueError):reason.append('INVALID_DECIMAL:'+key)
        try:date.fromisoformat(row['period'])
        except ValueError:reason.append('INVALID_DATE:period')
        row_hash=hashlib.sha256(line).hexdigest()
        locator={'stratum':entry['stratum'],'selected_row_index':index,
                 'source_byte_offset':position,'row_sha256':row_hash}
        position+=len(line)
        if reason:
            rejects.append({**locator,'reason':reason})
        else:
            rows.append((locator,row))
assert len(rows)+len(rejects)==manifest['selected_rows_total']

row_resources={};products={};presentations={};regions={};entries={};diagnoses={}
nhif_presentations=collections.defaultdict(set)
atc_labels=collections.defaultdict(set)
for loc,row in rows:
    # Repeated source row contents are distinct source records at distinct bytes.
    h=hashlib.sha256(f"{loc['source_byte_offset']}|{loc['row_sha256']}".encode('ascii')).hexdigest()[:20]
    rec=S['source-record/'+h]
    typed(rec,'SourceRecord')
    graph.add((release,CM.containsSourceRecord,rec))
    graph.add((rec,DCTERMS.identifier,Literal(f"source-byte-{loc['source_byte_offset']};sha256-{loc['row_sha256']}")))
    region=iri('region',row['region_num'],row['region_name'])
    typed(region,'AdministrativeRegion');label(region,row['region_name'])
    graph.add((region,SKOS.notation,Literal(row['region_num'])))
    regions[region]=1
    prod=iri('source-product',row['nhif_code'],row['market_name'])
    typed(prod,'MedicinalProduct','ClassifiedMedicinalProductRole','ClassifiedEntity')
    label(prod,row['market_name'])
    products[prod]=1
    pres=iri('source-presentation',row['nhif_code'],row['market_name'],row['packaging'],row['concentration'],row['num_in_pack'])
    typed(pres,'MedicinalProductPresentation','IdentifiedMedicinalProductPresentationRole','IdentifiedEntity')
    graph.add((pres,CM.presentationOf,prod))
    graph.add((pres,DCTERMS.description,Literal(f"source packaging={row['packaging']}; concentration={row['concentration']}; units={row['num_in_pack']}")))
    presentations[pres]=1;nhif_presentations[row['nhif_code']].add(pres)
    identifier=iri('nhif-identifier-assignment',row['nhif_code'],str(pres))
    typed(identifier,'IdentifierAssignment')
    graph.add((identifier,CM.identifierEntity,pres))
    graph.add((identifier,CM.identifierScheme,nhif_scheme))
    graph.add((identifier,CM.identifierLexicalValue,Literal(row['nhif_code'],datatype=XSD.string)))
    graph.add((identifier,PROV.wasDerivedFrom,rec))
    atc=iri('atc-entry',row['atc_code'])
    typed(atc,'ClassificationEntry','AppliedClassificationEntryRole')
    label(atc,row['atc_name']);graph.add((atc,SKOS.notation,Literal(row['atc_code'])))
    graph.add((atc,CM.entryInScheme,atc_scheme))
    entries[atc]=1;atc_labels[row['atc_code']].add(row['atc_name'])
    assignment=iri('atc-classification-assignment',str(prod),row['atc_code'])
    typed(assignment,'ProductClassificationAssignment')
    graph.add((assignment,CM.classificationEntity,prod))
    graph.add((assignment,CM.classificationEntry,atc))
    graph.add((assignment,PROV.wasDerivedFrom,rec))
    diagnosis=iri('icd-reference',row['icd_code'],row['icd_name'])
    typed(diagnosis,'DiagnosisClassificationReference');label(diagnosis,row['icd_name'])
    graph.add((diagnosis,SKOS.notation,Literal(row['icd_code'])))
    diagnoses[diagnosis]=1
    generated=[]
    for field,unit in [('patients_num','patient count (aggregate)'),('pack_num','package count (aggregate)'),
                       ('costs_bgn','BGN'),('costs_eur','EUR')]:
        ob=S[f'observation/{h}/{field}']
        typed(ob,'ReimbursementUtilisationObservationResult','ObservationResult')
        graph.add((ob,CM.measureNumericValue,Literal(Decimal(row[field]),datatype=XSD.decimal)))
        graph.add((ob,CM.measureUnitLabel,Literal(unit,datatype=XSD.string)))
        graph.add((ob,CM.validFrom,Literal(row['period']+'T00:00:00Z',datatype=XSD.dateTime)))
        graph.add((ob,CM.observationAboutProduct,prod))
        graph.add((ob,CM.observationAboutPresentation,pres))
        graph.add((ob,CM.reimbursementDiagnosisContext,diagnosis))
        graph.add((ob,DCTERMS.spatial,region))
        graph.add((ob,PROV.wasDerivedFrom,rec))
        generated.append(ob)
    row_resources[loc['source_byte_offset']]={'source_record':rec,'observations':generated,
                                     'identifier_assignment':identifier,'classification_assignment':assignment}

def shacl_check(g):
    ok,report,_=validate(data_graph=g,shacl_graph=shapes,advanced=True,inference='none',abort_on_first=False)
    results=list(report.subjects(RDF.type,SH.ValidationResult))
    focus=sorted(set(str(report.value(r,SH.focusNode)) for r in results))
    kinds=collections.Counter((str(report.value(r,SH.sourceConstraintComponent)).split('#')[-1],
                               str(report.value(r,SH.resultMessage))[:100]) for r in results)
    return bool(ok),len(results),focus,kinds

conforms,violations,focus,kinds=shacl_check(graph)
assert conforms,(violations,focus[:4],kinds.most_common(8))
# SHACL full graph success allows every schema-accepted row to be admitted;
# if a future source slice fails, this script must fail rather than assign a
# misleading per-row success rate from a global report.
first=rows[0][0]['source_byte_offset'];witness=row_resources[first]
# Negative sensitivity uses the full graph so all reused scheme/entry nodes
# retain their other valid participants. Mutations target only a real row's nodes.
negatives=[]
def negative(name,add=None,remove=None):
    test=Graph()
    test+=graph
    if remove:test.remove(remove)
    if add:test.add(add)
    ok,n,fs,_=shacl_check(test)
    negatives.append({'case':name,'expected_conforms':False,'conforms':ok,
                      'validation_results':n,'sample_focus':fs[:3],'pass':not ok})
    assert not ok,name
negative('real_identifier_missing_scheme',remove=(witness['identifier_assignment'],CM.identifierScheme,nhif_scheme))
atc_target=next(graph.objects(witness['classification_assignment'],CM.classificationEntry))
negative('real_classification_missing_entry',remove=(witness['classification_assignment'],CM.classificationEntry,atc_target))
ob=witness['observations'][0]
prod=next(graph.objects(ob,CM.observationAboutProduct))
region=next(graph.objects(ob,DCTERMS.spatial))
test=Graph();test+=graph;test.remove((ob,CM.observationAboutProduct,prod));test.add((ob,CM.observationAboutProduct,region))
ok,n,fs,_=shacl_check(test);negatives.append({'case':'real_observation_wrong_product_type','expected_conforms':False,'conforms':ok,'validation_results':n,'sample_focus':fs[:3],'pass':not ok});assert not ok
negative('real_geography_self_containment',add=(region,CM.withinRegion,region))
pres=next(graph.objects(ob,CM.observationAboutPresentation))
negative('real_presentation_on_product_only_active_substance_relation',add=(pres,CM.productHasActiveSubstance,atc_target))

source=witness['source_record']
product=next(graph.objects(ob,CM.observationAboutProduct))
presentation=next(graph.objects(ob,CM.observationAboutPresentation))
diagnosis=next(graph.objects(ob,CM.reimbursementDiagnosisContext))
entry=next(graph.objects(witness['classification_assignment'],CM.classificationEntry))
witness_subjects={dataset,release,atc_scheme,nhif_scheme,source,product,presentation,diagnosis,region,entry,
                  witness['identifier_assignment'],witness['classification_assignment'],*witness['observations']}
witness_graph=Graph()
for subject in witness_subjects:
    for triple in graph.triples((subject,None,None)):
        if subject==release and triple[1]==CM.containsSourceRecord and triple[2]!=source:continue
        witness_graph.add(triple)
witness_ok,witness_violations,_,_=shacl_check(witness_graph)
assert witness_ok and not witness_violations
witness_path=out/'one-real-row-witness.ttl'
witness_graph.serialize(destination=witness_path,format='turtle')

# Every ABox term is named, so lexically sorted N-Triples is deterministic.
graph_path=out/'real-source-abox.nt'
nt_lines=graph.serialize(format='nt').splitlines()
assert len(nt_lines)==len(graph) and not any(line.startswith('_:') for line in nt_lines)
graph_path.write_text('\n'.join(sorted(nt_lines))+'\n')
compressed=gzip.compress(graph_path.read_bytes(),compresslevel=9,mtime=0)
compressed_path=out/'real-source-abox.nt.gz.b64'
compressed_path.write_text(base64.b64encode(compressed).decode('ascii')+'\n')
fields={k:'RDF_semantic_or_descriptive' for k in required}
for k in ['costs','part','currency']:fields[k]='raw_source_and_provenance_only'
for k in ['packaging','concentration','num_in_pack']:fields[k]='descriptive_presentation_text_only_not_formal_package_semantics'
fields['atc_name']='classification_label_only_not_confirmed_substance_identity'
result={"source_record":"10.5281/zenodo.19160825",
        "sample_scope":"five deterministic byte-range prefixes; 768 records, not representative of the whole source",
        "input":{"sampled_rows":manifest['selected_rows_total'],"schema_accepted":len(rows),
                 "preflight_rejected":len(rejects),"missing_cells":dict(missing),
                 "column_count":len(required),"field_projection_status":fields},
        "mapped":{"rdf_triples":len(graph),"source_records":len(row_resources),"reimbursement_metric_observations":len(rows)*4,
                  "product_nodes":len(products),"presentation_nodes":len(presentations),
                  "region_nodes":len(regions),"atc_entry_nodes":len(entries),"diagnosis_nodes":len(diagnoses),
                  "nhif_codes_with_multiple_presentation_keys":{k:len(v) for k,v in nhif_presentations.items() if len(v)>1},
                  "atc_codes_with_multiple_labels":{k:sorted(v) for k,v in atc_labels.items() if len(v)>1},
                  "asserted_pharmaceutical_substances":0,"asserted_product_active_substance_links":0,
                  "asserted_patient_individuals":0},
        "full_candidate_pyshacl":{"conforms":conforms,"validation_results":violations,"admitted_rows":len(rows) if conforms else None,
                                 "rejected_rows_by_full_graph":0 if conforms else None,
                                 "scope":"All shapes on the complete 768-row mapped graph, no RDFS/OWL inference"},
        "negative_sensitivity":{"cases":negatives,"passed":sum(x['pass'] for x in negatives)},
        "preflight_rejections":rejects,
        "abox":{"path":graph_path.name,"sha256":hashlib.sha256(graph_path.read_bytes()).hexdigest(),
                "compressed_base64_path":compressed_path.name,"compressed_gzip_sha256":hashlib.sha256(compressed).hexdigest(),
                "witness_path":witness_path.name,"witness_triples":len(witness_graph),"witness_pyshacl_conforms":witness_ok},
        "interpretation_limit":"No claim of full-source quality, external validity, clinical correctness, verified product/substance identity, unique patients or approved 29 relation/14 isolate/19 RepRel policies."}
(out/'migration-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({"rows":len(rows),"triples":len(graph),"shacl_conforms":conforms,
                  "negative_passed":sum(x['pass'] for x in negatives),
                  "products":len(products),"presentations":len(presentations),
                  "identifier_collisions":len(result['mapped']['nhif_codes_with_multiple_presentation_keys'])}))
