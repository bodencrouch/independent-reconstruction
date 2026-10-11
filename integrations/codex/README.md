# Codex

The project installer links skills into `.agents/skills`, copies the complete package into `.independent-reconstruction/package`, and merges native hooks into `.codex/hooks.json`. It provides `.agents/independent-reconstruction.md` as an instruction fragment. The package's `agents/` directory contains portable role prompts to pass to a fresh role session; the installer preserves existing AGENTS.md and config.toml.

The adapter follows [OpenAI's native hook protocol](https://learn.chatgpt.com/docs/hooks). The native plugin template uses `PLUGIN_ROOT`, and the project installer substitutes a quoted absolute script location so launching from a project subdirectory works. Codex hooks have their own schema; `.cursor/hooks.json` is not a Codex configuration. See [OpenAI's plugin packaging reference](https://developers.openai.com/plugins/build/plugins) for plugin hook discovery.

Use `/hooks` in the host to review and trust these exact hook definitions. Codex skips untrusted new or changed hooks, and project configuration must also be trusted. Installation or successful direct adapter execution does not prove that the current host version loaded and activated them. This installer does not bypass host trust.

PreToolUse gates shell, MCP, unknown local tools, and Agent/spawn_agent delegation. The apply_patch adapter extracts every mutation path, including move source and destination, and permits only candidate writes. Structured read adapters allow the sealed pack and generated candidate. UserPromptSubmit enforces exact approved prompt digests for implementers. Allowed calls emit empty JSON so normal host permission rules continue; denied calls emit the documented event-specific decision and exit 2.

Hosted WebSearch tools do not pass through local tool hooks. Specialized tool paths can opt out, and write_stdin sends input to previously approved unified-exec sessions without another PreToolUse gate. Hook failures can also let execution continue. Start with no inherited exec sessions, disable unconfined retrieval channels, and enforce filesystem/network limits outside the host. Treat the sandbox as the actual access boundary.

An implementing subagent must receive no inherited source analysis. Where a runtime offers `fork_turns: "none"`, use it, while recognizing that an empty conversational fork still shares filesystem and tool access. Use a fresh external process and the sealed pack with a restricted environment. SubagentStart is observational and cannot stop creation; delegation is denied at PreToolUse when that path is covered.

Use scripts/ir.py for workflow state and sandboxed local commands. Native registration, hook activation, tool execution, hosted inference, provider credentials, OS isolation, and conformance support distinct receipts. A role prompt on disk is not evidence that the runtime registered that name as a custom native agent type.
