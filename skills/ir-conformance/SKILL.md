---
name: ir-conformance
description: Compares candidate and pinned oracle behavior using approved cases, explicit normalization, and reproducible environments. Use explicitly for differential conformance validation or a compatibility audit.
disable-model-invocation: true
---
# Measure behavioral compatibility

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Confirm that the application implementation is complete enough for the requested validation phase and that the session permits executing checks. Pin oracle and candidate artifacts, commands, runtime, seed, and environment.
2. Build cases from the approved requirements and observation contract. Record provenance for inputs; keep original test implementation outside the handoff unless its use is explicitly justified and reviewed. Obtain a substantive corpus review from a registered `firewall-reviewer`, then `approve-cases` for the exact case digest. Acceptance IDs alone do not approve inputs.
3. Define comparisons before execution: stdout, stderr, exit status, structured output, side effects, state transitions, and documented numeric tolerances. Record any exclusions.
4. Confirm the controller has registered the actual fresh implementer context with `sealed-spec-only` exposure. Encode commands as JSON argument arrays; avoid shell strings and implicit interpolation. Execute potentially hostile artifacts only through a suitable isolated validator environment.
5. Run `validate` against the exact approved corpus and registered implementer. Any case edit needs another corpus review before execution. Inspect failed, errored, skipped, and timed-out cases separately. A failed oracle run is not candidate compatibility evidence.
6. Produce a minimal synthetic counterexample for each difference. Review feedback through the firewall before sending it to the implementer.
7. Map results to requirement coverage. Report corpus-limited compatibility and gaps; retain the original receipts and rerun only affected or justified cases after changes.

## Execute

Register a session only for an actual new context. If the required reviewer or implementer record already exists, use its exact registered context and do not invent another ID or register a duplicate.

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" session "$RUN" --record "$REVIEWER_SESSION_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" session "$RUN" --record "$IMPLEMENTER_SESSION_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" approve-cases "$RUN" --cases "$CASES_JSON" --review "$CORPUS_REVIEW_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" validate "$RUN" --cases "$CASES_JSON" --oracle "$ORACLE_COMMAND_JSON" --candidate "$CANDIDATE_COMMAND_JSON"
```

## Return

Return command/environment digests, approved corpus digest, reviewer and implementer context records, case totals by status, requirement coverage, reproducible counterexamples, excluded comparisons, unsupported behavior, and the validation receipt.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
