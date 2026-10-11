# Cursor

The project installer writes `.cursor/hooks.json` and `.cursor/hooks/independent-reconstruction/`, and copies skills, commands, agents, and rules. The provided template follows [Cursor's official hook protocol](https://cursor.com/docs/hooks). Gate entries set `failClosed: true`; adapters also return deny and exit 2 when an active run is invalid.

`preToolUse` covers structured file tools and denies unadapted implementer tools. Dedicated shell, MCP, read, Tab read, prompt, and subagent gates provide additional host surfaces. Event payloads are hashed for private receipts without recording their contents. Post events only observe. SessionStart can inject context but cannot block session creation; a context message is not an isolation receipt.

Start Cursor with the run and role environment, open only the dedicated role workspace, and confirm the Hooks tab/output channel shows the configured handlers. Desktop and cloud execution differ: hooks do not cover early read-only cloud exploration, and some dedicated desktop events are absent in cloud agents. Use `preToolUse` plus OS isolation and fresh context rather than assuming every hook fires in every surface. Tab edits are observed after the edit; disable Tab when it would create an uncontrolled channel.

The checked-in hooks.json is a project template. A native Cursor plugin hook file must use `CURSOR_PLUGIN_ROOT`, not the project-relative path. Do not install this template as a global hook file without adapting the paths.
