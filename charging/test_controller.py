import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import unittest

loader = importlib.machinery.SourceFileLoader('controller', str(Path(__file__).with_name('omarchy-charge')))
spec = importlib.util.spec_from_loader(loader.name, loader)
c = importlib.util.module_from_spec(spec)
loader.exec_module(c)

class FakeBackend:
    model = 'MacBookPro8,2'
    current = 80
    plugged = True
    fail = False
    def online(self): return self.plugged
    def read(self): return self.current
    def write(self, value):
        if self.fail: raise RuntimeError('Firmware rejected write')
        self.current = value

class ChargingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        c.STATE = Path(self.temp.name) / 'state.json'
        self.backend = FakeBackend()
        self.state = {'limit': 80, 'topup': False}
    def test_topup_then_unplug_restores_saved_limit(self):
        state = c.reconcile(self.backend, self.state, 'topup')
        self.assertEqual(self.backend.current, 100)
        self.assertEqual(state['limit'], 80)
        self.backend.plugged = False
        state = c.reconcile(self.backend, state)
        self.assertEqual(self.backend.current, 80)
        self.assertFalse(state['topup'])
    def test_reboot_preserves_topup_on_ac(self):
        state = c.reconcile(self.backend, self.state, 'topup')
        self.backend.current = 80
        state = c.reconcile(self.backend, state)
        self.assertEqual(self.backend.current, 100)
        self.assertTrue(state['topup'])
    def test_cancel_restores_limit(self):
        state = c.reconcile(self.backend, self.state, 'topup')
        state = c.reconcile(self.backend, state, 'cancel')
        self.assertEqual(self.backend.current, 80)
        self.assertFalse(state['topup'])
    def test_apply_cancels_topup(self):
        state = c.reconcile(self.backend, self.state, 'topup')
        state = c.reconcile(self.backend, state, 'set', 75)
        self.assertEqual(self.backend.current, 75)
        self.assertEqual(state['limit'], 75)
        self.assertFalse(state['topup'])
    def test_unplugged_topup_rejected(self):
        self.backend.plugged = False
        with self.assertRaisesRegex(RuntimeError, 'Connect'):
            c.reconcile(self.backend, self.state, 'topup')
        self.assertEqual(self.backend.current, 80)
    def test_failed_restore_retains_intent_for_retry(self):
        state = c.reconcile(self.backend, self.state, 'topup')
        self.backend.plugged = False
        self.backend.fail = True
        with self.assertRaises(RuntimeError): c.reconcile(self.backend, state)
        state = c.json.loads(c.STATE.read_text())
        self.assertFalse(state['topup'])
        self.assertTrue(state['error'])
        self.backend.fail = False
        state = c.reconcile(self.backend, state)
        self.assertEqual(self.backend.current, 80)
        self.assertEqual(state['error'], '')

if __name__ == '__main__': unittest.main()
