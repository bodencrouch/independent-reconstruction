---
name: ir-intake
description: Defines the scope, evidence access, versions, roles, and acceptance criteria for independent reconstruction. Use explicitly before collecting evidence or when a reconstruction brief is incomplete.
disable-model-invocation: true
---
# Define the run boundary

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Recover the user's requested outcome from the active conversation. Infer reversible choices; ask only for missing information that changes authorization, access, or acceptance.
2. Pin the original artifact or oracle version and its digest. State whether the goal is API compatibility, binary interoperability, file compatibility, dependency replacement, or a new interface with related behavior.
3. Identify allowed evidence channels and which roles may access each. Record prior source exposure and any conceptual briefs already seen by the implementer or coordinator.
4. Define public interface names, language/runtime, supported platforms, determinism assumptions, and out-of-scope behavior. List license or notice records separately from technical acceptance.
5. Identify privacy and execution constraints: credentials, personal data, remote model uploads, oracle side effects, and system isolation availability. Preserve current-session authorization.
6. Start the run. Draft a case matrix and completion criteria without creating or running test suites during implementation-only work.
7. Label unknowns. Proceed with authorized independent work; do not invent permission to inspect a protected repository or publish a replacement.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" init "$RUN" --target "$TARGET" --language "$LANGUAGE"
```

## Return

Return a compact run brief with target/version, outcome, evidence channels, exposure ledger, role boundaries, acceptance criteria, exclusions, and material unknowns.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
