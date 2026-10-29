#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Collect converter forensics; never authorizes or changes a publication pin."""
import argparse,hashlib,json,os,shutil,subprocess,zipfile
from prepare_converter_build import prepare
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def inspect(p):
    with zipfile.ZipFile(p) as z:
        names=sorted(n for n in z.namelist() if not n.endswith('/'))
        assert len(names)==len(set(names)), 'Duplicate ZIP names'
        entries={n:sha(z.read(n)) for n in names}
        digests={}
        for label,sep,end in [('legacy_literal',b'\\0',b'\\n'),('binary_framing',b'\0',b'\n')]:
            h=hashlib.sha256()
            for n in names:h.update(n.encode());h.update(sep);h.update(z.read(n));h.update(end)
            digests[label]=h.hexdigest()
        texts={n:z.read(n).decode('utf-8',errors='replace') for n in names if n=='META-INF/MANIFEST.MF' or n.endswith('pom.properties')}
    return {'jar_sha256':sha(p.read_bytes()),'content_digests':digests,'entries':entries,'generated_text':texts}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    root=Path.cwd();source=a.source.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    def run(cmd,cwd,path):
        with path.open('w') as f:subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,check=True)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()=='2833ead00122ca252a0fd0e18c5e5b696d711d2c'
    run(['mvn','--version'],source,out/'maven-version.txt');run(['java','-version'],source,out/'java-version.txt')
    reports=[]
    for number in [1,2,3,4]:
        if number==3: overlay=prepare(source)
        command=['mvn','-B']+(['-f','pom.cmpe.xml'] if number>=3 else [])+['clean','package','-P','standalone-release','-DskipTests']
        run(command,source,out/f'build-{number}.log')
        jar=out/f'converter-{number}.jar';shutil.copyfile(source/'target/OWL2VOWL-0.3.7-shaded.jar',jar)
        reports.append(inspect(jar));write(out/f'entries-{number}.json',reports[-1])
    run(['mvn','-B','dependency:tree','-P','standalone-release'],source,out/'dependency-tree.txt')
    run(['mvn','-B','help:effective-pom','-P','standalone-release'],source,out/'effective-pom.txt')
    dependencies={str(p.relative_to(Path.home()/'.m2/repository')):sha(p.read_bytes()) for p in (Path.home()/'.m2/repository').rglob('*') if p.is_file() and p.suffix in {'.jar','.pom'}}
    write(out/'resolved-maven-files.json',dependencies)
    first,second=reports[:2];changed=[n for n in sorted(set(first['entries'])|set(second['entries'])) if first['entries'].get(n)!=second['entries'].get(n)]
    projection={};reg=json.loads((root/'docs/documentation/ontology-version-registry.json').read_text());contract=json.loads((root/'docs/documentation/ontology-documentation-build-contract.json').read_text())
    for v in reg['versions']:
        cfg=next(x for x in contract['versions'] if x['id']==v['id']);ttl=root/'build/input'/v['id']/cfg['build']['documentation_input_artifact'];outputs=[]
        for number in [1,2,3,4]:
            target=out/f'{v["id"]}-{number}.json'
            run(['java','-jar',str(out/f'converter-{number}.jar'),'-file',str(ttl),'-output',str(target)],root,out/f'{v["id"]}-{number}-conversion.log')
            data=json.loads(target.read_text());outputs.append({'sha256':sha(target.read_bytes()),'canonical_json_sha256':sha(json.dumps(data,sort_keys=True,separators=(',',':')).encode()),'classes':len(data.get('class',[])),'properties':len(data.get('property',[]))})
        projection[v['id']]=outputs
    expected=json.loads((root/'docs/documentation/webvowl-adapter.json').read_text())['owl2vowl']['expected_shaded_jar_content_sha256']
    result={'schema_version':1,'diagnostic_only':True,'publication_authorized':False,'expected_pin_unchanged':expected,'source_commit':'2833ead00122ca252a0fd0e18c5e5b696d711d2c','content_digests':[r['content_digests'] for r in reports],'changed_entries':changed,'changed_classes':[n for n in changed if n.endswith('.class')],'changed_text':{str(i+1):{n:t for n,t in r['generated_text'].items() if n in changed} for i,r in enumerate(reports)},'projections':projection,'maven_files':len(dependencies),'overlay':overlay,'restored_pin_twice':all(r['content_digests']['legacy_literal']==expected for r in reports[2:]),'pinned_build_entries_identical':reports[2]['entries']==reports[3]['entries'],'default_to_pinned_changed_entries':[n for n in sorted(set(reports[0]['entries'])|set(reports[2]['entries'])) if reports[0]['entries'].get(n)!=reports[2]['entries'].get(n)]}
    write(out/'summary.json',result);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
