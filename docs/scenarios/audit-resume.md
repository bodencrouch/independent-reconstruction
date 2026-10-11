# Audit, caching, and resume

Use this scenario when continuing an interrupted run, reconciling durable handoffs, changing environment/model/configuration, evaluating caches, or preparing release claims. Preserve all existing work and unrelated configuration.

## Read state before acting

```text
python3 scripts/ir.py status RUN
python3 scripts/ir.py audit RUN
python3 scripts/ir.py resume RUN
```

`resume` verifies recorded integrity and the existing sealed handoff. It does not call a provider, regenerate implementation, run conformance cases, or change a sealed contract. Follow-up actions need their own authorization and gate.

Reconcile recorded state with actual files and current execution context. A ledger phase, timed-out worker, or READY_TO_COMMIT status does not establish an application is complete. An unavailable file must be reported; do not fabricate a replacement receipt or repeatedly poll a missing temporary handoff.

## Audit inventory

| Binding | Reconcile |
| --- | --- |
| Input identity | Original version/digest, authorized input set, license/provenance class |
| Environment | OS/architecture/runtime/dependencies/configuration, clock/seed/locale |
| Evidence | Every opaque ID resolves privately; confidence and lineage preserved |
| Specification | Canonical hash, requirements, exclusions, unknowns, acceptance IDs |
| Review | Exact candidate digest, registered firewall-reviewer context/exposure, real semantic review, identity limitations |
| Corpus review | Exact specification/case digests, semantic findings, case provenance, registered reviewer, limits |
| Handoff | Manifest, approved files, separate destination, trusted receipt binding |
| Implementation | Fresh context, actual access controls, candidate files/dependencies |
| Validation | Case/adapter/candidate/version bindings, coverage, execution failures |
| Incidents | Quarantine status, dependent invalidated artifacts, recovery lineage |
| Release | Distributable inventory, private-material exclusion, notices, claims |

The runtime's digest/chain checks detect recorded inconsistency under their assumptions. They do not authenticate reviewer identity, verify every exposure declaration, prove an adapter faithful, establish training-data isolation, or prevent an owner from rewriting all storage. Record external trusted anchors when available and state their limits.

## Cache policy

Cache reuse requires matching original/input digest, evidence lineage, contract revision, firewall decision, model/configuration where relevant, toolchain/environment, and intended access lane. Content addressing helps bind bytes; it does not make cached content appropriate for another role.

Never reuse original-source caches, upstream fixtures, private analysis summaries, or tainted candidate code in an implementation lane. Never count old conformance results against a changed candidate, comparator, case corpus, or environment without an explicit justified binding. Case/input/tolerance changes require a new digest-bound corpus review before executing adapters; raw corpus remains reviewer-side.

The current runtime offers content-addressed private storage and verification, not automatic provider-response caching or a cross-run dependency rebuild engine. Describe manual reuse honestly rather than promising unsupported automation.

## Resume choice

Continue already authorized clean work after verification. Do not ask a redundant proceed question for routine orientation. Preserve independent gates for destructive edits, credential changes, external publication, and third-party PR creation.

Use a fresh run when the sealed contract changes, an incident quarantines progression, or source/environment bindings no longer support the old run. Keep the predecessor privately and record lineage; do not mutate its manifest or rewrite its history. A fresh implementer context must receive only the reapproved handoff.

Return verified state, changed bindings, safe next task, invalidated receipts, missing records, and unresolved uncertainty.
