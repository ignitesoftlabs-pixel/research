import unittest,json
from pathlib import Path
from dataclasses import replace
from caa_reference import Contract,Approval,Context,Adapter,Denied,Escalation
R=Path(__file__).resolve().parents[1]
class Invariants(unittest.TestCase):
 def setUp(self):self.c=Contract();self.a=Approval(self.c.digest());self.ctx=Context();self.ad=Adapter()
 def deny(self,c=None,a=None,ctx=None):
  with self.assertRaises(Denied):self.ad.execute(c or self.c,a or self.a,ctx or self.ctx)
  self.assertEqual(len(self.ad.effects),0)
 def test_valid_receipt(self):
  r=self.ad.execute(self.c,self.a,self.ctx);self.assertEqual(r['patient'],self.c.patient);self.assertEqual(self.ad.effects[0],r)
 def test_wrong_patient(self):self.deny(ctx=replace(self.ctx,patient='SYNTHETIC-OTHER'))
 def test_wrong_encounter(self):self.deny(ctx=replace(self.ctx,encounter='SYNTHETIC-OTHER'))
 def test_adapter_binding(self):self.ad.patient='SYNTHETIC-OTHER';self.deny()
 def test_prohibited_operation(self):
  c=replace(self.c,operation='prescribe_drug');self.deny(c,Approval(c.digest()))
 def test_changed_resource(self):self.ad.resource_version=4;self.deny()
 def test_changed_evidence(self):self.ad.evidence_version=4;self.deny()
 def test_missing_approval(self):
  with self.assertRaises(Denied):self.ad.execute(self.c,None,self.ctx)
  self.assertEqual(self.ad.effects,[])
 def test_mutated_approved_arguments(self):self.deny(c=replace(self.c,arguments=('different task',)))
 def test_wrong_reviewer(self):self.deny(a=replace(self.a,reviewer='SYNTHETIC-OTHER'))
 def test_expired_contract(self):
  c=replace(self.c,expires=99);self.deny(c,Approval(c.digest()))
 def test_future_evidence(self):
  c=replace(self.c,evidence_time=101);self.deny(c,Approval(c.digest()))
 def test_stale_evidence(self):
  c=replace(self.c,evidence_time=89);self.deny(c,Approval(c.digest()))
 def test_idempotent_retry(self):
  r=self.ad.execute(self.c,self.a,self.ctx);self.assertEqual(self.ad.execute(self.c,self.a,self.ctx),r);self.assertEqual(len(self.ad.effects),1)
 def test_key_conflict(self):
  self.ad.execute(self.c,self.a,self.ctx);c=replace(self.c,arguments=('changed',))
  with self.assertRaises(Denied):self.ad.execute(c,Approval(c.digest()),self.ctx)
  self.assertEqual(len(self.ad.effects),1)
 def test_receipt_mismatch_escalates(self):
  self.ad.corrupt_receipt=True
  with self.assertRaises(Escalation):self.ad.execute(self.c,self.a,self.ctx)
  self.assertEqual(len(self.ad.effects),1)
 def test_revoked_scope_on_replay(self):
  self.ad.execute(self.c,self.a,self.ctx)
  with self.assertRaises(Denied):self.ad.execute(self.c,self.a,replace(self.ctx,scopes=()))
  self.assertEqual(len(self.ad.effects),1)
 def test_changed_policy(self):self.deny(ctx=replace(self.ctx,policy_version=2))
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Invariants)
 with (R/'research/audit/software_tests.txt').open('w') as f:result=unittest.TextTestRunner(stream=f,verbosity=2).run(suite)
 report={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'success':result.wasSuccessful(),'scope':'synthetic software invariants; no clinical validation'};(R/'research/audit/software_test_report.json').write_text(json.dumps(report,indent=2));print(report)
 if not result.wasSuccessful():raise SystemExit(1)
