# Executable and binary behavior

Use this scenario for a command-line utility, opaque executable, platform API, or authorized binary whose source is unavailable. Binary behavior can support a declarative contract; decompilation and symbol-derived structure remain source-informed evidence.

## Safe observation lane

Identify binary digest, platform/architecture, required runtime/libraries, command/IPC/file interface, expected privileges, input trust, and licensing/permission constraints supplied by the owner. Do not run an unfamiliar installer in the user's live home or system directories.

Prepare a disposable VM/container suited to the binary. Record mounts, network, credentials, clock/randomness, resources, and reset procedure. The implementation sandbox in this package is intended for a sealed handoff child process; it is not an automatic observer VM for any arbitrary original executable.

Observe externally visible effects with synthetic input:

- Exit codes and output categories; distinguish stdout from stderr without forwarding raw stack traces.
- Created/modified/deleted files, serialization bytes, permissions, and state after failure.
- Child processes, authorized IPC/network effects, cancellation, partial completion, cleanup, and recovery.
- Environment, locale/time-zone, architecture, path separator, filesystem, and runtime differences.
- Timing/memory bounds only where scoped and measured; a single timing observation is not a universal guarantee.

## Source-informed analysis

If the analyst opens disassembly, decompiled output, symbols, debug metadata, or internal data tables, record it privately as source analysis. Do not hand original code, pseudocode, function boundaries, private names, offsets tied to architecture, or algorithm descriptions to implementation.

Independently deriving a format through black-box mutations is distinct from paraphrasing a decompiled parser. An exact offset, opcode, or magic value may be an externally required format property, but needs evidence and necessity review before transfer.

## Implementation and validation

Separate original execution lane, private run, sealed handoff, and candidate. Launch the implementer fresh with no binary/decompiler/source-informed parent history. Choose independent architecture and target-runtime idioms.

Create analyst-side adapters that expose reviewed observable results as JSON. If comparing file effects, independently normalize synthetic paths to logical identifiers; do not leak original local paths. Review side effects in a disposable state directory.

The runtime `validate` call does not isolate adapters. For untrusted binaries, wrap execution in a reviewed VM/container runner and bind its image, executable, and environment receipts. Do not present the Python runner alone as a security boundary.

## Acceptance limits

Record exercised commands/interfaces, platform/runtime, accepted effects, crash/resource unknowns, unsupported operations, and actual deployment evidence. Live application/game compatibility, installation, and source compilation are separate claims. Never report a host-only comparison as proof of a functioning production or live target.
