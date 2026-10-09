"""A stricter structural-probe entry point. Never a full-fidelity converter.

The previous bridge only emitted readOnly when true, causing legacy defaults
for null. Refuse null now. Nature and annotation/metadata fidelity still require
the native route and explicit loss reports; no official source is modified.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'2.1.0-alpha.1-detector-calibration'))
from adapter_specialization import convert as prior_convert


def convert(model):
    unknown = [e['id'] for e in model['elements'] if e['type']=='Property' and e.get('isReadOnly') is None]
    if unknown:
        raise ValueError('Unknown isReadOnly must not become a legacy false default: '+', '.join(unknown[:8]))
    raw, report = prior_convert(model)
    report['readonly_guard']='All included Property.isReadOnly flags explicitly specified'
    report['full_fidelity']=False
    return raw, report
