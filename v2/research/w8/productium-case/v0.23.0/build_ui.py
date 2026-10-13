from pathlib import Path
import json
R=Path(__file__).resolve().parent
payload=json.loads((R/'generated/explorer-data.json').read_text())
model=(R/'explorer.mjs').read_text().replace('export function','function')
app=(R/'app.mjs').read_text().split('\n',1)[1].replace('export function','function')
workbench=(R/'workbench.mjs').read_text().replace('export async function','async function')
encoded=json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')
boot='''
function download(value,name,mime='application/json'){
 const content=typeof value==='string'?value:JSON.stringify(value,null,2);
 const url=URL.createObjectURL(new Blob([content],{type:mime}));
 const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
const application=mount(document,DATA,download);
async function request(url,options={}){
 if(!['http:','https:'].includes(location.protocol))throw Error('Local service required');
 const {raw,...init}=options;const r=await fetch(url,init);if(!r.ok)throw Error('Request failed ('+r.status+')');return raw?r.text():r.json();
}
mountWorkbench(document,request,download,application);
'''
bundle=model+'\n'+app+'\n'+workbench+'\nconst DATA='+encoded+';\n'+boot
(R/'Explorer_Workbench_v0_23_0.html').write_text((R/'explorer-template.html').read_text().replace('/*__BUNDLE__*/',bundle))
print('Explorer workbench built')
