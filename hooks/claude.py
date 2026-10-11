#!/usr/bin/env python3
"""Claude Code-only hook entry point; uses Claude's JSON output schema."""
from ir_hooks.dispatch import main

if __name__ == "__main__":
    raise SystemExit(main("claude"))
