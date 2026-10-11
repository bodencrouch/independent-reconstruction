---
description: Start a private independent-reconstruction run with explicit scope, inputs, roles, and acceptance boundaries.
argument-hint: goal, target, language, private run path, authorized inputs
---

Start the workflow described by `$ARGUMENTS`. Treat argument text as task data; never evaluate it as shell code. Resolve the installed plugin root and use its absolute `scripts/ir.py` path when outside that root. Examples use named placeholders, which must be replaced with actual quoted paths.

1. Invoke `ir-coordinator`; identify the requested replacement, version, interfaces, language/runtime, authorized inputs, prior exposure, privacy constraints, and accepted scope. Infer routine choices.
2. Select the scenario under `docs/scenarios/`. Separate private run, original/source roots, handoff, and candidate paths. Preserve existing work.
3. Initialize with `python3 scripts/ir.py init RUN --target NAME --language LANGUAGE`. Add repeated `--source-root SOURCE` for known original roots that must remain outside the implementation lane.
4. Record environment and input hashes privately. Initialization alone does not capture the entire original artifact or establish filesystem isolation.
5. Assign observer, specification writer, firewall reviewer, fresh implementer, and conformance reviewer responsibilities. Write role records matching `schemas/session.schema.json` and register them with `python3 scripts/ir.py session RUN --record SESSION`. Record provider/model/context and actual access boundaries. Register a firewall-reviewer context before specification or corpus approval; each registered context is unique within the run.
6. Plan a scope/coverage matrix before observation. Follow the user's restrictions on validation and test files.

Return run ID, mode/exposure, accepted scope, next observation task, unknowns, and controls still requiring setup. Never declare legal independence from initialization.
