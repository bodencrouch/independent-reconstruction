# Claude Code

The project installer merges `.claude/settings.json`, installs the Claude adapter, and copies skills, commands, agents, and converted rules. The project template uses `CLAUDE_PROJECT_DIR`; the native plugin hook template uses `CLAUDE_PLUGIN_ROOT`.

The adapter follows [Claude Code's official hook protocol](https://code.claude.com/docs/en/hooks). PreToolUse gates all tools, including Agent/Task/Workflow delegation, shell execution, network retrieval, MCP calls, and structured file access. UserPromptSubmit enforces exact prompt approval for implementer sessions. Allowed calls return an empty JSON object so the host's normal permission rules still apply. Denied calls return the event-specific decision and exit 2.

Failure blocking in the template uses `onFailure: "block"`, which requires Claude Code 2.1.295 or later. Older hosts may fail open when the interpreter, imports, script, timeout, or output parsing fails. Check the installed version and real hook activation before relying on the gate. A successful direct adapter invocation alone does not prove host loading or version compatibility.

SubagentStart is observational in Claude Code and cannot block creation. The actual delegation gate belongs in PreToolUse. Agents spawned by another interface, host-provided context, resumed sessions, automatic instruction loading, shared memories, and transcript files still need independent isolation review. Start implementing in a fresh external process with only the approved pack available.
