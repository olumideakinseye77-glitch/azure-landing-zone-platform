import json
import unittest
from pathlib import Path

from scripts.validate_request import validate

ROOT = Path(__file__).resolve().parents[1]


class RequestValidationTests(unittest.TestCase):
    def setUp(self):
        self.request = json.loads(
            (ROOT / "requests/dev.json").read_text()
        )

    def test_valid_request(self):
        self.assertEqual(validate(self.request), [])

    def test_missing_owner(self):
        del self.request["owner"]
        self.assertTrue(any("owner" in e for e in validate(self.request)))

    def test_unapproved_region(self):
        self.request["location"] = "eastus"
        self.assertTrue(any("location" in e for e in validate(self.request)))

    def test_subnet_outside_network(self):
        self.request["subnet_cidr"] = "10.61.1.0/24"
        self.assertTrue(any("inside" in e for e in validate(self.request)))

    def test_public_network(self):
        self.request["network_cidr"] = "8.8.0.0/16"
        self.request["subnet_cidr"] = "8.8.1.0/24"
        self.assertTrue(any("private" in e for e in validate(self.request)))

    def test_malformed_network(self):
        self.request["network_cidr"] = "not-a-network"
        self.assertTrue(any("Invalid IPv4" in e for e in validate(self.request)))

    def test_unknown_field(self):
        self.request["unexpected"] = "value"
        self.assertTrue(any("unknown" in e for e in validate(self.request)))

    def test_non_object(self):
        self.assertTrue(validate(["not", "an", "object"]))


if __name__ == "__main__":
    unittest.main()
