# Separate evidence from implementation

## Define the target

Pin the reference version, environment, interfaces and compatibility goal. List
excluded behavior and unknowns. Record evidence authority, licenses and collection
method privately. A dependency range is not a resolved reference version.

Use five roles for each reconstruction. Each has different input privileges:

| Role | Inputs | Outputs | Denied transfer |
| --- | --- | --- | --- |
| Observer | Authorized docs, reference execution, optional source analysis | Classified private observations | Direct implementation instructions |
| Specification writer | Private observations | Candidate behavioral contract | Source fragments, internal design, copied tests |
| Firewall reviewer | Candidate contract and provenance | Digest-bound approval or rejection | Unreviewed content reaching implementer |
| Implementer | Sealed contract and handoff guidance | Original candidate code, own design record | Reference access, prior context, analyst sessions |
| Conformance reviewer | Reference/candidate adapters and original cases | Results, failures, coverage gaps | Raw reference artifacts as repair hints |

The coordinator may be source-exposed. It must not implement the candidate itself
after seeing reference material. Agent names and fork isolation alone do not limit
files, subprocesses, network, package caches, search or memory access.

## Move artifacts through review

Private observations contain `id`, classified kind, summary, confidence and origin
locator/digest/license. The public contract contains only target interfaces,
behavioral requirements, opaque evidence IDs, acceptance IDs, exclusions and unknowns.
No source locator, transcript or evidence prose is automatically copied into it.

Each requirement must cite registered evidence. Observed claims cannot cite
uncertain observations. Inferred requirements retain that label. The reviewer
checks public identifiers, externally visible errors, fixtures and constants for
necessity and provenance. The automatic screen catches only obvious patterns.

Approval is bound to a canonical JSON SHA-256 digest. Handoff files have byte hashes
in a manifest. One run has one handoff. Changes after handoff create a new run,
new review, new seal and fresh implementation context; they do not overwrite history.

## Execute and compare

The offline implementation sandbox exposes sealed files read-only and candidate
files read/write. It excludes reference directories, host home, credentials and
network. Runtime directories are trusted mounts; reference software installed there
needs a different VM image. Never fall back silently when sandbox creation fails.

The conformance controller uses independent adapters that consume one JSON value
and return one JSON value. Case sequences model state inside one invocation. Errors,
bytes, timing and nondeterminism require explicit representations in adapters.
Candidate and case hashes tie results to a bounded snapshot. Coverage is per
requirement and acceptance case, not a broad claim of complete equivalence.

Mismatch repair uses an opaque case/requirement identifier and a newly reviewed
behavioral clarification. Keep raw traces reviewer-side. Broad redesign is the
implementer's own decision; never relay the reference algorithm as a fix.

## Preserve provenance

`.ir/objects/` stores canonical content-addressed records. `.ir/audit.jsonl` records
mutations with sequence and previous-event hash. `.ir/policy.json` is bound to the
recorded policy. File locking serializes runtime operations. Partial operations
retain work and fail integrity checks when their snapshots no longer match.

`.ir/hook-events.jsonl` is a separate observational ledger. Runtime audit does not
claim it has a cryptographic trust anchor. Keep both under private ownership.

Role sessions record provider/model/context/exposure and artifact hashes. The tool
does not authenticate the person, inspect opaque model training data, or prove that
an attested fresh session had no other input. Contamination quarantines a run;
recovery copies only independently reviewed unaffected observations into a new run.

## Keep claims distinct

Technical behavior, provenance process, security isolation, ownership and licensing
are separate questions. Public reports describe measured cases and unknowns.
Low similarity, changed language, isolated agents and passing tests are never
converted into an automatic licensing or copyright verdict.
