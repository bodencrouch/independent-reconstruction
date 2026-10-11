---
name: ir-implement
description: Implements a candidate from an approved behavioral pack in a fresh context and separate workspace. Use explicitly for the implementation lane of an independent reconstruction.
disable-model-invocation: true
---
# Implement from the approved pack

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Receive only the approved handoff. Do not inherit the collector's conversation, raw evidence, source repository, browsing results, private notes, or unrestricted retrieval tools.
2. Verify the handoff manifest and approved digest before implementation. Record participant identity, model/provider/version when known, prior exposure, tools, workspace, and isolation mechanism. The controller registers this actual fresh context as `implementer` with `sealed-spec-only` exposure before validation.
3. Use a fresh conversation with history disabled. Restrict file access to the pack, candidate workspace, and explicitly approved toolchain. Use the package sandbox command where supported; report a missing operating-system boundary honestly.
4. Choose algorithms, data structures, module layout, names, and comments independently within the behavioral contract. Honor license obligations for any new dependencies.
5. When requirements are ambiguous, ask behavioral questions using requirement IDs. Send the question to the specification lane; receive only reviewed answers tied to a new approved digest.
6. Preserve authored work and disclose accidental exposure immediately. Stop the affected lane and use `ir-recover`; do not pretend that deleting a file erases knowledge.
7. Deliver the candidate plus implementation environment, dependency inventory, supported requirements, gaps, and changes. The controller admits only a digest-approved case corpus and the registered fresh implementation context to validation. Run scoped conformance only when the current task requests validation or permits its phase.

## Execute

Register a session only for an actual new context. If the required reviewer or implementer record already exists, use its exact registered context and do not invent another ID or register a duplicate.

The controller exports and launches these commands. The implementer receives only the sealed pack and candidate workspace; it must not inspect the private `RUN` directory.

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" handoff "$RUN" --dest "$HANDOFF_DEST"
python3 "$PLUGIN_ROOT/scripts/ir.py" session "$RUN" --record "$IMPLEMENTER_SESSION_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" sandbox "$RUN" -- python3 /handoff/candidate/main.py
```

## Return

Return candidate location, received pack digest, exposure record, actual isolation level, dependencies, implemented requirement IDs, known gaps, and validation status.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
