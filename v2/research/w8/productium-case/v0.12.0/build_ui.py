from pathlib import Path
import json
R=Path(__file__).resolve().parent
payload=json.loads((R/'generated/explorer-data.json').read_text())
model=(R/'explorer.mjs').read_text().replace('export function','function')
app=(R/'app.mjs').read_text().split('\n',1)[1].replace('export function','function')
encoded=json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')
bundle=model+'\n'+app+'\nconst DATA='+encoded+';\nmount(document,DATA,(brief,name)=>{const blob=new Blob([JSON.stringify(brief,null,2)],{type:"application/json"});const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});'
html=(R/'explorer-template.html').read_text().replace('/*__BUNDLE__*/',bundle)
(R/'CMPharmE_Evidence_Explorer_v0_12_0.html').write_text(html)
print('Standalone Explorer generated',len(html.encode()),'bytes')
