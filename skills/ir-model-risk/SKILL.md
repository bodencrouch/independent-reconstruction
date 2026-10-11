---
name: ir-model-risk
description: Records model training uncertainty, retrieval exposure, provider handling, and tool-mediated contamination risks. Use explicitly when planning model separation or assessing a reconstruction provenance claim.
disable-model-invocation: true
---
# Assess model exposure

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Record collector and implementer provider/model identifiers, versions when known, invocation mode, prompts, contexts, tools, and supplied artifacts. Submit role/context/exposure/model metadata with `session`.
2. Identify whether the target may be in training data, memory, retrieval indexes, repository search, shared sessions, or tool responses. Record uncertainty rather than assuming absence.
3. Inspect available provider documentation or local configuration when the task requires current facts. Use authoritative sources; do not guess retention or training policies.
4. Keep private inputs local unless remote processing is already authorized. Minimize permitted remote payloads to the role's approved artifacts.
5. Prefer fresh conversations, role-specific tools, separate workspaces, and enforced filesystem/network boundaries. Different model providers can reduce shared context but do not prove independent training histories.
6. Record source exposure or suspicious recall as an incident when warranted. Route behavioral questions through approved observation and review, never target-source retrieval in the implementation lane.
7. State what controls exist and what remains unknowable. Do not use a model name, low overlap score, or a promise to forget as certification.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" session "$RUN" --record "$SESSION_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" incident "$RUN" --record "$INCIDENT_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" audit "$RUN"
```

## Return

Return provider/model record, known context/tool exposures, remote handling basis, implemented restrictions, training uncertainty, incidents, and the supported provenance claim.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
