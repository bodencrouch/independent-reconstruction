#!/usr/bin/env python3
"""Cursor-only hook entry point; uses Cursor's JSON output schema."""
from ir_hooks.dispatch import main

if __name__ == "__main__":
    raise SystemExit(main("cursor"))
