# Fresh contexts and execution isolation

Use this scenario before dispatching implementation, switching model/providers, continuing after compaction, or claiming a clean-room boundary. Context separation, artifact separation, and operating-system isolation are distinct controls.

## What a fresh context means

The implementer receives the approved handoff and independent build constraints. It receives no parent conversation, summarized history, analysis transcript, original repository, original binary/tests, raw observations, source links, original architecture description, or informal source-informed feedback.

If the host supports delegation without inherited history, select that mode explicitly. A role prompt loaded into an existing source-exposed conversation does not create a fresh implementer. A newly named agent with full-history inheritance remains exposed.

Record context/session ID, provider/model/version, role, known prior exposure, and active permissions privately. Model training exposure is generally unknown. Switching providers does not prove the new model lacks prior knowledge or training examples.

## Host access checks

| Boundary | Check before implementation |
| --- | --- |
| Filesystem | Original/private roots absent; no symlink/mount escape into excluded storage |
| Home/cache | Other transcripts, package caches, original installs, histories, credentials absent |
| Network/MCP | No source retrieval or private registry APIs; only approved channels if required |
| Tool permissions | Read/write scope matches handoff/candidate; unmanaged shell/tool paths considered |
| Parent communication | Only approved artifacts flow to implementation; no informal hints |
| Runtime libraries | Original package not hidden inside a trusted system dependency |
| Approval integrity | Handoff manifest checked against private trusted digest, not only itself |

The plugin's role files guide behavior. The host decides whether those files become selectable agents and which tool permissions apply. Installing Markdown does not itself constrain a model's filesystem or network.

## Local bubblewrap launcher

The runtime command is `python3 scripts/ir.py sandbox RUN -- COMMAND` after sealing a handoff. Inspect current implementation/capabilities before use. Its planned Linux boundary mounts the handoff read-only at `/handoff`, exposes `candidate/` writable, creates disposable home/tmp, clears environment, unshares namespaces/network, and trusts system runtime mounts such as `/usr`, `/bin`, `/lib`, and `/lib64`.

Bubblewrap availability and user-namespace permissions are host-specific. The launcher must fail closed when unavailable; do not silently fall back to ordinary host execution. A registered original/source root overlapping trusted system mounts requires a separate VM/image. Even without a registered overlap, original software inside a system runtime can remain visible; inventory trusted mounts.

The sandbox controls the launched child process. It does not isolate an already-running parent model session, its tools, or other tabs/agents. Host kernel and system runtime remain trusted. No hardware, hypervisor, or training-data isolation is claimed.

The network-disabled child cannot directly call a hosted model provider. Viable modes include an already approved local model reachable through an appropriately designed bounded interface, or an external controller that runs a fresh model context and exchanges only reviewed handoff/output artifacts. The current CLI does not implement a hosted-provider bridge, local model server, or automatic transcript filtering; do not advertise one.

## Hook limits

Project/user hooks can reject managed file reads, tool calls, inherited-context requests, or unsafe role transitions as defense in depth. Verify event schemas/load behavior for the actual host. Cursor and Claude hooks are not interchangeable, and installed Codex may not support the same events.

Hooks cannot reliably parse all shell indirection, block unmanaged clients, revoke information already in context, prevent storage-owner tampering, or isolate a shared filesystem. An allow/deny hook receipt describes that event's decision, not total confinement.

## Compaction and provider changes

Preserve only approved handoff state in implementation continuity. A compaction summary that inserts source-informed coordinator notes contaminates the implementation lane. On resume, verify stored digests, context exposure, model/configuration changes, and incidents. If the old implementation context cannot be reconstructed without excluded history, start a fresh restricted context from the reviewed handoff.

Report actual controls and gaps concretely. If only prompt/artifact boundaries are available, label that weaker mode honestly and do not claim operating-system isolation.
