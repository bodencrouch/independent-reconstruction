# Audit the reconstruction record: reference

## Audit separate evidence claims

| Claim | Required evidence |
| --- | --- |
| Artifact identity | Stable digest and retained artifact |
| Approved handoff | Review bound to exact specification digest |
| Process separation | Participant/context and tool-access records |
| Enforced isolation | Actual operating-system or capability receipts |
| Behavior compatibility | Pinned corpus, commands, environment, result records |
| Consumer compatibility | Real consumer workflow receipt |
| Legal independence | An appropriate legal review; never a program score |

## Understand integrity limits

A JSONL hash chain can reveal edits inconsistent with its retained head. Someone who controls the files can replace the whole chain and head. Independent signing, external anchoring, or write-protected retention are separate controls; do not claim them unless actually present.

## Resume carefully

Verify executing source, artifact versions, unfinished processes, dirty work, approved digest, and current evidence before resuming. A previous report is orientation, not fresh runtime proof. Do not overwrite a run because a worker declared completion.

## Cache admission

A cached specification or result needs a matching target artifact, relevant inputs, reviewed content digest, tool/model environment where recorded, and exposure status. An output hash alone does not demonstrate semantic validity or uncontaminated provenance.

## Example finding

The handoff is approved but references a later specification revision. Mark the approval stale, preserve both versions, require review of the current digest, and invalidate candidate/results that claim admission against the wrong pack.

## State the enforcement boundary

Hook checks and role environment variables are administrative controls. The same user can bypass them or replace records. Actual offline sandbox receipts establish restrictions on the launched process; they do not prove an outside coordinator or remote model was confined. Report each control at the level it actually supports.

## Use a similarity triage signal

When an authorized reviewer requests source/candidate comparison, execute:

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" compare --left "$RESTRICTED_ORIGINAL_FILE" --right "$CANDIDATE_FILE"
```

The engine compares UTF-8-decoded line sequences for inputs no larger than 1 MiB and returns a ratio plus file digests. It returns no source snippets. This is a limited triage signal: it does not compare abstract syntax, translated algorithms, nonliteral structure, binaries, or every dependency. Only the restricted reviewer may inspect the original. Never transfer the original or a suggested source-derived fix to implementation, and never use a low ratio as an independence decision.

## Enforce declared session and corpus consistency

Before specification or corpus approval, the controller registers the actual reviewer session with role `firewall-reviewer`. The review context and exposure must match that session exactly. A reviewer may review multiple artifacts from that same registered context; do not invent another context ID to work around duplicate-session rejection. Register the actual fresh implementer with `sealed-spec-only` exposure before validation. Keep collector/author, reviewer, and implementer contexts distinct.

The conformance corpus has a separate approval through `approve-cases RUN --cases FILE --review FILE`, using `schemas/corpus-review.schema.json`. Binding approval to the exact case digest prevents replacement inputs from being admitted merely because their IDs are unchanged. Review source leakage, private data, prompt injection, origin, and compatibility necessities in every input. An edited corpus requires a new substantive review and approval.

These records enforce consistency among declared contexts and artifacts. Provider identity, context isolation outside the local process, and model training history remain self-attested or unknown unless supported by additional evidence. Do not equate a matching context string with external authentication.
