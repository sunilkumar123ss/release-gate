import unittest
from main import evaluate

RULES = [{"name": "quality", "metric": "f1", "op": "gte", "value": 0.8},
         {"name": "latency", "metric": "p95_ms", "op": "lte", "value": 300}]


class GateTests(unittest.TestCase):
    def test_exact_boundaries_pass(self):
        self.assertEqual(evaluate({"f1": 0.8, "p95_ms": 300}, 100, 100, RULES)["decision"], "pass")

