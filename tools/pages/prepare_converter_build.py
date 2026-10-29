#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Pin default Maven plugins to the successful 2026-09-30 converter receipt."""
import argparse,hashlib,json,subprocess
from pathlib import Path

def prepare(source):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()=='2833ead00122ca252a0fd0e18c5e5b696d711d2c'
    original=source/'pom.xml';data=original.read_bytes();text=data.decode()
    plugins='''<plugins>
            <!-- CM-PharmE: reproduce successful hosted converter run 36679317918. -->
            <plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-resources-plugin</artifactId><version>3.4.0</version></plugin>
            <plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-jar-plugin</artifactId><version>3.5.0</version></plugin>'''
    assert '<plugins>' in text
    target=source/'pom.cmpe.xml';target.write_text(text.replace('<plugins>',plugins,1))
    return {'original_pom_sha256':hashlib.sha256(data).hexdigest(),'derived_pom_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'resources_plugin':'3.4.0','jar_plugin':'3.5.0','basis_run':36679317918}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);a=ap.parse_args();print(json.dumps(prepare(a.source)))
