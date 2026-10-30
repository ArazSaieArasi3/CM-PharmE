"""Narrow exact-Boolean admission wrapper; historical structural adapter unchanged."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'2.1.0-alpha.1-native-fidelity-audit'))
from adapter_readonly_guard import convert as historical_guarded_convert


def convert(model):
    unknown=[];invalid=[]
    for e in model['elements']:
        if e['type']!='Property':continue
        value=e.get('isReadOnly')
        if value is None:unknown.append(e['id'])
        elif type(value) is not bool:invalid.append(e['id'])
    if unknown:raise ValueError('unknown_native_readonly: '+', '.join(unknown[:8]))
    if invalid:raise ValueError('invalid_native_readonly: '+', '.join(invalid[:8]))
    raw,report=historical_guarded_convert(model)
    report['explicit_boolean_admission']='Exact native bool values only; no missing/null coercion'
    report['full_fidelity']=False
    return raw,report
