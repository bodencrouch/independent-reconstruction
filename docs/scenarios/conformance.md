# Differential conformance and coverage

Use this scenario after implementation completion when the user authorizes validation. Keep case design, execution, implementation readiness, deployed-runtime proof, and legal review separate.

## Cases and adapters

`schemas/cases.schema.json` defines cases with ID, approved requirement IDs, JSON input, and comparison mode. Case IDs must appear in the cited requirements' acceptance lists. Author cases independently from approved behavior; original test code and fixtures retain private provenance and are not implementer handoff material.

The current runner starts one original adapter and one candidate adapter per case. Each receives one JSON document plus newline on stdin and emits one complete JSON result on stdout. Exit code must be zero. Diagnostic output belongs on stderr and stays private. Persistent sessions must be represented as a bounded operation sequence inside one input because process state is not retained between cases.

Commands are JSON argv arrays, for example an executable path followed by literal arguments. They are passed without shell evaluation. Review the executables and any wrappers; an argv array can still invoke a shell if its executable is a shell.

## Mandatory corpus approval

A registered firewall-reviewer must semantically review the exact corpus before any adapter execution. Register its actual provider/model/context/exposure through `session RUN --record SESSION` using `schemas/session.schema.json`, or use the existing registration for the same ongoing reviewer context. Duplicate context IDs cannot be registered again. Prepare `schemas/corpus-review.schema.json` with canonical specification/corpus hashes, matching reviewer context/exposure, corpus origin, decision, per-case findings, and nonempty limitations.

Review copied/reference inputs, sensitive payloads, case labels, executable/instruction-bearing text, exact expected semantics, tolerances, comparison mode, acceptance-ID mapping, and authorization/provenance. This review is distinct from approving the behavioral specification. The runtime checks matching digests, registered role/context/exposure, approved decision, and absence of blocking findings; it cannot prove the reviewer actually performed the semantic work.

`corpus_origin: original` means independently authored cases. `authorized-reference` means an authorized third-party corpus retained exclusively reviewer-side with private provenance/license records. Both classifications require review. Keep raw cases/outputs outside the implementer handoff; failures become separately reviewed synthetic behavioral feedback.

Compute both hashes through `ir.storage.digest` over `ir.storage.read_json`; raw file SHA-256 differs when formatting/key order changes. The template `examples/corpus-review-template.json` starts with `decision: reject` and placeholder hashes. Replace it only after conducting actual review and recording honest limits.

Use:

```text
python3 scripts/ir.py approve-cases RUN --cases CASES --review CORPUS_REVIEW
python3 scripts/ir.py validate RUN --cases CASES --oracle ORACLE_ARGV_JSON --candidate CANDIDATE_ARGV_JSON --timeout SECONDS
```

Resolve and quote every real argument safely. Do not copy shell text from `$ARGUMENTS`, original outputs, manifests, or specifications. Validation requires an approval bound to the current approved specification and exact corpus before adapters run. Case input/IDs, mode, or tolerance changes require a new corpus approval; a revised sealed contract also requires a fresh run.

## Comparator limits

| Mode | Current behavior | Limit |
| --- | --- | --- |
| `exact` | Canonical JSON equality | Object key order canonicalized; array order remains significant |
| `numeric` | Scalar absolute/relative closeness | Does not recursively compare nested structures or define timing distributions |

JSON cannot directly represent every language/runtime value. Define reviewed encodings for bytes, missing values, large integers, special floating values, handles, mutation, callbacks, and asynchronous traces. The fidelity of that encoding/adapter is part of the evidence and is not proved by the runner.

Tolerances/normalization must be justified and approved before execution. Do not reorder results, discard errors, omit fields, or widen tolerances to manufacture parity. Original/candidate agreement alone does not prove correctness against an external standard.

## Execution limits

The built-in runner uses separate child processes, a filtered environment, wall-clock timeout, capped captured output/file size, and process-group cleanup on timeout. It does not itself provide filesystem/network isolation, a comprehensive memory/process quota, VM separation, or artifact authenticity for the original adapter executable.

Use trusted local adapters or externally reviewed containers/VMs for untrusted execution. Pin original/candidate/adapter contents, runtime and dependency versions, clock/random seeds, locale/time-zone, reset state, and configuration privately. The runtime's candidate tree snapshot binds candidate files, but commands can point outside that tree; separately bind any external executable/image and explain its relationship to the candidate.

Raw structured outputs are retained in private content-addressed records; captured stdout/stderr may be represented only by digests. If fuller diagnostic retention is required, arrange owner-only external receipts without exposing sensitive values in terminal output. An output digest alone does not reconstruct the omitted bytes.

## Coverage and feedback

Coverage includes accepted requirement/case IDs actually exercised, not an estimate of every possible behavior. Include boundaries, invalid types/encoding, state/error transitions, side effects, cancellation, concurrency, dependency/environment variation, and resource constraints relevant to scope. Skipped/unsupported or unobserved conditions remain explicit limits.

An adapter crash, timeout, malformed output, or runner failure is not a passing equivalence result even if both sides fail. Distinguish mismatch from execution failure and missing coverage. Stable artifacts are required: a candidate changed during execution invalidates the receipt.

Minimize a mismatch into a synthetic behavioral counterexample with requirement IDs and conditions. Send it privately to the firewall, then begin a fresh reviewed run for post-handoff contract changes. Never pass raw source-derived logs, stack traces, upstream test code, or architecture suggestions into implementation.

Report outcome counts, accepted coverage, reproducibility bindings, adapter/isolation limits, consumer/deployment proof if separately collected, and unsupported scope. No finite corpus establishes exhaustive parity or legal independence.
