"""Source-qualified label scope, not a chemical membership or clinical inference engine."""
from pathlib import Path
import json,re
from decimal import Decimal,InvalidOperation
H=Path(__file__).resolve().parent
def normalized(label):return re.sub(r'\s+',' ',str(label).strip().lower())
def lookup(data,label,version,amount=None,unit=None,route=None,basis=None):
 if version!=data['scope_version']:return 'UNKNOWN_SOURCE_VERSION'
 term=normalized(label)
 if not term:return 'INVALID_INPUT'
 for entry in data['entries']:
  if normalized(entry['source_label'])==term:return 'SOURCE_LABEL_LISTED'
 # This is an explicitly proposed parsing of the source qualifier, not a
 # claim that an actual marketed product or dose is covered by a legal rule.
 if term=='medroxyprogesterone':
  if amount is None or unit is None or route is None or basis is None:return 'UNKNOWN_QUALIFIERS'
  if basis!='source-formulation-amount':return 'UNKNOWN_AMOUNT_BASIS'
  if unit!='mg':return 'UNKNOWN_UNSUPPORTED_UNIT'
  try:n=Decimal(str(amount))
  except InvalidOperation:return 'INVALID_INPUT'
  if not n.is_finite() or n<=0:return 'INVALID_INPUT'
  if normalized(route)!='oral' or n>=100:return 'OUTSIDE_THIS_ENTRY_UNDER_PROPOSED_MAPPING'
  return 'QUALIFIER_MATCH_UNDER_PROPOSED_MAPPING'
 return 'NOT_LISTED_IN_EXTRACTED_SCOPE_UNKNOWN_CHEMICAL_MEMBERSHIP'
if __name__=='__main__':
 data=json.loads((H/'pv-group-source.json').read_text())
 print(json.dumps({'version':data['scope_version'],'entry_count':len(data['entries']),'example':lookup(data,'dienogest',data['scope_version'])}))
