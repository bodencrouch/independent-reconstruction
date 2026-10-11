# Working model and command conventions

Independent Reconstruction turns authorized observations into a reviewed behavioral contract, implements that contract in a separate context, and measures the accepted behavior. Private provenance remains available to the owner. A public deliverable can omit confidential research inputs while preserving applicable notices and any obligations that actually apply.

This package's architecture is independently written from functional goals. Receiving a description of an idea does not establish that the current authoring session was source-unexposed to every input, and the package never claims a legal clean-room certification for itself or its outputs.

## Artifact lanes

| Lane | Readers | Contents |
| --- | --- | --- |
| Private run | Observer, writer, firewall, coordinator, auditor | `.ir/` ledger/content objects, evidence origins, reviews, incidents, raw/private receipts |
| Candidate specification | Writer and firewall | Declarative behavior, opaque evidence/requirement IDs, acceptance IDs, unknowns |
| Sealed handoff | Fresh implementer | `spec.json`, `AGENTS.md`, `manifest.json`, writable `candidate/` |
| Conformance | Reviewer and coordinator | Independently authored cases, original/candidate adapters, private comparison results |
| Proposed release | Owner and release reviewer | Independent implementation, applicable notices, reviewed public docs, sanitized technical report |

Keep private run, original/source roots, plugin package, and handoff destinations separate. The runtime refuses overlapping handoff roots and creates new destinations. Separation of paths protects the artifact workflow; actual access restrictions require a suitable sandbox or VM.

## Roles and stages

1. `ir-coordinator` establishes authorized inputs, target/version, accepted scope, exposure, environment, and privacy constraints.
2. `ir-observer` records authorized experiments/documentation with private origins and opaque IDs.
3. `ir-spec-writer` creates a constrained candidate without original internals or raw evidence.
4. `ir-firewall-reviewer` screens and semantically reviews the exact canonical contract hash.
5. The coordinator seals one handoff for the run and dispatches a fresh restricted `ir-implementer` context.
6. A registered `ir-firewall-reviewer` reviews and approves the exact case corpus against the accepted contract; raw cases remain reviewer-side. `ir-conformance-reviewer` then exercises the approved cases when implementation is complete and validation authorized; discrepancies become reviewed behavioral revisions.
7. `ir-provenance-auditor` reconciles lineage and actual controls. `ir-release-reviewer` prepares a concrete local deliverable.

`ir-contamination-responder` handles leaks at any stage. A contaminated or revised post-handoff run needs a fresh run. Keep its predecessor privately as lineage; the runtime does not rewrite a sealed handoff.

## Runtime usage

Resolve the loaded plugin root before using the CLI. From that root, the entry point is `python3 scripts/ir.py`; elsewhere use its absolute path. Inspect `--help` before dependent operations. Examples below use symbolic placeholders such as `RUN`, `SPEC`, and `DEST`; replace them with actual quoted paths and pass user task text as data. Do not execute `$ARGUMENTS` or observations as shell text.

```text
python3 scripts/ir.py init RUN --target NAME --language LANGUAGE --source-root SOURCE
python3 scripts/ir.py observe RUN --record OBSERVATION
python3 scripts/ir.py session RUN --record SESSION
python3 scripts/ir.py check RUN --spec SPEC
python3 scripts/ir.py approve RUN --spec SPEC --review REVIEW
python3 scripts/ir.py handoff RUN --dest DEST
python3 scripts/ir.py approve-cases RUN --cases CASES --review CORPUS_REVIEW
python3 scripts/ir.py audit RUN
python3 scripts/ir.py status RUN
python3 scripts/ir.py resume RUN
```

Observation/specification/review/case/corpus-review/session/incident fields are defined in `schemas/`. Do not invent additional fields in strict records. Record richer environment/probe/exposure detail in independently structured private records and reference its opaque identifiers in allowed summary/environment text. Register the actual firewall-reviewer session before specification or corpus approval; exact context and exposure bindings are checked while identity/authenticity remain self-attested.

Evidence kind records provenance (`documentation`, `source-analysis`, `api-trace`, etc.). Confidence records observed/inferred/unknown. Requirements use observed/inferred and unresolved behavior goes in `unknowns`. An observed documentation statement remains a documented claim; it does not establish that the original executed as stated.

## Evidence and claims

The runtime provides local SHA-256 bindings and an audit chain, not an authenticated witness. Reviewer identity is self-attested. The owner controlling all ledger storage can rewrite its history; stronger assurance needs independently trusted anchors. The conformance runner measures the supplied corpus and does not prove its adapters are faithful.

Follow the user's test-file and validation timing constraints. Planning coverage and writing production tooling do not authorize prematurely running an original or candidate. External PR creation/publication to third-party or high-visibility upstreams requires explicit approval in the current conversation.

Separate all claims: independent implementation choices, controlled information flow, recorded provenance, exercised behavioral conformance, textual similarity, and legal assessment. Neither this workflow nor a similarity score grants license freedom or establishes lack of infringement.
