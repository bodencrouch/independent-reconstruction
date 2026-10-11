# Port the behavioral contract: reference

## Compare semantics deliberately

| Boundary | Contract questions |
| --- | --- |
| Numbers | Precision, overflow, NaN, infinity, signed zero, rounding |
| Strings | Bytes/code points, normalization, invalid encoding, locale |
| Collections | Ordering, duplicate keys, mutation visibility, equality |
| Errors | Category, message necessity, stack visibility, status |
| Async behavior | Cancellation, callback order, timeout, retry |
| Time | Calendar, timezone, clock source, serialization |

Do not quietly adapt the oracle to target-language defaults. Either preserve the required behavior or record an intentional incompatibility approved in scope.

## Use fresh design

The implementation may use idiomatic ownership, error handling, data structures, and modules. It must not receive a line-by-line algorithm translation or the original decomposition disguised as a specification.

A cross-language candidate can still reproduce protected expression or structure. This workflow measures behavior and records exposure; it does not establish a license exemption.

## Example

An original API accepts a numeric string and rejects whitespace-only text. Observe the exact coercion boundary, then specify it. A Rust implementation can choose an independently designed parser while satisfying the approved input/output contract.

## Adapter evidence

Record adapter source origin and version. If serialization loses large integers, nonfinite floats, or key order, correct the adapter before claiming compatibility. Store raw comparison outputs privately and pass only reviewed counterexamples to implementation.
