// Software-product declarations are deliberately separate from pharmaceutical records.
export async function mountWorkbench(document,request,download,application) {
 const $=id=>document.getElementById(id);let context,selectedRecord=null;
 const show=(id,value)=>$(id).textContent=typeof value==='string'?value:JSON.stringify(value,null,2);
 const button=(title,fn)=>{const b=document.createElement('button');b.textContent=title;b.addEventListener('click',fn);return b;};
 async function reload(){
  const rows=await request('/api/history');$('ledger-history').replaceChildren();
  show('ledger-count',`${rows.length} recent attempts. Rejected and review-required attempts never populate the accepted graph.`);
  for(const row of rows){
   const item=document.createElement('div');item.className='ledger-row';
   item.append(button(`${row.request_id} · ${row.status}`,async()=>{
    selectedRecord=await request('/api/record?id='+encodeURIComponent(row.request_id));
    show('ledger-result',selectedRecord);application.setDeclaration(selectedRecord);
   }));$('ledger-history').append(item);
  }
 }
 try {
  context=await request('/api/context');application.setBuild(context.build);
  show('software-build',`Explorer ${context.version} · Build ${context.build.build_sha256.slice(0,12)} · Pharma data remains unchanged.`);
  function example(kind){
   const id=globalThis.crypto?.randomUUID?.()||String(Date.now());
   const root=`urn:cm-pharme:scenario:${id}:`;const v=context.build.software_version_iri;
   const t={before_r:root+'r1',after_r:root+'r1',before_v:v,after_v:v,before_c:root+'c1',after_c:root+'c1',operation:'restart',system_continuity:'PRESERVED',disposition_continuity:'PRESERVED',branching:false,evidence:root+'operator-note'};
   if(kind==='upgrade'){t.operation='upgrade';t.after_v=root+'proposed-version';t.after_r=root+'r2';t.after_c=root+'c2';}
   if(kind==='review')t.system_continuity='UNKNOWN';
   $('transition-input').value=JSON.stringify({request_id:'attempt-'+id,workspace:'case-'+id,mode:'SCENARIO',transition:t},null,2);
  }
  $('sample-restart').addEventListener('click',()=>example('restart'));
  $('sample-upgrade').addEventListener('click',()=>example('upgrade'));
  $('sample-review').addEventListener('click',()=>example('review'));
  $('submit-transition').addEventListener('click',async()=>{
   const b=$('submit-transition');b.disabled=true;
   try {
    const value=JSON.parse($('transition-input').value);
    const result=await request('/api/transitions',{method:'POST',headers:{'Content-Type':'application/json','X-Explorer-Token':context.token},body:JSON.stringify(value)});
    show('ledger-result',result);selectedRecord=null;application.setDeclaration(null);
    if(result.request_id){selectedRecord=await request('/api/record?id='+encodeURIComponent(result.request_id));application.setDeclaration(selectedRecord);}
    await reload();
   } catch(error){show('ledger-result','Could not record: '+error.message);}finally{b.disabled=false;}
  });
  $('export-ledger').addEventListener('click',()=>{
   if(selectedRecord)download(selectedRecord,`Explorer_Declaration_${selectedRecord.declaration.request_id}.json`);
   else show('ledger-result','Select a recorded attempt first.');
  });
  $('export-graph').addEventListener('click',async()=>{
   if(!selectedRecord)return show('ledger-result','Select a recorded attempt first.');
   const ws=selectedRecord.declaration.workspace;
   const nt=await request('/api/graph?workspace='+encodeURIComponent(ws),{raw:true});
   download(nt,`Explorer_Accepted_${ws}.nt`,'application/n-triples');
  });
  example('restart');await reload();
 } catch(error){show('software-build','Start the local service with python server.py to use the deployment workbench. The pharmaceutical Explorer remains available.');$('submit-transition').disabled=true;}
}
