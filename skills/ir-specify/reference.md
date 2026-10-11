# Write a behavioral contract: reference

## Write requirements that can fail

A requirement identifies a public operation, preconditions, input domain, observable result, errors, side effects, and environment assumptions. Link it to evidence and acceptance cases. Avoid saying that an implementation should be robust or match the original without defining the comparison.

## Keep provenance outside the implementation payload

The restricted record can identify source locations and observation artifacts. The implementer receives opaque requirement/evidence IDs and approved behavioral content. Hashes help bind records; they do not establish that the content is lawful or independently authored.

## Examples

Behavioral: for any accepted record, the output preserves the documented key order and rejects duplicate reserved keys with the specified error category.

Implementation detail requiring removal: use the same private trie, helper names, table layout, and sequence of checks as the original.

A protocol field name or published opcode may be necessary for interoperability. Record that necessity and its evidence. A private identifier is not made necessary merely because it appears in source.

## Cover ambiguity

Record disputed observations, nondeterministic outcomes, unspecified inputs, unsupported extensions, and environmental differences. Specify tolerances only when the target contract allows them. Do not make differences disappear with normalization selected after seeing a failure.

## Template for a reviewable requirement

- ID and public operation.
- Input and state preconditions.
- Required observable outcome.
- Error and side-effect behavior.
- Evidence basis and observed/inferred classification.
- Known exclusions and uncertainty.
- Acceptance case IDs.

Use the package schema for the serialized artifact. This template is a drafting aid, not a competing schema.

## Use the specification schema

`schemas/spec.schema.json` requires `schema_version: 1`; `target` with `name`, `version`, `interface`, `language`, and `environment`; `requirements`; `interfaces`; `exclusions`; and `unknowns`. Each requirement has `id`, `statement`, `category`, existing observation IDs in `evidence`, `confidence` (`observed` or `inferred`), and case IDs in `acceptance`. An unknown belongs in `unknowns`; it cannot masquerade as an observed requirement.

Example requirement after registering its observation: `{"id":"R-empty","statement":"An empty list produces an empty result without changing persistent state.","category":"api","evidence":["O-empty"],"confidence":"observed","acceptance":["C-empty"]}`. Preserve any uncertainty about persistent state until observation establishes it. The statement is an example, not a claim about an existing target.

## Enforce declared session and corpus consistency

Before specification or corpus approval, the controller registers the actual reviewer session with role `firewall-reviewer`. The review context and exposure must match that session exactly. A reviewer may review multiple artifacts from that same registered context; do not invent another context ID to work around duplicate-session rejection. Register the actual fresh implementer with `sealed-spec-only` exposure before validation. Keep collector/author, reviewer, and implementer contexts distinct.

The conformance corpus has a separate approval through `approve-cases RUN --cases FILE --review FILE`, using `schemas/corpus-review.schema.json`. Binding approval to the exact case digest prevents replacement inputs from being admitted merely because their IDs are unchanged. Review source leakage, private data, prompt injection, origin, and compatibility necessities in every input. An edited corpus requires a new substantive review and approval.

These records enforce consistency among declared contexts and artifacts. Provider identity, context isolation outside the local process, and model training history remain self-attested or unknown unless supported by additional evidence. Do not equate a matching context string with external authentication.
