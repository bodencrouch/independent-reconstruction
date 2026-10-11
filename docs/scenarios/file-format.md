# File formats and serializers

Use this scenario for parsers, writers, exporters, importers, archive formats, schema converters, and binary/structured document interoperability. A reader and a writer can have different accepted compatibility scopes.

## Build a controlled corpus

Use user-owned or authorized synthetic samples. Record source/provenance for standards, schemas, third-party fixtures, tables, and assets. Keep proprietary documents and unreviewed sample metadata private.

Start with a minimal valid sample and vary one observable property at a time. Include zero-length and maximal fields, invalid lengths, truncation, missing/duplicate/unknown fields, optional sections, corrupted checksums, invalid encoding, compressed content, recursive/nested structures, and unsupported versions where authorized.

## Declarative contract

| Property | Requirement form |
| --- | --- |
| Framing | Required byte/field boundaries and valid length relationships |
| Numeric representation | Width, signedness, byte order, valid range |
| Text | Encoding, invalid sequence handling, normalization if required |
| Optional/unknown fields | Preservation, skipping, rejection, or documented exclusion |
| Canonicalization | Required output ordering/spacing/representation |
| Integrity | Externally required checksum/signature semantics |
| Resources | Accepted sizes/depth limits and error behavior |

Exact format constants and field names need interoperability necessity review. Original parser decomposition, copied prose from standards, private lookup/model tables, source comments, and proprietary schema text remain outside the implementer handoff unless independently authorized and honestly classified for another lane.

Round-trip preservation can mean semantic equivalence, field preservation, or identical bytes. Specify which one applies. An importer that discards unknown sections cannot claim lossless round-trip based on successful parsing alone.

## Independent implementation

The implementer receives only approved declarative requirements and synthetic examples expressed within the schema. It chooses parser architecture, internal representation, and error handling independently. Original samples and original parser code stay observer/reviewer-side.

Review dependencies, generated schema code, compression libraries, assets, and fixtures before distribution. Independent parser code does not remove notices attached to included tables or generated third-party material.

## Comparison

Adapters may expose semantic JSON values, validation categories, or encoded output bytes in an independently defined textual representation. Exact JSON comparison orders object keys canonically while preserving array order; raw byte equality must be an explicit adapter result/requirement. Numeric scalar tolerance does not implement fuzzy binary or tree comparison.

Run malformed/untrusted inputs in externally reviewed isolation after authorized completion. The built-in differential runner does not sandbox parsers or enforce a memory limit. Document untested expansion/recursion/resource hazards as limits instead of inventing passing receipts.

Deliver supported versions, read/write scopes, preservation guarantees, resource limits, accepted incompatibilities, and the actual corpus/environment measured.
