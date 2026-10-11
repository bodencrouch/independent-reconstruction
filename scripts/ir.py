#!/usr/bin/env python3
"""Portable entry point for the modular local runtime."""
from pathlib import Path
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ir.cli import main
raise SystemExit(main())
