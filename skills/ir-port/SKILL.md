---
name: ir-port
description: Plans independent implementations across programming languages while preserving defined runtime semantics and public interfaces. Use explicitly for behavior-based ports or language migration reconstruction.
disable-model-invocation: true
---
# Port the behavioral contract

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Pin source-facing behavior and target language/runtime. Distinguish an independently implemented compatibility port from a source translation permitted under an existing license.
2. Identify semantic boundaries: numeric precision, overflow, coercion, truthiness, exceptions, Unicode, iteration order, cancellation, time, and concurrency.
3. Observe boundary cases in the pinned oracle. Make required semantics explicit rather than relying on the target language's defaults.
4. Write behavior-only requirements and adapter contracts. Leave target idioms, algorithms, names, and module structure to the implementer.
5. Review exact public identifiers and constants needed for compatibility. Changing language or names is not evidence of independence.
6. Export the approved pack to a fresh target-language implementation lane. Track new dependency licenses and target runtime constraints.
7. Compare results through explicit adapters and reviewed normalization. Report semantic and platform gaps separately.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" check "$RUN" --spec "$SPEC_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" handoff "$RUN" --dest "$HANDOFF_DEST"
```

## Return

Return the language/runtime matrix, semantic compatibility decisions, adapter policy, approved digest, candidate status, dependency changes, and remaining mismatches.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
