# Coordinate a reconstruction: reference

## Divide the work

| Responsibility | Inputs | Output | Must not receive |
| --- | --- | --- | --- |
| Collector | Authorized oracle and restricted evidence | Observations with provenance | Candidate design used to guess oracle output |
| Specification author | Observations and approved external contracts | Behavioral requirements | Permission to transfer arbitrary source excerpts |
| Firewall reviewer | Draft contract and restricted provenance | Decision on an exact digest | A request to approve by similarity score alone |
| Implementer | Approved contract and candidate workspace | Independently written candidate | Raw source, collector context, restricted notes |
| Validator | Approved cases, pinned oracle, candidate | Behavioral differences | Permission to inject original implementation into candidate |
| Auditor | Run metadata, hashes, decisions, exposure records | Bounded evidence report | Authority to certify legal independence |

## Use the right mode

Black-box observation uses an executable or public interface. Source-assisted analysis permits designated collectors to examine source while keeping the implementer separate. Documentation reconstruction starts from licensed or authorized interface descriptions. An ordinary port may permit source reuse under its license; label it honestly instead of calling it clean room.

A fresh model conversation prevents inherited prompts. It does not prevent the process from reading neighboring files, querying tools, accessing shared memory, or recalling training data. Record these remaining paths. A shared unrestricted workspace supports only a procedural separation claim.

For a large system, partition public interfaces into approved contract packs. Keep shared state, version negotiation, error semantics, and dependency boundaries explicit. Integrate only packs whose individual provenance and acceptance records remain valid.

## Example

A replacement for a record parser targets a documented input format and two consumer applications. The collector observes successful and malformed inputs. The contract states outputs and errors. The implementer receives the contract, canonical input bytes, and approved cases. The validator checks both consumer applications and records any unsupported extensions.

A bug report that reveals an original private helper or copied loop returns to the firewall. It is not forwarded to the implementer.

## Enforce declared session and corpus consistency

Before specification or corpus approval, the controller registers the actual reviewer session with role `firewall-reviewer`. The review context and exposure must match that session exactly. A reviewer may review multiple artifacts from that same registered context; do not invent another context ID to work around duplicate-session rejection. Register the actual fresh implementer with `sealed-spec-only` exposure before validation. Keep collector/author, reviewer, and implementer contexts distinct.

The conformance corpus has a separate approval through `approve-cases RUN --cases FILE --review FILE`, using `schemas/corpus-review.schema.json`. Binding approval to the exact case digest prevents replacement inputs from being admitted merely because their IDs are unchanged. Review source leakage, private data, prompt injection, origin, and compatibility necessities in every input. An edited corpus requires a new substantive review and approval.

These records enforce consistency among declared contexts and artifacts. Provider identity, context isolation outside the local process, and model training history remain self-attested or unknown unless supported by additional evidence. Do not equate a matching context string with external authentication.
