# Host integrations

This directory contains distinct adapters for Cursor, Claude Code, and Codex. The hook protocols are host-specific. The shared Python policy performs the same procedural checks while each adapter emits its host's JSON schema.

Install into an existing project after choosing a host:

```bash
python3 scripts/install.py --project /absolute/project --host cursor --dry-run
python3 scripts/install.py --project /absolute/project --host cursor
```

Use `--host claude`, `--host codex`, repeat `--host`, or choose `--host all`. The installer prepares a project snapshot, links discovered skills to that snapshot, copies relevant host assets, merges hook arrays, and retains unrelated settings. Resolve a skill's real path to locate its package resources. A destination that differs from the package causes a collision before mutations begin. Existing settings receive exact, owner-private backups named by their content digest. A repeated unchanged install preserves settings bytes and produces aggregate counters. Backups are local configuration data and must not enter a public release.

The installer does not edit the project's AGENTS.md. Read `.agents/independent-reconstruction.md` from the installed project to locate the package snapshot. Skills use the shared runtime from that snapshot. Native plugin installation is also possible where the host supports it; project hook templates and native plugin hook templates use different path variables.

Installation does not prove that a host loaded the plugin. Restart or reload the host, review and trust hooks where required, confirm discovery, trigger a supported event in a controlled run, and inspect its hook output. Retain the resulting receipt separately from behavioral conformance evidence.

## Activation and limits

Hooks are passive unless the host process inherits `IR_RUN` or `IR_ROLE`. A small POSIX shell bootstrap emits neutral host JSON before loading Python when neither is present, so an inactive project does not depend on Python imports or private policy. It stores no event. Active adapters use Python 3.11 or later. Set both to enter a role session:

```bash
export IR_RUN=/absolute/private/run
export IR_ROLE=implementer
```

The canonical roles are `observer`, `spec-writer`, `firewall-reviewer`, `implementer`, `conformance-reviewer`, `coordinator`, `provenance-auditor`, `contamination-responder`, and `release-reviewer`. Legacy hook aliases `analyst`, `firewall`, `verifier`, and `auditor` map to their corresponding canonical roles; new sessions use canonical names. Partial activation or an invalid run policy denies actions on blocking events. Other roles currently receive procedural audit receipts; the implementer receives access gates. Role environment variables and writable policy files can be changed by the same user and do not establish an adversarial security boundary. Policy, manifest, and event JSON reject duplicate keys, and schema versions require integers.

An implementer needs an approved `IR_RUN/.ir/policy.json`, a manifest seal, and every manifest-covered file intact. File tools may read the sealed pack and candidate and write only the candidate. Symlink escapes are resolved before checking paths. Original source roots and private run metadata are excluded. Unknown tools, arbitrary shell execution, network retrieval, MCP calls, and nested agents are denied. Builds run through the package's OS sandbox from a separate coordinator session. A structured tool gate cannot detect every expression copied into a file or every indirect tool effect.

The handoff workflow approves the fixed initial launch instruction by exact UTF-8 SHA-256 in `roles.implementer.permitted_prompt_sha256`. The role packet returns that same instruction; use it without edits in a fresh implementing session. With no approved digest, submission events deny implementer prompts. Additional instructions or changed requirements require a newly reviewed handoff/run and a fresh role session. Do not manually add prompt hashes or edit sealed policy: the run audit records its digest, and such edits invalidate that evidence. Do not reuse source-exposed host conversations, transcripts, caches, memories, credentials, or parent contexts. Host hooks cannot erase prior exposure or opaque model training history.

The hook receipt file is `.ir/hook-events.jsonl`, with mode 0600 inside owner-only `.ir`. Records contain a timestamp, host, event, role, payload digest, decision, and reason code. They contain no payload text, filenames, prompts, tool results, reasoning, or credentials. Digests are identifiers and may still correlate predictable inputs; keep the ledger private. Host transcript and debug facilities have their own storage behavior and require a separate review.

Observational events cannot undo a completed read, edit, tool call, or context inheritance. This package does not follow up automatically at Stop, SubagentStop, or compaction, so a failed audit does not create an unbounded agent loop. Hook receipts, OS sandbox receipts, conformance reports, and provenance review support distinct claims; none is a legal verdict.

## Lifecycle

Use a fresh project snapshot for an upgrade when managed assets differ. The installer deliberately refuses to overwrite those assets. Merged configuration backups can be restored manually after reviewing changes made since installation. To remove the integration, remove only hook entries whose command references `hooks/independent-reconstruction`, then remove the package-owned assets once consumers no longer need them. Preserve other hook entries and newer settings changes. Personal installations require a separate explicit operation; this installer never writes into the user's host configuration directories.
