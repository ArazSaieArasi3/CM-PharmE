import {search,inspect,exportBrief} from './explorer.mjs';
export function mount(document,data,download) {
 const $=id=>document.getElementById(id); let selected=data.products[0].id;
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
  $('unknowns').textContent='Manufacturer: not established · Distributor: not established · Regulatory approval: unknown';
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
  $('brief').value=JSON.stringify(exportBrief(data,id),null,2);renderList();
 }
 $('search').addEventListener('input',renderList);
 $('export').addEventListener('click',()=>{
  const brief=exportBrief(data,selected);$('brief').value=JSON.stringify(brief,null,2);
  if(download)download(brief,`CMPharmE_Research_Brief_${brief.product.ndc}_v0_12_0.json`);
 });
 select(selected);return {select,selected:()=>selected,brief:()=>exportBrief(data,selected)};
}
