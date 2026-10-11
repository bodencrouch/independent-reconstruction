# Cross-language reconstruction

Use this scenario for a compatibility port whose implementation language differs from the original. Translation of source remains source-derived work; an independent behavioral implementation requires its own observed contract and exposure records.

## Semantic inventory

| Area | Possible compatibility difference |
| --- | --- |
| Integers/floats | Overflow, precision, negative zero, NaN/infinity, division |
| Strings | Code units/code points, normalization, invalid encoding, indexing |
| Values | Null, undefined/missing, booleans, coercion, truthiness |
| Containers | Key equality, ordering, duplicates, identity, mutation |
| Errors | Exceptions versus return values, error category, cleanup |
| Async | Cancellation, scheduling, callbacks, backpressure, races |
| Runtime | Locale, time-zone, filesystem/process behavior, dependency APIs |

Observe cases that distinguish these semantics. Do not silently implement the target language's defaults where the contract requires different behavior. Unsupported source-runtime quirks must be explicit exclusions rather than guessed parity.

## Handoff

Write a language-neutral contract with exact public interfaces only where needed. Examples use synthetic data and independently described operations. The implementer receives no original source, algorithm translation, private type names, upstream tests, or source-informed parent summary.

The implementer chooses target-language structure and independently licensed dependencies. Bind toolchain/runtime versions and packaging constraints separately from original implementation details. Do not require matching an original class hierarchy to satisfy a public protocol.

## Adapters and comparison

Each side translates its public input/output into a reviewed comparison representation. Define treatment of values JSON cannot represent directly: missing fields, bytes, large integers, special floats, handles, and callbacks. Adapter transformations are part of the compatibility claim and need private provenance review.

Exact mode compares canonical JSON, not all language-level identity/mutation semantics. Numeric mode compares only two scalar finite JSON numbers with approved absolute/relative tolerances. Use independently defined structured encodings and explicit requirements for additional semantics.

Stateful sequences run inside a single adapter input; separate cases start separate processes. Validate only after complete implementation and authorization, with recorded environments and independently authored cases.

## Acceptance

Report required semantic emulation, explicit intentional differences, case/environment coverage, packaging/runtime receipts, third-party notices, and unsupported features. A different language may reduce superficial textual similarity while preserving source lineage; it is not a legal conclusion.
