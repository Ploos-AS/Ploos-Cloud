import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("zone", Path(__file__).parent / "scripts" / "zone.py")
zone = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zone)

class ZoneTests(unittest.TestCase):
    def test_lab_zone_is_fixed(self):
        self.assertEqual(zone.ZONE, "lab.invalid.")
        self.assertEqual(zone.API, "http://127.0.0.1:8089/api/v1/servers/localhost")
    def test_delete_requires_confirmation(self):
        with patch.dict(os.environ, {"CONFIRM_DELETE_LAB_ZONE": ""}):
            with self.assertRaises(RuntimeError):
                zone.delete()
    def test_create_is_idempotent(self):
        with patch.object(zone, "request", return_value=[{"name": "lab.invalid."}]) as mock:
            zone.create()
            mock.assert_called_once_with("GET", "/zones")

if __name__ == "__main__":
    unittest.main()
