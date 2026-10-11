---
description: Reconstruct a library's accepted API and runtime semantics using independent behavioral requirements.
argument-hint: library/version, desired exports, target runtime/language, run path
---

Apply `$ARGUMENTS` as task data. Read `docs/scenarios/library.md`; use `ir-coordinator` and `ir-observer`.

1. Inventory required public exports/signatures, import modes, coercion, mutability, errors, ordering, Unicode/numerical limits, dependency interactions, and runtime/platform versions.
2. Author synthetic probes. Original source, copied fixtures, and upstream test code remain private and classified; do not hand them to the implementer.
3. Initialize and register evidence with `init` and `observe`. Build the candidate contract from `schemas/spec.schema.json` with acceptance case IDs and explicit unsupported exports.
4. Run `check`, semantic review, `approve`, and `handoff`. Launch the implementer in a fresh restricted context using only the handoff.
5. When implementation is complete and validation authorized, wrap original/candidate independently behind the JSON-line comparison interface and use `validate`.
6. Filter mismatches through the firewall. Post-handoff contract revisions require a new run.

Deliver the independently written library, approved API scope, environment-bound conformance receipts, dependency notices, and remaining incompatibilities. A small suite does not establish total package parity.
