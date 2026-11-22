import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

spec = importlib.util.spec_from_file_location("notify_secondaries", Path(__file__).parent / "scripts" / "notify-secondaries.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class NotifyTests(unittest.TestCase):
    def test_fixed_lab_endpoint(self):
        self.assertEqual(mod.ZONE, "lab.invalid.")
        self.assertEqual(mod.API, "http://127.0.0.1:8089/api/v1/servers/localhost")
    def test_requires_confirmation(self):
        with patch.object(mod, "KEY", "test-key"), patch.dict(os.environ, {"CONFIRM_LAB_NOTIFY": ""}):
            with self.assertRaises(ValueError): mod.notify()
    def test_requires_key(self):
        with patch.object(mod, "KEY", ""), patch.dict(os.environ, {"CONFIRM_LAB_NOTIFY": "yes"}):
            with self.assertRaises(ValueError): mod.notify()
    def test_http_request(self):
        response = MagicMock()
        response.status = 204
        response.__enter__.return_value = response
        with patch.object(mod, "KEY", "test-key"), patch.dict(os.environ, {"CONFIRM_LAB_NOTIFY": "yes"}), patch.object(mod.urllib.request, "urlopen", return_value=response) as urlopen:
            mod.notify()
            req = urlopen.call_args.args[0]
            self.assertEqual(req.get_method(), "PUT")
            self.assertEqual(req.full_url, mod.API + "/zones/lab.invalid./notify")

if __name__ == "__main__":
    unittest.main()
