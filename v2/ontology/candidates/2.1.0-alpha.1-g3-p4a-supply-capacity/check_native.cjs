// Native OntoUML schema and official parser check.
// node check_native.cjs ontouml.json /path/to/node_modules official-native-results.json
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const [input, modules, output] = process.argv.slice(2);
if (!input || !modules || !output) throw new Error('input, node_modules, output required');
// uniqid inside ontouml-js probes networkInterfaces; this sandbox does not expose it.
os.networkInterfaces = () => ({lo: [{address:'127.0.0.1',mac:'00:00:00:00:00:00'}]});
const from = name => require(path.resolve(modules, name));
const raw = fs.readFileSync(input,'utf8');
const schema = from('ontouml-schema');
const Ajv = from('ajv/dist/2020').default;
const addFormats = from('ajv-formats');
const ontouml = from('ontouml-js');
const ajv = new Ajv({allErrors:true,strict:false});
addFormats(ajv);
const validate = ajv.compile(schema);
const valid = validate(JSON.parse(raw));
let parsed=null, parseError=null;
try {
  const project=ontouml.serializationUtils.parse(raw);
  parsed={type:project.constructor.name,id:project.id,classes:project.classes?.length,
          elementCount:project.elements?.length};
} catch(e) {parseError={name:e.name,message:e.message};}
const result={
  tool_versions:{
    node:process.version,ontouml_js:from('ontouml-js/package.json').version,
    ontouml_schema:from('ontouml-schema/package.json').version,
    ajv:from('ajv/package.json').version
  },
  schema_valid:valid,schema_errors:validate.errors||[],
  official_parser:parsed,parser_error:parseError,
  pass:valid&&!!parsed&&!parseError
};
fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({pass:result.pass,schema_errors:result.schema_errors.length,parsed,parseError}));
if(!result.pass)process.exitCode=1;
