"""Fail-closed metric gates for a local evaluation report."""
import argparse
import json
from pathlib import Path
import math
import sys


def number(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("thresholds and metric values must be finite numbers")
    return value


def evaluate(metrics, samples, minimum_samples, rules):
    if not isinstance(metrics, dict) or any(not isinstance(key, str) for key in metrics):
        raise ValueError("metrics must be a name-to-number mapping")
    for value in metrics.values():
        number(value)
    if type(samples) is not int or samples < 0 or type(minimum_samples) is not int or minimum_samples < 1:
        raise ValueError("sample counts must be integers; minimum_samples must be positive")
    if not isinstance(rules, list) or not rules:
        raise ValueError("at least one rule is required")
    results = [{"rule": "minimum_samples", "passed": samples >= minimum_samples,
                "observed": samples, "required": minimum_samples}]
    names = {"minimum_samples"}
    for rule in rules:
        name, metric, operator = rule["name"], rule["metric"], rule["op"]
        if not isinstance(name, str) or not name or name in names:
            raise ValueError("rule names must be unique nonempty strings")
        names.add(name)
        if not isinstance(metric, str) or not metric:
            raise ValueError("metric names must be nonempty strings")
        threshold = rule["value"]
        if operator == "between":
            if not isinstance(threshold, list) or len(threshold) != 2:
                raise ValueError("between requires two bounds")
            lower, upper = map(number, threshold)
            if lower > upper:
                raise ValueError("between bounds are reversed")
        elif operator in ("gte", "lte"):
            number(threshold)
        else:
            raise ValueError("supported operations: gte, lte, between")
        observed = metrics.get(metric)
        if observed is None:
            passed, reason = False, "missing_metric"
        else:
            passed = (observed >= threshold if operator == "gte" else
                      observed <= threshold if operator == "lte" else lower <= observed <= upper)
            reason = "within_policy" if passed else "threshold_failed"
        results.append({"rule": name, "metric": metric, "passed": passed, "reason": reason,
                        "observed": observed, "op": operator, "required": threshold})
    return {"decision": "pass" if all(row["passed"] for row in results) else "block", "checks": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        input_path = Path(args.input)
        if not input_path.is_absolute():
            input_path = Path(__file__).resolve().parent / input_path
        with input_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        result = evaluate(data["metrics"], data["samples"], data["minimum_samples"], data["rules"])
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result["decision"] == "pass" else 1
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"Invalid gate policy or metrics: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
