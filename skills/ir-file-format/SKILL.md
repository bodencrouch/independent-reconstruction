---
name: ir-file-format
description: Reconstructs parser and writer contracts for file formats, including canonicalization, malformed inputs, and round trips. Use explicitly for format interoperability or archive/document compatibility.
disable-model-invocation: true
---
# Specify a file format

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Pin format variants, producer/consumer versions, encodings, and authorized sample provenance. Use synthetic samples where possible and preserve originals privately.
2. Observe headers, lengths, tags, checksums, ordering, endianness, alignment, optional fields, unknown extensions, and error behavior.
3. Distinguish required format structure from original parser implementation. Document what exact bytes are necessary and what allows multiple valid encodings.
4. Capture read/write behavior separately: accepted inputs, emitted canonical form, round-trip preservation, metadata loss, and malformed input handling.
5. Prepare reviewed examples with approved sample bytes and source-free descriptions. Exclude original parser code, copied comments, and undocumented implementation tables unless a necessary public format contract justifies their transfer.
6. Run `check`; route necessity decisions through the firewall. Use conformance adapters for parse/write/round-trip comparisons in an authorized validation phase.
7. Report format versions, corpus coverage, supported extensions, preservation limits, and resource limits.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" observe "$RUN" --record "$FORMAT_OBSERVATION_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" check "$RUN" --spec "$SPEC_JSON"
```

## Return

Return the format contract, approved sample provenance, canonicalization policy, parser/writer coverage, malformed cases, unsupported extensions, and interoperability evidence.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
