# Recover from contamination: reference

## Recognize exposure

Examples include an implementer receiving original source, a copied test, a source-aware parent conversation, a private stack trace, an internal algorithm summary, a search snippet, shared memory, or a poisoned tool response. Accidental access is still an exposure event.

## Preserve the record

Record identity, time, channel, content category, artifact digests, scope of access, detection method, and action taken. Store any sensitive detail in the restricted record. A summary can use opaque IDs and categories.

Deleting a local copy or asking an agent to forget does not erase knowledge. Rewriting code after exposure cannot justify a claim that the same participant never saw the source.

## Trace dependencies

A contaminated specification may affect handoff packs, cached summaries, feedback, cases, candidate modules, reports, and agents that inherited context. Reuse requires an explicit decision and accurate exposure label. Artifact hashing helps trace dependency, but it does not identify every semantic influence.

## Recovery choices

An exposed lane may continue when source reuse is authorized and its applicable obligations are addressed. A separate clean-room lane requires a fresh participant, independently reviewed behavior-only pack, and genuine restrictions on evidence access. Keep both histories.

## Example

A validator posts a private function's stack trace into the implementation conversation. Preserve the trace privately, record the event, quarantine the lane, and extract a behavior-only counterexample through review. A fresh implementer can start from the revised approved pack; the original lane remains labeled exposed.

## Use the incident schema

`schemas/incident.schema.json` records `kind`, `summary`, `affected_roles`, `evidence_ids`, `containment`, and `recovery`. Keep restricted source content outside the summary and refer to opaque evidence IDs. Describe actions already taken separately from a recovery plan; an unexecuted plan is not a receipt.
