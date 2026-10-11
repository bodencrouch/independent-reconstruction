#!/usr/bin/env python3
"""Create a local package archive from the public file allowlist."""
from pathlib import Path
import argparse
import json
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ir.packaging import bundle
from ir.storage import Invalid

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", required=True)
args = parser.parse_args()
try:
    print(json.dumps(bundle(Path(__file__).resolve().parents[1], args.output), sort_keys=True))
except (Invalid, OSError):
    print(json.dumps({"status": "rejected", "error": "Bundle operation failed; inspect destination and package integrity"}), file=sys.stderr)
    raise SystemExit(2)
