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

