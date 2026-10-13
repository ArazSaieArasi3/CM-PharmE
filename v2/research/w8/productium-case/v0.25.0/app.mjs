import {search,inspect,exportBrief} from './explorer.mjs';
export function mount(document,data,download) {
 const $=id=>document.getElementById(id); let selected=data.products[0].id; let build=null,declaration=null;
 const brief=()=>({...exportBrief(data,selected),schema_version:'0.25.0',application_build:build,software_declaration:declaration,software_declaration_scope:'Separate operator declaration; not a pharmaceutical identity or approval assertion.'});
 const text=(tag,value)=>{const e=document.createElement(tag);e.textContent=value;return e;};
 const line=(root,title,value)=>{const p=text('p','');p.append(text('strong',title+': '),document.createTextNode(value));root.append(p);};
 const policy=data.policy;
 $('summary').textContent=`${data.statistics.source_rows} source product records · ${data.statistics.package_projections} package projections · ${data.statistics.rdf_triples} RDF triples`;
 $('scope').textContent='Historical openFDA query extract. Listing information is source-reported; domain acceptance is pending.';
 $('snapshot').textContent=`CM-PharmE ${policy.cm_commit.slice(0,12)} · Source retrieved ${policy.source_retrieved_at}`;
 function renderList(){
  const rows=search(data,$('search').value);$('results').replaceChildren();$('count').textContent=`${rows.length} of ${data.products.length} product records`;
  for(const p of rows){const b=text('button',`${p.name} · ${p.ndc}`);b.setAttribute('aria-current',String(p.id===selected));b.addEventListener('click',()=>select(p.id));$('results').append(b);}
  if(!rows.length)$('results').append(text('p','No matching source record. This does not establish absence in the market.'));
 }
 function select(id){
  selected=id;const {product:p,relations}=inspect(data,id);
  $('name').textContent=p.name;$('generic').textContent=p.generic_name;$('identity').textContent=p.id;
  $('organization').textContent=p.organization_name;
  $('role').textContent='Organization «Kind» · Listing responsible organization «Role» (source-scoped)';
  $('unknowns').textContent='Manufacturing activity: not established · Wholesale distribution: not established · Regulatory approval: unknown';
  const evidence=brief().role_evidence;$('role-evidence').replaceChildren();
  if(evidence.labeler.status!=='SOURCE_REPORTED_LISTING_RESPONSIBILITY')$('role').textContent='Organization projection requires source review';
  line($('role-evidence'),'Source labeler',evidence.labeler.name||'Not reported');
  line($('role-evidence'),'Listing responsibility',evidence.labeler.status);
  line($('role-evidence'),'Reported manufacturer-name field',evidence.harmonized_manufacturer.observations.map(x=>x.value).join(' | ')||'Not reported');
  line($('role-evidence'),'Field relationship',evidence.harmonized_manufacturer.comparison_to_labeler);
  for(const observation of evidence.harmonized_manufacturer.observations)line($('role-evidence'),'Field evidence',observation.json_pointer||'Source locator missing');
  line($('role-evidence'),'Interpretation',evidence.interpretation);
  if(evidence.review_reasons.length)line($('role-evidence'),'Review needed',evidence.review_reasons.join('; '));
  $('relations').replaceChildren();
  for(const r of relations){const pack=p.packages.find(x=>x.id===r.presentation);const a=text('article','');a.className='package';
   a.append(text('h3',pack.ndc),text('p',pack.description));
   line(a,'Reported relationship','Medicinal product ← presentationOf ← Presentation ← listingPresentation ← Market listing → listingResponsibleOrganization → Organization');
   line(a,'Evidence',r.source_pointer||'Source missing');line(a,'Source record',r.source_record||'Source missing; this does not establish that the relationship is false.');
   line(a,'Package marketing start',pack.package_marketing_start||'Not reported');
   line(a,'Product marketing start',p.product_marketing_start||'Not reported');
   line(a,'Conclusion',r.status+'; approval UNKNOWN');$('relations').append(a);
  }
  $('source-json').textContent=JSON.stringify(p.source_envelope,null,2);
  $('source-pointer').textContent=p.source_pointer;
  $('source-hash').textContent=policy.raw_source_sha256;
  $('brief').value=JSON.stringify(brief(),null,2);renderList();
 }
 $('search').addEventListener('input',renderList);
 $('export').addEventListener('click',()=>{
  const output=brief();$('brief').value=JSON.stringify(output,null,2);
  if(download)download(output,`CMPharmE_Research_Brief_${output.product.ndc}_v0_25_0.json`);
 });
 select(selected);return {select,selected:()=>selected,brief,setBuild:value=>{build=value;$('brief').value=JSON.stringify(brief(),null,2)},setDeclaration:value=>{declaration=value;$('brief').value=JSON.stringify(brief(),null,2)}};
}
