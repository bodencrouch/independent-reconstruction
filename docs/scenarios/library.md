# Library replacement

Use this scenario for replacing a package or selected exports, including small utilities and substantial stateful libraries. Scope starts with what the consuming application actually requires and expands only through accepted requirements.

## Intake

Record package/version/digest, public exports, import/module modes, calling conventions, source and target runtime versions, supported operating systems, consumer usage, and compatibility exclusions. Register known original/source roots even when the observer never opens them. Preserve a source-informed classification for any agent that already read original code or upstream tests.

For a scalar validator, distinguish numbers, numeric strings, whitespace, empty strings, null/missing values, arrays/objects, Unicode digits, special floating values, infinities, and extreme representations. For a padding function, distinguish input coercion, empty/multibyte padding, negative/fractional lengths, already-long strings, Unicode code units versus characters, and allocation limits. These are observation topics, not assumptions about a particular package's behavior.

## Observation and specification

| Area | Distinguishing observation | Contract output |
| --- | --- | --- |
| Type semantics | Same value in distinct runtime types | Accepted/coerced/rejected input classes |
| Errors | Missing input, invalid input, resource limits | Error category, return shape, state after failure |
| Mutation | Reuse input object after operation | Ownership and observable changes |
| Ordering | Different insertion/order histories | Stable/unspecified iteration behavior |
| Runtime | Same case under supported runtime versions | Supported environment conditions |
| Async state | Cancel/retry/concurrent operations | State transitions and scheduling invariants |

Create independently authored synthetic probes and private evidence records. If the user permits upstream tests for analyst evaluation, retain their licenses/provenance and keep their code out of the implementer lane. An independent adapter may invoke a public API without sharing the original source.

Write accepted requirements with opaque evidence IDs and independently named cases. Public export/signature names require necessity review; original helper functions, module architecture, comments, and test narratives do not belong in the contract.

## Implementation

Use `/ir-spec`, `/ir-firewall`, `/ir-handoff`, and `/ir-implement`. The implementer chooses internal structure independently. Record newly used dependencies; importing the original as a hidden implementation dependency defeats the intended replacement.

If a callback, closure, generator, or asynchronous interface cannot be represented directly as JSON, define a reviewed adapter vocabulary for bounded operation sequences. For example, a sequence can create a handle, invoke operations, and emit observable values with synthetic handle IDs. The adapter must not leak original internal object IDs or stack traces.

## Acceptance

After complete implementation and authorized validation, compare independently written original/candidate adapters through `/ir-conformance`. Record consumer integration separately; case parity does not prove the consuming application has been migrated or works in deployment.

Report exported API coverage, environment, case outcomes, package/dependency notices, unsupported exports, performance/resource unknowns, and actual integration receipts. A 111-case suite, or any other fixed case count, proves only what its cases measure.
