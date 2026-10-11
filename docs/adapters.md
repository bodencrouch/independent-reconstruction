# Implement a behavioral adapter

An adapter command is a JSON array of executable and arguments. The runner never
invokes a shell. It launches each adapter once per case, sends the case's `input`
as one JSON value followed by newline on stdin, and expects exactly one JSON value
on stdout. Send diagnostics to stderr. Exit zero only after returning a valid value.
The runner bounds output file size and timeout and kills the process group on timeout.
Reference and candidate adapter commands run under the reviewer/controller account;
this runner is not itself an OS sandbox. Use separate VMs for untrusted programs.

Define original adapters with the same external mapping. Review that each actually
invokes the intended reference or candidate version. A wrapper that echoes canned
answers can pass a corpus without proving anything about the target software.
Pin executable/library digests, locale, architecture, toolchain and environment in
private observations. Runtime command hashes alone do not hash the entire executable
dependency closure. Raw values and adapter command paths stay in private reports.

Represent bytes as base64 plus a declared encoding; represent exceptional results
as tagged JSON objects. Compare structured errors only when the contract requires
the error fields. Exact comparison preserves types, array order and string bytes;
JSON object key order is ignored by canonicalization. Numeric comparison accepts
only top-level finite numbers with explicit absolute and relative tolerance.
No timestamps, addresses, line endings or floating values are normalized implicitly.

Stateful tests put a whole operation sequence inside a single input. The adapter
creates a fresh instance, applies operations and returns the result sequence.
For persistent state, create an isolated store and declare cleanup. Concurrent,
distributed, streaming, GUI and real-time systems need scenario-specific adapters
and original observer tooling. The generic runner does not synthesize those systems.

Original cases should cover empty, zero, negative, boundary, Unicode, malformed,
error, state reset, ordering and resource conditions as applicable. Add independent
held-out inputs, metamorphic relations and fuzzing in reviewer-owned tooling. Record
seed and failing input privately; have the firewall review any behavior amendment.
Do not copy upstream test files into the implementer's context as a shortcut.

Reference adapter crashes are measurement failures, even when the candidate crashes
the same way. Model an intentional error as a tagged JSON result if error semantics
are part of the contract. Do not treat two failed runs as conformance.
