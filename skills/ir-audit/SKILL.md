---
name: ir-audit
description: Audits run provenance, hashes, approvals, exposure, cache validity, and bounded evidence claims. Use explicitly before handoff, integration, resumption, or release reporting.
disable-model-invocation: true
---
# Audit the reconstruction record

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Read the run metadata and ledger under the authorized auditor role. Confirm pinned target/version and candidate artifacts; preserve existing evidence.
2. Run `audit`. Inspect ledger integrity, event ordering, artifact digests, current approvals, handoff references, incidents, and result validity.
3. Reconcile every handed-off requirement with its review and evidence record. Require a reviewer session whose context and exposure match the review, an approval bound to each executed corpus digest, and a registered fresh implementer context before validation. Check that observed, documented, and inferred claims remain distinguishable.
4. Review actual participant exposure, contexts, tools, workspace access, sandbox receipts, network channels, and remote model uploads. Check that collector/author, reviewer, and implementer contexts are distinct. A declared context or boundary is self-attested and does not prove an enforced one.
5. Check cached artifacts against target version, model/prompt/tool versions, input digests, review digest, and environment. Mark unsupported cache provenance or stale results explicitly.
6. Record omissions, conflicts, tamper possibilities, unresolved incidents, and scope-limited acceptance. A local hash chain supports internal consistency; it does not independently authenticate its author or timestamp.
7. Produce an audit finding record and the smallest appropriate next action. Keep private source locations and raw traces out of public reports.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" audit "$RUN"
python3 "$PLUGIN_ROOT/scripts/ir.py" report "$RUN"
```

## Return

Return audit status, exact artifact digests, valid/invalid approvals and results, exposure/isolation level, coverage gaps, cache decisions, integrity limitations, and required corrections.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
