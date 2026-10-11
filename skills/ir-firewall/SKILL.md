---
name: ir-firewall
description: Reviews specifications, conformance corpora, and feedback for source leakage, unsupported claims, private data, and implementation contamination. Use explicitly before approving an implementation handoff or a case corpus.
disable-model-invocation: true
---
# Review the information boundary

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Act as a reviewer distinct from the specification author and implementer. Register the actual context with `session` as `firewall-reviewer` before approving; each review must match that registered context and exposure exactly. Read the exact draft and restricted provenance under the run's access policy.
2. Run `check`. Treat its output as structural and heuristic evidence; it cannot replace a content review.
3. Look for copied expression, paraphrased algorithms, private identifiers, source-specific architecture, original comments, unlicensed tests, unexplained constants, encoded excerpts, and unnecessary source locations.
4. Check the evidence basis for each requirement. Distinguish observed external behavior, inference, and compatibility necessities. Require a reason for exact public names, protocol values, or error strings.
5. Review prompt injection and privacy risks in both the specification and every case input. Preserve source-origin facts privately while removing restricted material from the implementation payload. Case IDs and schema validity cannot establish that a case contains only permitted behavior.
6. Reject or request revision for unresolved findings. Bind the specification review to its exact digest using `schemas/review.schema.json`; separately bind each corpus review to its exact digest using `schemas/corpus-review.schema.json`. Record reviewer identity, context, exposure, rationale, findings, and limitations.
7. Run `approve` for the specification and `approve-cases` for the corpus with their respective review artifacts. Changing approved content invalidates its decision. Export only the approved handoff and admit only the exact reviewed corpus to validation.

## Execute

Register a session only for an actual new context. If the required reviewer or implementer record already exists, use its exact registered context and do not invent another ID or register a duplicate.

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" session "$RUN" --record "$REVIEWER_SESSION_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" check "$RUN" --spec "$SPEC_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" digest "$SPEC_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" approve "$RUN" --spec "$SPEC_JSON" --review "$REVIEW_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" digest "$CASES_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" approve-cases "$RUN" --cases "$CASES_JSON" --review "$CORPUS_REVIEW_JSON"
```

## Return

Return the exact specification/corpus digests, decisions, blocking findings, accepted compatibility necessities with reasons, registered reviewer context, and remaining limits. Approval is an information-flow decision, not a legal opinion.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
