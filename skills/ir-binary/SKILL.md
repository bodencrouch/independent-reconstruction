---
name: ir-binary
description: Defines observable ABI and binary interoperability contracts without transferring disassembly or original internal structure to implementers. Use explicitly for native SDK, executable, or binary compatibility reconstruction.
disable-model-invocation: true
---
# Reconstruct a binary interface

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Define whether the goal is ABI compatibility, executable behavior, file compatibility, or a host integration. Pin architecture, platform, calling convention, artifact digest, and toolchain.
2. Keep disassembly, decompiler output, debug symbols, internal names, and source-assisted notes in the restricted collector lane. Use only authorized tools and artifacts.
3. Observe public exports, calling conventions, layout constraints, ownership, lifetime, error behavior, threading requirements, and externally visible side effects.
4. Express the contract with evidence for required public names, offsets, flags, and constants. Distinguish required binary layout from an unnecessary copy of internal structures.
5. Review the contract through the firewall and export it to the independent implementation lane.
6. Design and, when authorized, execute interoperability probes against real consumers with a isolated harness. Record crashes and unsupported architecture separately from behavioral mismatches.
7. Report ABI, platform, and consumer proof independently. Do not infer live compatibility from compilation or static inspection.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" observe "$RUN" --record "$BINARY_OBSERVATION_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" check "$RUN" --spec "$SPEC_JSON"
```

## Return

Return the pinned artifact, public ABI requirements, layout necessities and evidence, ownership/threading contract, supported platforms, actual consumer receipts, and unverified behavior.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
