# Specify a file format: reference

## Separate reading and writing

A parser may accept several representations while the writer emits one canonical representation. Byte-for-byte output comparison is appropriate only when required. A semantic comparator needs a reviewed definition and must not hide unsupported fields or data loss.

## Include hostile and partial inputs

Probe truncation, oversized lengths, invalid checksums, duplicate fields, unknown tags, nested depth, cyclic references where possible, encoding errors, empty content, and trailing bytes. Run hostile artifacts in a bounded validator environment.

## Record preservation

Specify which fields, ordering, unknown extensions, whitespace, comments, and metadata survive a read/write cycle. Avoid claiming lossless compatibility when the adapter discards unobserved data.

## Evidence rules

A sample file is itself an artifact with origin, license/access basis, version, and privacy classification. Redacting private bytes can change behavior; retain the private original and disclose which synthetic replacement was validated.

A public magic number or format tag may be necessary. An original implementation table may contain a mix of necessary values and protected arrangement. Route that decision through the firewall; do not copy the table mechanically.

## Example

The candidate reads both supported endian variants, rejects a length larger than available payload, and preserves unknown chunks on rewrite. The contract states these requirements and approved examples. It leaves allocation, dispatch, and internal object design open.
