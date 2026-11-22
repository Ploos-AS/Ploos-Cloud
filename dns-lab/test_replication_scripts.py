import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).parent / "scripts"
spec = importlib.util.spec_from_file_location("bootstrap", ROOT / "bootstrap-secondaries.py")
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)

class BootstrapTests(unittest.TestCase):
    def test_private_ip(self):
        self.assertEqual(bootstrap.validate_primary_ip("172.20.0.5"), "172.20.0.5")
    def test_reject_public_ip(self):
        with self.assertRaises(ValueError):
            bootstrap.validate_primary_ip("8.8.8.8")
    def test_reject_hostname(self):
        with self.assertRaises(ValueError):
            bootstrap.validate_primary_ip("primary")
    def test_reject_loopback(self):
        with self.assertRaises(ValueError):
            bootstrap.validate_primary_ip("127.0.0.1")
    def test_idempotent_existing_zone(self):
        with patch.object(bootstrap, "KEY", "testing-key"), patch.object(bootstrap, "PRIMARY_IP", "172.20.0.5"), patch.object(bootstrap, "api") as api:
            api.side_effect = [[{"name": "lab.invalid."}], {"kind": "Secondary", "masters": ["172.20.0.5"]}] * 2
            bootstrap.bootstrap()
            self.assertEqual(api.call_count, 4)

if __name__ == "__main__":
    unittest.main()
