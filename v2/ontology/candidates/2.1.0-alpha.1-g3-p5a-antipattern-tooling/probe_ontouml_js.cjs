// Reproducible API-surface qualification, not anti-pattern detection.
// node probe_ontouml_js.cjs <native-json> <node_modules> <output-json>
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
require('node:os').networkInterfaces=()=>({lo:[{address:'127.0.0.1',mac:'00:00:00:00:00:00'}]});
const [input,modules,output]=process.argv.slice(2);
if(!input||!modules||!output)throw Error('three arguments required');
const from=name=>require(path.resolve(modules,name));
const ont=from('ontouml-js');
const schema=from('ontouml-schema');
const Ajv=from('ajv/dist/2020').default;
const addFormats=from('ajv-formats');
const ajv=new Ajv({allErrors:true,strict:false});
addFormats(ajv);
const validate=ajv.compile(schema);
const raw=fs.readFileSync(input,'utf8');
const model=JSON.parse(raw);
const schemaValid=validate(model);
let parsed=null,parseError=null;
try {const project=ont.serializationUtils.parse(raw);
     parsed={type:project.constructor.name,classes:project.classes?.length,
             id:project.id};}
catch(e){parseError={name:e.name,message:e.message};}
const exportNames=Object.keys(ont);
const detectorExports=exportNames.filter(x=>/anti.?pattern|detector|verification|verify/i.test(x));
const report={scope:'Official native parser/schema and public ontouml-js API probe; not an anti-pattern detector run',
    model_sha256:crypto.createHash('sha256').update(raw).digest('hex'),
    model_elements:model.elements.length,
    versions:{node:process.version,ontouml_js:from('ontouml-js/package.json').version,
              ontouml_schema:from('ontouml-schema/package.json').version,
              ajv:from('ajv/package.json').version},
    schema_valid:schemaValid,schema_errors:validate.errors||[],
    parser:parsed,parser_error:parseError,
    public_exports:exportNames.length,public_detector_like_exports:detectorExports,
    OntoumlVerification_exported:typeof ont.OntoumlVerification==='function',
    conclusion:'No full 20-pattern detector is exposed by this installed public ontouml-js API; absence of an export does not prove no other engine exists.'};
fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({schema_valid:schemaValid,parser:parsed,
  detector_exports:detectorExports,export_count:exportNames.length}));
if(!schemaValid||parseError)process.exitCode=1;
