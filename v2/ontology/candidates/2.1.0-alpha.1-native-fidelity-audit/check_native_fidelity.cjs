// Native round trip with an explicit loss ledger and fail-closed export guard.
// Original JSON is authoritative. This does not change the official library.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const os = require('node:os');
os.networkInterfaces = () => ({lo:[{address:'127.0.0.1',mac:'00:00:00:00:00:00'}]});
const [input, modules, output] = process.argv.slice(2);
const from = name => require(path.resolve(modules,name));
const api = from('ontouml-js');
const canonical = obj => JSON.stringify(sort(obj));
function sort(x) {
  if(Array.isArray(x)) return x.map(sort);
  if(x && typeof x === 'object') return Object.fromEntries(Object.keys(x).sort().map(k=>[k,sort(x[k])]));
  return x;
}
const hash = text => crypto.createHash('sha256').update(text).digest('hex');
const clone = x => JSON.parse(JSON.stringify(x));
function guard(original, serialized) {
  const repaired = clone(serialized), ledger = [];
  const before = new Map(original.elements.map(e=>[e.id,e]));
  const after = new Map(repaired.elements.map(e=>[e.id,e]));
  if(before.size!==original.elements.length || after.size!==repaired.elements.length || before.size!==after.size)
    throw new Error('Element identity/count drift');
  for(const id of before.keys()) if(!after.has(id)) throw new Error('Element identity drift: '+id);
  const pairs = [[original,repaired,'@project'], ...[...before].map(([id,e])=>[e,after.get(id),id])];
  for(const [src,dst,id] of pairs) for(const key of new Set([...Object.keys(src),...Object.keys(dst)])) {
    if(key==='elements') continue;
    const a=src[key],b=dst[key];
    if(canonical(a)===canonical(b)) continue;
    let reason;
    if(['created','modified'].includes(key) && typeof a==='string' && typeof b==='string' &&
        Number.isFinite(Date.parse(a)) && Date.parse(a)===Date.parse(b)) reason='equal-instant date lexical normalization';
    else if(src.type==='Property' && key==='isReadOnly' && a===null && b===false)
      reason='unknown boolean coerced to false: restore explicit source null';
    else if(id==='@project' && key==='customProperties' && a===null && !(key in dst))
      reason='omitted explicit-null project metadata';
    else throw new Error(`Unapproved drift ${id}.${key}`);
    ledger.push({id,field:key,before:a,after:b===undefined?'@MISSING':b,reason});
    dst[key]=clone(a);
  }
  // Ordering of identity-keyed project elements is restored explicitly.
  repaired.elements=original.elements.map(e=>after.get(e.id));
  if(canonical(original)!==canonical(repaired)) throw new Error('Unexplained residual drift');
  return {repaired,ledger};
}
const raw=fs.readFileSync(input,'utf8'), original=JSON.parse(raw);
api.serializationUtils.validate(original);
const parsed=api.serializationUtils.parse(raw);
const serialized=JSON.parse(api.serializationUtils.serialize(parsed));
const {repaired,ledger}=guard(original,serialized);
api.serializationUtils.validate(repaired);
const origBy=new Map(original.elements.map(e=>[e.id,e])), outBy=new Map(serialized.elements.map(e=>[e.id,e]));
const fields=['stereotype','restrictedTo','propertyType','cardinality','subsettedProperties','redefinedProperties','text'];
const preservation={};
for(const field of fields) {
  const eligible=original.elements.filter(e=>field in e);
  preservation[field]={total:eligible.length,unchanged:eligible.filter(e=>canonical(e[field])===canonical(outBy.get(e.id)[field])).length};
}
const trials=[];
function reject(name,edit) {
  const m=clone(serialized); edit(m,new Map(m.elements.map(e=>[e.id,e])));
  try {guard(original,m);trials.push({name,rejected:false,pass:false});}
  catch(e) {trials.push({name,rejected:true,error:e.message,pass:true});}
}
reject('event-coerced-to-kind',(m,d)=>d.get('RiskAssessmentActivity').stereotype='kind');
reject('situation-coerced-to-kind',(m,d)=>d.get('StockoutSituation').stereotype='kind');
reject('nature-removed',(m,d)=>d.get('SupplyCapacity').restrictedTo=[]);
reject('note-erased',(m,d)=>d.get('decision-RR-01').text=null);
reject('subsetting-reference-dropped',(m,d)=>d.get('end-evidenceRecord-target').subsettedProperties=[]);
reject('unknown-cardinality-defaulted',(m,d)=>d.get('end-evidenceRecord-target').cardinality='0..*');
reject('known-readonly-false-to-true',(m,d)=>d.get('end-classificationEntry-target').isReadOnly=true);
reject('unknown-readonly-null-to-true',(m,d)=>d.get('end-evidenceRecord-target').isReadOnly=true);
reject('element-dropped',(m,d)=>m.elements=m.elements.filter(e=>e.id!=='StockoutSituation'));
reject('unknown-field-injected',(m,d)=>d.get('SupplyCapacity').unexpectedField='lost');
const result={scope:'Serialization fidelity only, not Event/Situation semantics or full antipattern validation.',
  source_sha256:hash(raw), versions:{node:process.version,ontouml_js:from('ontouml-js/package.json').version,ontouml_schema:from('ontouml-schema/package.json').version},
  runtime_hashes:{ontouml_js:hash(fs.readFileSync(path.resolve(modules,'ontouml-js/dist/index.js'))),schema:hash(fs.readFileSync(path.resolve(modules,'ontouml-schema/dist/ontouml-schema.json')))},
  source_elements:original.elements.length,parsed_elements:serialized.elements.length,
  raw_roundtrip_exact:canonical(original)===canonical(serialized), raw_field_changes:ledger.length,ledger,
  readonly_unknown_to_false:ledger.filter(r=>r.field==='isReadOnly').length,
  events_preserved:original.elements.filter(e=>e.stereotype==='event' && canonical(e)===canonical({...outBy.get(e.id),created:e.created,modified:e.modified})).length,
  situations:original.elements.filter(e=>e.stereotype==='situation').length,preservation,
  guarded_roundtrip_canonical_equal:canonical(original)===canonical(repaired),guarded_export_written:false,
  canonical_source_sha256:hash(canonical(original)),canonical_guarded_sha256:hash(canonical(repaired)),
  refusal_cases:trials,refusal_pass:trials.filter(t=>t.pass).length,refusal_total:trials.length,
  caveat:'The in-memory official parsed model has defaulted booleans. Guard restores the serialized JSON using the original input; native decision checks must read original/guarded JSON, not the parsed booleans.'};
fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({elements:result.source_elements,changes:ledger.length,unknown_booleans:result.readonly_unknown_to_false,guarded_equal:result.guarded_roundtrip_canonical_equal,refusals:result.refusal_pass+'/'+result.refusal_total,preservation}));
if(!result.guarded_roundtrip_canonical_equal || trials.some(t=>!t.pass)) process.exitCode=1;
