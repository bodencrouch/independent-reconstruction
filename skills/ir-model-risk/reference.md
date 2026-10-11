# Assess model exposure: reference

## Separate risk channels

Training exposure predates the run. Prompt exposure comes from current context and artifacts. Retrieval exposure comes from tools, indexes, browsing, and memory. Workspace exposure comes from unrestricted processes and files. These channels need different controls.

Opaque training history cannot be repaired by a fresh conversation. Record that limitation and avoid claiming absence. A model can produce a familiar implementation independently of the current source channel; suspicious resemblance still requires review.

## Record provider handling

Capture only documented or configured facts about remote inference, retention, logging, training use, regional processing, and account settings. Policies can change. Verify them when they matter to the user's task, and separate a provider statement from locally observed behavior.

## Controls

- Minimal approved prompts and artifact set.
- Fresh context with no parent history.
- No unrestricted target-source search or shared retrieval memory.
- Role-specific tool access and workspace isolation.
- Network restriction where required and actually enforced.
- Artifact and prompt digests plus exposure records.

These controls improve an inspectable process. They do not establish the complete origin of all model output.

## Example

The implementer uses a fresh context and has no target repository access, but its model training corpus is unavailable. Report those facts separately. If a tool response includes original source, preserve an incident record and recover the lane; changing providers alone is insufficient.

## Register each actual session

`schemas/session.schema.json` requires `role`, `provider`, `model`, `context_id`, `exposure`, `artifacts` (actual SHA-256 digests), and `training_history`. Exposure is `source-exposed`, `review-only`, `sealed-spec-only`, or `unknown`. Roles include `observer`, `spec-writer`, `firewall-reviewer`, `implementer`, `conformance-reviewer`, `coordinator`, `provenance-auditor`, `contamination-responder`, and `release-reviewer`. Use the real model/context data available; unknown training history must be stated as unknown.

An implementer session with known source exposure cannot honestly be declared `sealed-spec-only`. A provider outside the sandbox receives only an approved sanitized packet, and this does not prove its training corpus or confine its other tools.
