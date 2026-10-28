const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),os=require('node:os');
os.networkInterfaces=()=>({lo:[{address:'127.0.0.1',mac:'00:00:00:00:00:00'}]});
const [input,modules,output]=process.argv.slice(2),from=n=>require(path.resolve(modules,n));
const api=from('ontouml-js');
function sort(x){if(Array.isArray(x))return x.map(sort);if(x&&typeof x==='object')return Object.fromEntries(Object.keys(x).sort().map(k=>[k,sort(x[k])]));return x;}
const canon=x=>JSON.stringify(sort(x)),clone=x=>JSON.parse(JSON.stringify(x));
const original=JSON.parse(fs.readFileSync(input,'utf8'));api.serializationUtils.validate(original);
const raw=JSON.parse(api.serializationUtils.serialize(api.serializationUtils.parse(JSON.stringify(original))));
const repaired=clone(raw),by=new Map(repaired.elements.map(e=>[e.id,e])),ledger=[];
if(by.size!==original.elements.length||repaired.elements.length!==original.elements.length)throw Error('Element count/identity drift');
for(const e of original.elements)if(!by.has(e.id))throw Error('Element identity drift');
for(const [id,src,dst] of [['@project',original,repaired],...original.elements.map(e=>[e.id,e,by.get(e.id)])]){
 for(const key of new Set([...Object.keys(src),...Object.keys(dst)])){
  if(key==='elements'||canon(src[key])===canon(dst[key]))continue;
  const a=src[key],b=dst[key];let reason;
  if(['created','modified'].includes(key)&&typeof a==='string'&&typeof b==='string'&&Number.isFinite(Date.parse(a))&&Date.parse(a)===Date.parse(b))reason='equal-instant date normalization';
  else if(src.type==='Property'&&key==='isReadOnly'&&a===null&&b===false)reason='restore source unknown Boolean';
  else if(id==='@project'&&key==='customProperties'&&a===null&&!(key in dst))reason='restore explicit-null project metadata';
  else throw Error('Unapproved serialization drift '+id+'.'+key);
  ledger.push({id,field:key,before:a,parsed_after:b===undefined?'@MISSING':b,reason});dst[key]=clone(a);
 }
}
repaired.elements=original.elements.map(e=>by.get(e.id));
if(canon(original)!==canon(repaired))throw Error('Guarded roundtrip differs');api.serializationUtils.validate(repaired);
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const result={passed:true,source_elements:original.elements.length,guarded_elements:repaired.elements.length,raw_roundtrip_equal:canon(original)===canon(raw),guarded_roundtrip_equal:true,restored_unknown_readonly:ledger.filter(x=>x.field==='isReadOnly').length,ledger,source_canonical_sha256:hash(canon(original)),guarded_canonical_sha256:hash(canon(repaired)),versions:Object.fromEntries(['ontouml-js','ontouml-schema','ajv','ajv-formats'].map(n=>[n,from(n+'/package.json').version])),runtime_sha256:{ontouml_js:hash(fs.readFileSync(path.resolve(modules,'ontouml-js/dist/index.js'))),schema:hash(fs.readFileSync(path.resolve(modules,'ontouml-schema/dist/ontouml-schema.json')))},full_antipattern_validation:false,scientific_acceptance:false};
fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');
