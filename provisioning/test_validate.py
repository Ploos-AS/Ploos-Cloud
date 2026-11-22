import unittest
from validate import validate

GOOD = {"request_id":"pilot-001","organization_id":"demo-association","service":"drive","region":"EU","hostname":"pilot.example.org","quota_gb_total":50,"modules":["files"],"tenancy":"dedicated"}

class RequestTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate(dict(GOOD)))
    def test_bad_region(self):
        data = dict(GOOD, region="US")
        with self.assertRaises(ValueError): validate(data)
    def test_bad_quota(self):
        data = dict(GOOD, quota_gb_total=True)
        with self.assertRaises(ValueError): validate(data)
    def test_missing_files(self):
        data = dict(GOOD, modules=["calendar"])
        with self.assertRaises(ValueError): validate(data)
    def test_unexpected_secret(self):
        data = dict(GOOD, admin_password="do-not-store")
        with self.assertRaises(ValueError): validate(data)

if __name__ == "__main__":
    unittest.main()
