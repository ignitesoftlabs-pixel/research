"""Synthetic single-operation CAA gate. No clinical validation or production auth."""
from dataclasses import dataclass,asdict
from hashlib import sha256
import json,threading
@dataclass(frozen=True)
class Contract:
 patient:str='SYNTHETIC-P001'
 encounter:str='SYNTHETIC-E001'
 operation:str='create_followup_task'
 arguments:tuple=('review observation',)
 resource_version:int=3
 evidence_version:int=3
 evidence_time:int=95
 valid_from:int=90
 expires:int=110
 policy_version:int=1
 key:str='SYNTHETIC-TASK-001'
 def digest(self):return sha256(json.dumps(asdict(self),sort_keys=True,separators=(',',':')).encode()).hexdigest()
@dataclass(frozen=True)
class Approval:
 digest:str
 reviewer:str='SYNTHETIC-REVIEWER'
 expires:int=110
@dataclass(frozen=True)
class Context:
 patient:str='SYNTHETIC-P001'
 encounter:str='SYNTHETIC-E001'
 scopes:tuple=('create_followup_task',)
 reviewer:str='SYNTHETIC-REVIEWER'
 policy_version:int=1
 max_evidence_age:int=10
class Denied(Exception):pass
class Escalation(Exception):pass
class Adapter:
 def __init__(self):
  self.patient='SYNTHETIC-P001';self.encounter='SYNTHETIC-E001';self.resource_version=3;self.evidence_version=3;self.registry={};self.effects=[];self.lock=threading.Lock();self.corrupt_receipt=False
 def execute(self,c,a,ctx,now=100):
  with self.lock:
   checks={'subject':c.patient==ctx.patient==self.patient,'encounter':c.encounter==ctx.encounter==self.encounter,'scope':c.operation in ctx.scopes and c.operation=='create_followup_task','policy':c.policy_version==ctx.policy_version,'time':c.valid_from<=now<=c.expires,'evidence_fresh':0<=now-c.evidence_time<=ctx.max_evidence_age,'approval':a is not None and a.digest==c.digest() and a.reviewer==ctx.reviewer and now<=a.expires,'arguments':len(c.arguments)==1 and bool(c.arguments[0])}
   if not all(checks.values()):raise Denied(','.join(k for k,v in checks.items() if not v))
   if c.key in self.registry:
    digest,receipt=self.registry[c.key]
    if digest!=c.digest():raise Denied('idempotency key reused with different payload')
   else:
    if c.resource_version!=self.resource_version or c.evidence_version!=self.evidence_version:raise Denied('stale version')
    receipt={'patient':c.patient,'encounter':c.encounter,'operation':c.operation,'key':c.key,'effect_id':f'SYNTHETIC-EFFECT-{len(self.effects)+1}','arguments':c.arguments};self.effects.append(dict(receipt));self.resource_version+=1;self.registry[c.key]=(c.digest(),receipt)
   observed=dict(receipt)
   if self.corrupt_receipt:observed['patient']='SYNTHETIC-WRONG'
   if any(observed[k]!=v for k,v in {'patient':c.patient,'encounter':c.encounter,'operation':c.operation,'key':c.key,'arguments':c.arguments}.items()):raise Escalation('committed effect receipt mismatch: reconcile; do not assume rollback')
   return observed
