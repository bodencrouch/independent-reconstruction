---
name: ir-replace-dependency
description: Integrates an independently implemented dependency replacement through consumer checks, rollback, and bounded compatibility claims. Use explicitly after a reconstruction candidate and approved contract are available.
disable-model-invocation: true
---
# Integrate a replacement

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Confirm the candidate's approved contract digest, exposure record, dependency inventory, supported surface, and validation evidence. Identify the consumer's actual required operations.
2. Preserve dirty changes, current dependency resolution, notices, and a rollback path. Use an isolated checkout when integration could interfere with existing work.
3. Define package identity, import/API compatibility, supported versions, platform requirements, configuration, and migration steps. Avoid implying the candidate is the original project.
4. Update the consumer adapter or dependency declaration minimally. Do not change original source or notices merely to make the candidate look independent.
5. In the authorized validation phase, exercise affected consumer workflows and compare observable behavior. Keep unit corpus, integration, installed/runtime, and platform evidence distinct.
6. Route newly discovered behavior through observation, specification review, and fresh implementation feedback. Invalidate stale approvals or results when artifacts change.
7. Record the replacement, retained gaps, rollout/rollback steps, and distribution questions. Prepare a local release artifact; honor the user's explicit public pull-request gate.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" audit "$RUN"
python3 "$PLUGIN_ROOT/scripts/ir.py" report "$RUN"
```

## Return

Return changed integration files, replacement identity, supported consumer workflows, exact tested versions/platforms, rollback procedure, unresolved behavior, and publication status.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
