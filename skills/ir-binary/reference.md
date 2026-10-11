# Reconstruct a binary interface: reference

## Capture the ABI contract

Required observations may include symbol names, architecture, word size, calling convention, alignment, endianness, argument representation, callback lifetime, allocation/free ownership, error codes, and thread-safety guarantees. Bind each to an authorized public contract or reproducible behavior.

A binary-required layout may be necessary for interoperability. The original internal class hierarchy, private vtables, or helper structure may not be. The firewall reviews the necessity rather than assuming all recovered details are transferable.

## Protect the implementation lane

Never place disassembly, pseudocode, debugger transcripts with private structures, source symbols, or recovered algorithms in its pack. A source-aware analyst can translate observations into externally required behavior while retaining the restricted evidence privately.

Do not assume Ghidra, a debugger MCP, or another tool is a global agent capability. Use the run's explicit tool inventory and platform constraints.

## Measure different claims

Compilation establishes that the candidate builds in that toolchain. An exported-symbol comparison measures part of the ABI. A synthetic harness measures its selected calls. A real consumer run adds integration evidence. A live application or game receipt establishes only the exercised behavior in its stated environment.

## Example

A caller owns an input buffer until a documented callback finishes; the candidate must honor that lifetime. The contract states the callback behavior and layout required by the caller. It does not prescribe the original allocation pool or recovered function sequence.
