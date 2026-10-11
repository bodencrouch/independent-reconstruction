"""Bounded JSON entry point with active-run failure containment."""
import argparse
import json
import os
from pathlib import Path
import sys
from .adapters import CLAUDE_EVENTS, CLAUDE_GATES, CODEX_EVENTS, CODEX_GATES, CURSOR_EVENTS, CURSOR_GATES, normalize, output
from .audit import record
from .context import PolicyError, active, load, strict_json
from .policy import Decision, evaluate

MAX_INPUT = 32 * 1024 * 1024


def main(host: str) -> int:
    parser = argparse.ArgumentParser(description="Independent Reconstruction hook adapter")
    events = {"cursor": CURSOR_EVENTS, "claude": CLAUDE_EVENTS, "codex": CODEX_EVENTS}[host]
    parser.add_argument("--event", required=True, choices=sorted(events))
    args = parser.parse_args()
    enabled = active()
    ctx = None
    raw = b""
    decision = Decision(True, "passive")
    try:
        # Passive hooks do not parse or retain event content, load private run
        # files, or produce receipts. They still emit valid host responses.
        if enabled:
            raw = sys.stdin.buffer.read(MAX_INPUT + 1)
            if len(raw) > MAX_INPUT:
                raise PolicyError("Hook input exceeds the bounded payload limit.")
            data = strict_json(raw)
            if not isinstance(data, dict):
                raise PolicyError("Hook input must be a JSON object.")
            if data.get("hook_event_name", args.event) != args.event:
                raise PolicyError("Hook event does not match its configured adapter.")
            ctx = load()
            operation, tool, inputs, cwd = normalize(host, args.event, data)
            decision = evaluate(ctx, operation, tool, inputs, cwd)
            record(ctx.run, ctx.role, host, args.event, raw, "allow" if decision.allow else "deny", decision.code)
    except (PolicyError, ValueError, UnicodeError, OSError, TypeError, KeyError) as exc:
        decision = Decision(False, "invalid_active_context", str(exc) if isinstance(exc, PolicyError) else "Active reconstruction hook failed. Correct the role policy or hook registry from the coordinator session before continuing.")
    except Exception:
        # Never serialize an exception whose repr might contain source paths,
        # command text, secrets, or snippets of the event payload.
        decision = Decision(False, "hook_internal_error", "Active reconstruction hook encountered an internal error. Stop this role session and repair the adapter from the coordinator session.")
    response = output(host, args.event, decision, enabled)
    sys.stdout.write(json.dumps(response, separators=(",", ":")) + "\n")
    gates = {"cursor": CURSOR_GATES, "claude": CLAUDE_GATES, "codex": CODEX_GATES}[host]
    if not decision.allow and args.event in gates:
        # Exit 2 is the second denial signal. An observational event cannot
        # retroactively block a tool and must not claim that it did.
        if host in {"claude", "codex"}:
            sys.stderr.write(decision.message + "\n")
        return 2
    return 0
