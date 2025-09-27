import unittest
from main import evaluate

RULES = [{"name": "quality", "metric": "f1", "op": "gte", "value": 0.8},
         {"name": "latency", "metric": "p95_ms", "op": "lte", "value": 300}]


class GateTests(unittest.TestCase):
    def test_exact_boundaries_pass(self):
        self.assertEqual(evaluate({"f1": 0.8, "p95_ms": 300}, 100, 100, RULES)["decision"], "pass")

    def test_missing_metric_and_insufficient_samples_block(self):
        result = evaluate({"f1": 0.9}, 99, 100, RULES)
        self.assertEqual(result["decision"], "block")
        self.assertEqual(result["checks"][-1]["reason"], "missing_metric")
        self.assertFalse(result["checks"][0]["passed"])

    def test_between_and_threshold_failure(self):
        rule = [{"name": "coverage", "metric": "rate", "op": "between", "value": [0.1, 0.9]}]
        self.assertEqual(evaluate({"rate": 1}, 10, 1, rule)["decision"], "block")

