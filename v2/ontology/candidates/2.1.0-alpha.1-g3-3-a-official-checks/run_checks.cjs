// Usage: node run_checks.cjs <flat-ontouml.json> <current-node_modules> <legacy-node_modules> <output-dir>
// Install the pinned packages in distinct node_modules trees:
// current: ontouml-js@1.0.0 ontouml-schema@1.0.2 ajv@8.20.0 ajv-formats
// legacy:  ontouml-js@0.4.1
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const [input, currentDir, legacyDir, outputDir] = process.argv.slice(2);
if (!input || !currentDir || !legacyDir || !outputDir) throw Error('Four arguments required');
// uniqid queries networkInterfaces; the sandbox disables this read. No model data is changed.
os.networkInterfaces = () => ({lo:[{address:'127.0.0.1',mac:'00:00:00:00:00:00'}]});
const from = (dir, pkg) => require(path.resolve(dir, pkg));
const lib = from(currentDir, 'ontouml-js');
const schema = from(currentDir, 'ontouml-schema');
const Ajv = from(currentDir, 'ajv/dist/2020').default;
const addFormats = from(currentDir, 'ajv-formats');
const old = from(legacyDir, 'ontouml-js');
const raw = fs.readFileSync(input, 'utf8');
const source = JSON.parse(raw);
const ajv = new Ajv({allErrors:true,strict:false});
addFormats(ajv);
const validate = ajv.compile(schema);
const schemaValid = validate(source);
let parsed = null, parseError = null;
try {
  const p = lib.serializationUtils.parse(raw);
  parsed = {type:p.constructor.name,id:p.id,classes:p.classes?.length};
} catch(e) { parseError = {name:e.name,message:e.message}; }
const schemaResult = {
  tool_versions: {
    node: process.version,
    ontouml_js: from(currentDir,'ontouml-js/package.json').version,
    ontouml_schema: from(currentDir,'ontouml-schema/package.json').version,
    ajv: from(currentDir,'ajv/package.json').version
  },
  schema_valid:schemaValid,schema_errors:validate.errors,parsed,parse_error:parseError
};
const notes = new Set(source.elements.filter(e=>e.type==='Note').map(e=>e.id));
const all = new Map(source.elements.filter(e=>e.type!=='Note').map(e=>[e.id,e]));
function ref(id) {
  const e = all.get(id);
  return e ? {type:e.type==='BinaryRelation'?'Relation':e.type,id} : null;
}
function nest(id) {
  const e = all.get(id);
  if (!e) throw Error('Unresolved element '+id);
  const n = {...e,type:e.type==='BinaryRelation'?'Relation':e.type};
  if (n.type==='Package') n.contents=n.contents.filter(x=>!notes.has(x)).map(nest).filter(x=>x.type!=='Property');
  if (n.type==='Relation' || n.type==='Class') n.properties=(n.properties||[]).map(nest);
  if (n.type==='Generalization') {n.general=ref(n.general);n.specific=ref(n.specific);}
  if (n.type==='GeneralizationSet') n.generalizations=(n.generalizations||[]).map(ref);
  if (n.type==='Property') {
    if (n.propertyType) n.propertyType=ref(n.propertyType);
    n.subsettedProperties=(n.subsettedProperties||[]).map(ref);
    n.redefinedProperties=(n.redefinedProperties||[]).map(ref);
  }
  return n;
}
const projected = {...source,model:nest(source.root)};
delete projected.elements;delete projected.root;
const oldProject = old.serializationUtils.parse(JSON.stringify(projected),false);
const legacy = new old.OntoumlVerification(oldProject,null).run();
const rows = legacy.result.map(x=>({
  code:x.code,severity:x.severity,source_id:x.data.source.id,description:x.description
}));
fs.mkdirSync(outputDir,{recursive:true});
fs.writeFileSync(path.join(outputDir,'official-parser-schema-results.json'),JSON.stringify(schemaResult,null,2)+'\n');
fs.writeFileSync(path.join(outputDir,'legacy-verifier-findings.json'),JSON.stringify({
  tool:'ontouml-js OntoumlVerification',version:from(legacyDir,'ontouml-js/package.json').version,
  projection:{renamed_relation_type:'BinaryRelation -> Relation',nested_flat_elements:true,omitted_notes:notes.size,original_elements:source.elements.length,projected_elements:all.size},
  counts:Object.fromEntries([...new Set(rows.map(x=>x.code))].map(k=>[k,rows.filter(x=>x.code===k).length])),
  issues:rows
},null,2)+'\n');
fs.writeFileSync(path.join(outputDir,'legacy-projection.json'),JSON.stringify(oldProject,null,2)+'\n');
console.log(JSON.stringify({schema_valid:schemaValid,parsed,legacy_issue_count:rows.length}));
