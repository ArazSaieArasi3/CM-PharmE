"""Three manually extracted public PRAC documentary witnesses, no patient data."""
from lab import *
from datetime import datetime,timezone
import urllib.request
URL='https://www.ema.europa.eu/en/documents/prac-recommendation/prac-recommendations-signals-adopted-31-august-3-september-2026-prac-meeting_en.pdf'
rows=[
 {'epitt':'20223','topic':'Oxacillin','topic_kind':'substance','signal':'DRESS','disposition':'product-information-update-recommended','page':3},
 {'epitt':'20308','topic':'Anakinra','topic_kind':'substance','signal':'Fulminant hepatitis','disposition':'additional-information-requested','page':5},
 {'epitt':'20300','topic':'Progestogens','topic_kind':'group-with-source-defined-membership','signal':'Meningioma','disposition':'no-action-at-this-stage','page':6}]
manifest=H/'source-manifest.json'
if not manifest.exists():
 raw=urllib.request.urlopen(URL,timeout=45).read();assert raw.startswith(b'%PDF')
 write('source-manifest.json',{'url':URL,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'retrieved_at':datetime.now(timezone.utc).isoformat(),'document':'EMA/PRAC/183502/2026','meeting':'2026-08-31/2026-09-03','publication_date':'2026-09-28','pages':[3,5,6],'pdf_archived_in_repository':False,'extraction':'Manual source reading; three purposively selected records, not an exhaustive extraction.'})
meta=json.loads(manifest.read_text());g=graph();doc=T.PRACDocument;typ(g,doc,C.SourceRecord);g.add((doc,ctx.B.sourceURL,Literal(URL,datatype=XSD.anyURI)));g.add((doc,ctx.B.sourceSHA256,Literal(meta['sha256'])))
checks=[]
def check(name,actual,want):checks.append({'name':name,'actual':actual,'expected':want,'pass':actual==want})
for row in rows:
 record=T['PRAC-row-'+row['epitt']];signal=T['PRAC-signal-'+row['epitt']];result=T['PRAC-result-'+row['epitt']]
 typ(g,record,C.SourceRecord);g.add((record,ctx.PROV.wasDerivedFrom,doc));typ(g,signal,C.Assertion);typ(g,result,C.Assertion)
 g.add((signal,L.citesSourceRecord,record));g.add((result,L.citesSourceRecord,record))
 for field in ['epitt','topic','signal','disposition']:
  subject=result if field=='disposition' else signal
  ctx.claim(g,T[row['epitt']+'-'+field],record,subject,D[field],Literal(row[field]),origin='source-extracted',pointer='EMA/PRAC/183502/2026#page='+str(row['page']))
 # This relation is our interpretation, not an explicit RDF relation in EMA's PDF.
 ctx.claim(g,T[row['epitt']+'-result-link'],record,result,L.pvResultSignal,signal,origin='mapping-interpretation',pointer='EMA/PRAC/183502/2026#page='+str(row['page']))
 if row['topic_kind']=='substance':
  substance=T['substance-'+row['topic']];typ(g,substance,C.PharmaceuticalSubstance);g.add((substance,RDFS.label,Literal(row['topic'])))
  ctx.claim(g,T[row['epitt']+'-topic-link'],record,signal,L.signalSubstance,substance,origin='mapping-interpretation',pointer='EMA/PRAC/183502/2026#page='+str(row['page']))
 else:check('group-not-forced-into-one-substance',len(list(g.objects(signal,L.signalSubstance))),0)
 answer=ctx.claim_answer(g,result,D.disposition,Literal(row['disposition']));check('disposition-'+row['epitt'],answer['status'],'SOURCE_REPORTED')
 answer=ctx.claim_answer(g,result,L.pvResultSignal,signal);check('interpreted-result-link-'+row['epitt'],answer['status'],'MAPPING_PROPOSED')
check('three-different-source-dispositions',len({r['disposition'] for r in rows}),3)
check('combined-shapes',admission(g)['conforms'],True)
hr=ctx.prev.hermit(full+g);check('hermit',hr['consistent'] and not hr['unsatisfiable_named_classes'],True)
z=g+Graph()
for row in rows:
 signal=T['PRAC-signal-'+row['epitt']];result=T['PRAC-result-'+row['epitt']]
 ctx.prev.not_type(z,signal,C.MedicineShortageSituation);ctx.prev.not_edge(z,result,L.pvResultSignal,signal)
 z.add((signal,L.causallyEstablished,Literal(False)))
hr2=ctx.prev.hermit(full+z);check('source-recommendation-without-materialized-link-or-causal-proof',hr2['consistent'],True)
save('prac-claims.ttl',g);write('prac-extraction.json',{'source':meta,'rows':rows,'status':'MANUAL_DOCUMENTARY_EXTRACTION','limits':['Three purposively chosen recommendations, not patient-level ICSRs or independent clinical assessment.','A no-action recommendation is not a claim of no risk.','Grouping progestogens as one PharmaceuticalSubstance was deliberately not forced; group membership needs a separate model.','No assessment occurrence/time, regulatory compliance, patient event or causal relation is inferred.','Field extractions and semantic mapping proposals are kept distinct.','Regulatory obligations must be version checked: EMA notes Regulation 2025/1466 changed the former signal-detection pilot; GVP IX alone is not a current legal implementation.']})
write('pv-results.json',{'checks':checks,'pass':sum(x['pass'] for x in checks),'total':len(checks),'claims':len(list(g.subjects(RDF.type,ctx.B.StructuredClaim))),'rows':len(rows),'hermit':hr,'countermodel':hr2,'causality_established':False})
print(json.dumps({'pass':sum(x['pass'] for x in checks),'total':len(checks),'claims':len(list(g.subjects(RDF.type,ctx.B.StructuredClaim)))}),flush=True)
assert all(x['pass'] for x in checks)
