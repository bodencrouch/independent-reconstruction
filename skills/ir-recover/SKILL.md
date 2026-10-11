---
name: ir-recover
description: Records accidental source exposure or boundary failure, preserves evidence, and creates an honest recovery lane. Use explicitly when restricted information reaches an implementer or an approved handoff is compromised.
disable-model-invocation: true
---
# Recover from contamination

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Stop work in the affected implementation lane. Preserve the candidate, handoff, approvals, prompts, and relevant exposure metadata; do not delete evidence to simulate independence.
2. Identify the exposed participant, content class, channel, time, affected artifact digests, known reach, and uncertainty. Avoid reproducing private source or raw text in the incident summary.
3. Submit an incident record with `incident`. Treat the existing lane as exposed until the review establishes a narrower fact-supported boundary.
4. Trace downstream specifications, prompts, cases, caches, agents, and candidate artifacts that may depend on the exposure. Invalidate affected approvals and evidence.
5. Choose an honest path: continue as an exposed/reuse-permitted implementation with its obligations, or create a separate run with a genuinely fresh participant and sanitized approved pack.
6. Re-review the replacement specification and its feedback. Use a distinct workspace, no inherited context, and appropriate tool/process restrictions for a renewed isolation claim.
7. Preserve the original lane and document recovery limits. Re-run only justified conformance work once the replacement implementation is ready and validation is authorized.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" incident "$RUN" --record "$INCIDENT_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" audit "$RUN"
```

## Return

Return incident ID, affected roles/artifacts, preserved evidence, invalidated approvals/results, selected recovery path, new run if any, and uncertainty about exposure.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
