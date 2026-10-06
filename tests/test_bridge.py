import json, unittest
from tools.mobile_bridge import Bridge
class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.sent=[];self.now=0;self.b=Bridge('https://notify.example.test','lab',sender=self.sent.append,clock=lambda:self.now)
        self.record=dict(project_id=2,valid=True,temperature_c=31,humidity_pct=50,pressure_hpa=1013,alert=True)
    def emit(self):return self.b.process(json.dumps(self.record))
    def test_cooldown_and_recovery(self):
        self.assertTrue(self.emit());self.assertFalse(self.emit());self.now=300;self.assertTrue(self.emit())
        self.record['alert']=False;self.assertFalse(self.emit());self.record['alert']=True;self.assertTrue(self.emit())
    def test_invalid_does_not_notify(self):
        for key,value in [('valid',False),('project_id',3),('humidity_pct',101),('temperature_c',True),('pressure_hpa',float('nan'))]:
            r=self.record.copy();r[key]=value;self.assertFalse(self.b.process(json.dumps(r)))
        self.assertEqual(self.sent,[])
    def test_failed_send_can_retry(self):
        self.b.sender=lambda _: (_ for _ in ()).throw(RuntimeError('offline'))
        with self.assertRaises(RuntimeError):self.emit()
        self.b.sender=self.sent.append;self.assertTrue(self.emit())
    def test_bad_destination(self):
        for base,topic in [('file:///tmp','a'),('https://x','../a'),('https://u:p@x','a')]:
            with self.assertRaises(ValueError):Bridge(base,topic)
if __name__=='__main__':unittest.main()
