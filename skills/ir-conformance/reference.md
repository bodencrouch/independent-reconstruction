# Measure behavioral compatibility: reference

## Compare the contract

Before running a case, decide which observables matter. Exact bytes may be required for a wire protocol. A numeric API may permit a documented tolerance. A CLI may require stderr category and exit status while leaving timing unspecified. Do not choose normalization after seeing differences merely to improve the score.

The engine's direct runner supports its documented input/output model. State, side effects, protocol sessions, and performance often require separate adapters; do not imply that a stdin/stdout comparison measures them automatically.

## Build a case matrix

Include normal, boundary, malformed, regression, and integration cases. Add seeded generative probes only within an authorized validation phase. Record input generation method and seed. Minimize failures while preserving the actual behavioral difference.

Unknown requirements remain unknown even when every current case passes. Report both case counts and contract coverage. Cases selected from the candidate's behavior alone can miss oracle differences.

## Command inputs

`ORACLE_COMMAND_JSON` and `CANDIDATE_COMMAND_JSON` contain JSON arrays such as `["python3", "oracle_adapter.py"]`. Quote them when passing them to the CLI. Adapters consume the documented case format and emit only the observable output. Their own failures need separate diagnoses.

## Example feedback

Requirement R-6; synthetic input is an empty array following reset; oracle returns the documented empty result; candidate returns an error category. Include the sequence and approved outputs. Exclude original internal stack frames and guessed implementation fixes.

## Report bounds

State the exact version, platform, runtime, corpus, comparison policy, case statuses, requirement coverage, resource limits, and known exclusions. Passing the corpus is evidence of measured behavior, not complete equivalence or copyright independence.

## Use the cases schema

`schemas/cases.schema.json` requires `{"schema_version":1,"cases":[...]}`. A case has `id`, `requirement_ids`, arbitrary JSON `input`, and `comparison`. `exact` forbids a tolerance object; `numeric` requires both nonnegative `tolerance.absolute` and `tolerance.relative`. Use only tolerance already justified by the reviewed contract.

Example: `{"id":"C-empty","requirement_ids":["R-empty"],"input":[],"comparison":"exact"}`. Register its requirement in the approved specification. The direct runner passes JSON input to each command; adapters are responsible for turning public protocol, file, or state sequences into this interface.

## Enforce declared session and corpus consistency

Before specification or corpus approval, the controller registers the actual reviewer session with role `firewall-reviewer`. The review context and exposure must match that session exactly. A reviewer may review multiple artifacts from that same registered context; do not invent another context ID to work around duplicate-session rejection. Register the actual fresh implementer with `sealed-spec-only` exposure before validation. Keep collector/author, reviewer, and implementer contexts distinct.

The conformance corpus has a separate approval through `approve-cases RUN --cases FILE --review FILE`, using `schemas/corpus-review.schema.json`. Binding approval to the exact case digest prevents replacement inputs from being admitted merely because their IDs are unchanged. Review source leakage, private data, prompt injection, origin, and compatibility necessities in every input. An edited corpus requires a new substantive review and approval.

These records enforce consistency among declared contexts and artifacts. Provider identity, context isolation outside the local process, and model training history remain self-attested or unknown unless supported by additional evidence. Do not equate a matching context string with external authentication.

## Use the corpus review schema

`schemas/corpus-review.schema.json` requires integer `schema_version: 1`, the exact canonical `spec_sha256` and `cases_sha256`, `reviewer` with `identity`, `context_id`, and `exposure`, `corpus_origin`, `decision`, `findings`, and nonempty `limits`. A finding has `severity` (`blocking` or `advisory`), a case ID present in the corpus, and `reason`. Use `digest` on both artifacts rather than hashing their incidental JSON whitespace.

`corpus_origin: original` means independently authored cases for this run; it does not mean the upstream project's original test suite. `authorized-reference` means an authorized third-party corpus retained in the reviewer lane. That classification records an access basis; it does not authorize exposing its test implementation to the implementer or removing its notices. Only reviewed behavioral inputs and counterexamples cross the boundary.

The specification and corpus approvals use separate review artifacts. Both must name the actual registered reviewer context and exposure. Session records have no `schema_version` field. Registration and matching remain self-attested process facts; the local tool does not authenticate a remote model or prove its training history.
