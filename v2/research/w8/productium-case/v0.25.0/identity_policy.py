"""Exact v0.22 decision policy; unchanged function source. Not independent semantic acceptance."""
import re
IRI=re.compile(r'^(?:urn:[^\s]+|https?://[^\s]+)$')
OPS={'restart','migrate','upgrade','rollback','clone','recreate'}
STATES={'PRESERVED','BROKEN','UNKNOWN'}
FIELDS=['before_r','after_r','before_v','after_v','before_c','after_c','evidence']
def assess(t):
 errors=[]
 for k in FIELDS:
  if not isinstance(t.get(k),str) or not IRI.fullmatch(t[k]):errors.append('INVALID_'+k.upper())
 if t.get('operation') not in OPS:errors.append('UNKNOWN_OPERATION')
 for k in ['system_continuity','disposition_continuity']:
  if t.get(k) not in STATES:errors.append('INVALID_'+k.upper())
 if type(t.get('branching')) is not bool:errors.append('INVALID_BRANCHING')
 if errors:return dict(status='REJECTED',errors=errors)
 changed=t['before_v']!=t['after_v'];op=t['operation']
 if op in {'upgrade','rollback'} and not changed:return dict(status='REJECTED',errors=['VERSION_CHANGE_REQUIRED'])
 if op in {'restart','migrate'} and changed:return dict(status='REJECTED',errors=['VERSION_CHANGE_REQUIRES_SUCCESSOR_OPERATION'])
 if changed or op in {'clone','recreate'} or t['branching'] or t['system_continuity']=='BROKEN':r='DISTINCT'
 elif t['system_continuity']=='UNKNOWN':return dict(status='REVIEW_REQUIRED',errors=['SYSTEM_CONTINUITY_UNDETERMINED'])
 else:r='SAME'
 if (t['before_r']==t['after_r'])!=(r=='SAME'):errors.append('REALIZATION_IDENTITY_CONTRADICTION')
 if errors:return dict(status='REJECTED',realization_identity=r,errors=errors)
 if r=='DISTINCT':c='DISTINCT'
 elif t['disposition_continuity']=='UNKNOWN':return dict(status='REVIEW_REQUIRED',errors=['DISPOSITION_CONTINUITY_UNDETERMINED'])
 else:c='SAME' if t['disposition_continuity']=='PRESERVED' else 'DISTINCT'
 if (t['before_c']==t['after_c'])!=(c=='SAME'):errors.append('CAPABILITY_IDENTITY_CONTRADICTION')
 return dict(status='REJECTED' if errors else 'ACCEPTED',realization_identity=r,capability_identity=c,errors=errors)
