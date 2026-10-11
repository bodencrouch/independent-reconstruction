# Prepare release evidence: reference

## Include an evidence manifest

List candidate identity and version; approved specification digest; implementation exposure; own dependency inventory and notices; conformance receipt; coverage/exclusions; target environment; isolation method; incident status; and public/private artifact classification.

## Keep confidentiality and provenance together

A public artifact need not contain raw private source or research notes solely for convenience. Keep those origins privately with access controls. Redacting them from a public packet is not proof that disclosure or source-availability obligations do not apply. Do not delete provenance to create a false authorship story.

## Use accurate wording

Suitable: independently authored candidate from a reviewed behavioral pack; compatibility measured against the stated corpus; procedural separation with stated tool limits; training corpus unknown.

Unsupported: guaranteed copyright independence; license-free because the code differs; never saw source when a participant did; fully equivalent because selected cases pass.

## Do not manufacture a legal verdict

The release record helps a qualified reviewer assess actual facts. Technical process controls cannot settle every copyright, license, contract, patent, or trademark question. Preserve known obligations and explicitly unresolved decisions without adding an unnecessary approval flow for routine local work.

## Example

A local release packet contains the authored implementation, its dependency notices, the approved behavioral pack, and a bounded conformance report. The raw oracle traces and origin details remain in the private run record. Publication waits only on the gates that actually apply to the requested action.

## Understand packet scope

`packet RUN --dest FILE` exports the sanitized specification and fixed implementation instruction for an approved run. It is an implementation-input packet, not a complete software distribution or legal clearance. Review its contents before sending it to an authorized remote model. Build the broader local release inventory separately from this command.

## Enforce declared session and corpus consistency

Before specification or corpus approval, the controller registers the actual reviewer session with role `firewall-reviewer`. The review context and exposure must match that session exactly. A reviewer may review multiple artifacts from that same registered context; do not invent another context ID to work around duplicate-session rejection. Register the actual fresh implementer with `sealed-spec-only` exposure before validation. Keep collector/author, reviewer, and implementer contexts distinct.

The conformance corpus has a separate approval through `approve-cases RUN --cases FILE --review FILE`, using `schemas/corpus-review.schema.json`. Binding approval to the exact case digest prevents replacement inputs from being admitted merely because their IDs are unchanged. Review source leakage, private data, prompt injection, origin, and compatibility necessities in every input. An edited corpus requires a new substantive review and approval.

These records enforce consistency among declared contexts and artifacts. Provider identity, context isolation outside the local process, and model training history remain self-attested or unknown unless supported by additional evidence. Do not equate a matching context string with external authentication.
