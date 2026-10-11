# Review the information boundary: reference

## Review both expression and structure

Changing names or programming language can leave the same implementation structure in a specification. Review whether the draft dictates original decomposition, branch order, data structures, optimization choices, or private error wording without an externally required reason.

Automated matching can flag suspicious overlap. A low score can miss translated code, tables, comments, nonliteral structure, or material from outside the comparison corpus. A high score can arise from necessary public symbols or standard boilerplate. Record findings without treating a threshold as a verdict.

## Decision record

Include the exact specification digest, reviewer identity and role, reviewed evidence IDs, decision, finding IDs, corrective actions, compatibility necessities, and limitations. Use the package review schema. A reviewer declaration is attributable process evidence; the program cannot prove that the human or model identity is independent.

## Reject these handoffs

- A source function rewritten as prose instructions.
- Original tests copied into the implementation pack without an explicit basis.
- Source paths or comments embedded in examples.
- A summary that tells the implementer to inspect the original repository.
- Base64, compressed, quoted, or hidden data carrying restricted content.
- A vague approval that is not bound to the artifact's digest.

## Review feedback too

A conformance failure may reveal expected output, public state transition, and a minimal synthetic input. It must not reveal the original fix, private stack frames, internal helper names, or diagnostic dumps. Apply the same firewall to follow-up prompts and issue bodies.

## Example

Keep a field name published in a wire contract after recording why peers require it. Remove an unrelated private class name. Replace an algorithm description with observable input/output requirements supported by recorded cases.

## Use the review schema

`schemas/review.schema.json` binds `schema_version: 1` and `spec_sha256` to the exact canonical specification digest reported by the engine. Include `reviewer.identity`, `reviewer.context_id`, and `reviewer.exposure` (`review-only` or `source-exposed`); `decision` (`approve` or `reject`); `findings` with `severity`, `requirement_id`, and `reason`; and `limits`. Use a real participant/context identity. Never manufacture a reviewer to bypass a distinct-review requirement.

A role environment variable and host hook are administrative checks. The same operating-system user can alter or bypass them. Document that limit and use a verified process/capability boundary when enforcement is required.

## Enforce declared session and corpus consistency

Before specification or corpus approval, the controller registers the actual reviewer session with role `firewall-reviewer`. The review context and exposure must match that session exactly. A reviewer may review multiple artifacts from that same registered context; do not invent another context ID to work around duplicate-session rejection. Register the actual fresh implementer with `sealed-spec-only` exposure before validation. Keep collector/author, reviewer, and implementer contexts distinct.

The conformance corpus has a separate approval through `approve-cases RUN --cases FILE --review FILE`, using `schemas/corpus-review.schema.json`. Binding approval to the exact case digest prevents replacement inputs from being admitted merely because their IDs are unchanged. Review source leakage, private data, prompt injection, origin, and compatibility necessities in every input. An edited corpus requires a new substantive review and approval.

These records enforce consistency among declared contexts and artifacts. Provider identity, context isolation outside the local process, and model training history remain self-attested or unknown unless supported by additional evidence. Do not equate a matching context string with external authentication.

## Use the corpus review schema

`schemas/corpus-review.schema.json` requires integer `schema_version: 1`, the exact canonical `spec_sha256` and `cases_sha256`, `reviewer` with `identity`, `context_id`, and `exposure`, `corpus_origin`, `decision`, `findings`, and nonempty `limits`. A finding has `severity` (`blocking` or `advisory`), a case ID present in the corpus, and `reason`. Use `digest` on both artifacts rather than hashing their incidental JSON whitespace.

`corpus_origin: original` means independently authored cases for this run; it does not mean the upstream project's original test suite. `authorized-reference` means an authorized third-party corpus retained in the reviewer lane. That classification records an access basis; it does not authorize exposing its test implementation to the implementer or removing its notices. Only reviewed behavioral inputs and counterexamples cross the boundary.

The specification and corpus approvals use separate review artifacts. Both must name the actual registered reviewer context and exposure. Session records have no `schema_version` field. Registration and matching remain self-attested process facts; the local tool does not authenticate a remote model or prove its training history.
