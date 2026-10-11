---
name: ir-release
description: Builds a release evidence packet that separates compatibility, process provenance, isolation, and unresolved distribution questions. Use explicitly before sharing or publishing a reconstruction candidate.
disable-model-invocation: true
---
# Prepare release evidence

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Confirm the release scope and existing user authorization. Preserve the exact candidate, approved contract, run ledger, and private origin/exposure record.
2. Run `audit` and `report`. Confirm matching reviewer sessions, exact specification and corpus approvals, and the fresh implementer session used for validation. Resolve blocking record inconsistencies; do not hide incidents, unsupported behavior, or failed checks.
3. Inventory distributable candidate files, own dependencies, notices, generated artifacts, and selected reports. Exclude private evidence from the public pack while retaining its provenance privately.
4. Document tested versions/platforms, approved corpus digest and requirement coverage, oracle/candidate commands, normalization, known gaps, declared participant contexts, actual isolation, and model training uncertainty. Context registration is self-attested; external model identity and history may remain unknown.
5. Write bounded claims. Say what was measured and how the work was authored; do not assert source was unseen by participants who saw it or infer legal freedom from test/similarity results.
6. Distinguish technical release readiness from unresolved license, notice, contractual, trademark, or other distribution questions. Do not automatically choose a license or remove inherited notices.
7. Prepare a local reviewable release packet. Publish only within explicit authorization and honor the current-conversation approval gate for public upstream pull requests.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" audit "$RUN"
python3 "$PLUGIN_ROOT/scripts/ir.py" report "$RUN"
python3 "$PLUGIN_ROOT/scripts/ir.py" packet "$RUN" --dest "$PACKET_JSON"
```

## Return

Return local release packet location, included artifacts/digests, measured compatibility, process/isolation claims, private evidence retained, unresolved distribution items, and publication status.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
