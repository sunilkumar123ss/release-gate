# Evaluation release gate

A fail-closed local policy evaluator for already-computed metrics. The example report and thresholds are synthetic; passing this fixture does not certify a model.

~~~sh
python3 main.py --input example.json
python3 -m unittest -v
~~~

All rules and the minimum sample count must pass. Supported inclusive operations are gte, lte, and between. A missing required metric blocks release. Nonfinite metrics, invalid bounds, duplicate rule names, and empty policies are configuration errors.

Exit code 0 means pass, 1 means policy block, and 2 means invalid input. A CI system can consume those codes. This program does not deploy anything or independently verify measurement provenance, slice coverage, statistical uncertainty, security, or model safety.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
