"""Translate host payloads and decisions without sharing protocol schemas."""
from pathlib import Path
from .policy import Decision

CURSOR_GATES = {"preToolUse", "beforeShellExecution", "beforeMCPExecution", "beforeReadFile", "beforeTabFileRead", "beforeSubmitPrompt", "subagentStart"}
CLAUDE_GATES = {"PreToolUse", "UserPromptSubmit"}
CURSOR_EVENTS = CURSOR_GATES | {"sessionStart", "sessionEnd", "postToolUse", "postToolUseFailure", "afterFileEdit", "afterTabFileEdit", "afterShellExecution", "afterMCPExecution", "subagentStop", "preCompact", "stop"}
CLAUDE_EVENTS = CLAUDE_GATES | {"SessionStart", "SessionEnd", "PostToolUse", "PostToolUseFailure", "SubagentStart", "SubagentStop", "PreCompact", "Stop"}
CODEX_GATES = {"PreToolUse", "UserPromptSubmit"}
CODEX_EVENTS = CODEX_GATES | {"SessionStart", "SessionEnd", "PostToolUse", "SubagentStart", "SubagentStop", "PreCompact", "PostCompact", "Stop", "Interrupt"}


def patch_paths(inputs):
    """Extract every mutation path from the documented apply_patch envelope."""
    command = inputs.get("command") if isinstance(inputs, dict) else inputs
    if not isinstance(command, str):
        raise ValueError("Patch tool must expose its documented command envelope.")
    lines = command.splitlines()
    if len(lines) < 3 or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch":
        raise ValueError("Patch envelope is invalid.")
    paths = []
    headers = ("*** Add File: ", "*** Update File: ", "*** Delete File: ", "*** Move to: ")
    for line in lines[1:-1]:
        header = next((prefix for prefix in headers if line.startswith(prefix)), None)
        if header:
            paths.append(line[len(header):])
        elif line.startswith("*** ") and line != "*** End of File":
            raise ValueError("Patch metadata is unsupported.")
    if not paths:
        raise ValueError("Patch contains no supported mutation paths.")
    return {"paths": paths}


def tool_operation(tool: str) -> str:
    value = tool.lower()
    if value.startswith(("mcp:", "mcp__")) or value == "mcp":
        return "mcp"
    if value in {"bash", "powershell", "shell", "terminal", "exec_command", "computer", "browser"}:
        return "shell"
    if value in {"agent", "task", "workflow", "spawn_agent", "sendmessage", "teamcreate"}:
        return "delegate"
    if value in {"webfetch", "websearch", "fetch", "search_web"}:
        return "network"
    if value in {"read", "read_file", "tabread"}:
        return "read"
    if value in {"write", "edit", "delete", "notebookedit", "write_file", "tabwrite"}:
        return "write"
    if value in {"glob", "grep", "list_directory"}:
        return "search"
    if value in {"todowrite", "taskcreate", "taskupdate", "tasklist", "taskget", "askuserquestion", "exitplanmode", "enterplanmode", "update_plan"}:
        return "control"
    return "unknown"


def normalize(host: str, event: str, data: dict):
    tool = data.get("tool_name", "")
    if not isinstance(tool, str):
        raise ValueError("Invalid tool descriptor.")
    if event in {"preToolUse", "PreToolUse"}:
        inputs = data.get("tool_input", {})
        operation = tool_operation(tool)
        if host == "codex" and tool == "apply_patch":
            inputs, operation = patch_paths(inputs), "write"
    elif event == "beforeShellExecution":
        operation, inputs = "shell", data
    elif event == "beforeMCPExecution":
        operation, inputs = "mcp", data
    elif event in {"beforeReadFile", "beforeTabFileRead"}:
        operation, inputs = "read", data
    elif event in {"beforeSubmitPrompt", "UserPromptSubmit"}:
        operation, inputs = "prompt", data
    elif event == "subagentStart":
        operation, inputs = "delegate", data
    else:
        # Claude's SubagentStart cannot prevent an inherited context. It is
        # observational; PreToolUse gates the initiating Agent/Task call.
        operation, inputs = "observe", data
    if not isinstance(inputs, dict):
        # MCP tool_input can be a JSON string, but it is denied before parsing
        # in the implementer role; never treat it as structured file access.
        if operation == "mcp":
            inputs = {}
        else:
            raise ValueError("Invalid structured tool input.")
    cwd_value = data.get("cwd")
    if cwd_value is None:
        roots = data.get("workspace_roots")
        cwd_value = roots[0] if isinstance(roots, list) and len(roots) == 1 else None
    cwd = Path(cwd_value).resolve() if isinstance(cwd_value, str) and Path(cwd_value).is_absolute() else Path.cwd().resolve()
    return operation, tool, inputs, cwd


def output(host: str, event: str, decision: Decision, active=False):
    message = decision.message
    if host == "cursor":
        if event == "beforeSubmitPrompt":
            out = {"continue": decision.allow}
            if message:
                out["user_message"] = message
            return out
        if event in CURSOR_GATES:
            out = {"permission": "allow" if decision.allow else "deny"}
            if message and event != "beforeTabFileRead":
                out["user_message"] = message
            if message and event in {"preToolUse", "beforeShellExecution", "beforeMCPExecution"}:
                out["agent_message"] = message
            return out
        if event == "sessionStart" and active:
            return {"additional_context": "Independent Reconstruction role policy is active. Hooks are procedural controls; use a sealed handoff and OS isolation for an implementer session."}
        if not decision.allow and event in {"postToolUse", "postToolUseFailure"}:
            return {"additional_context": message}
        return {}
    if event == "PreToolUse" and not decision.allow:
        return {"hookSpecificOutput": {"hookEventName": event, "permissionDecision": "deny", "permissionDecisionReason": message}}
    if event == "UserPromptSubmit" and not decision.allow:
        if host == "codex":
            return {"decision": "block", "reason": message}
        return {"decision": "block", "reason": message, "hookSpecificOutput": {"hookEventName": event, "suppressOriginalPrompt": True}}
    if event in {"SessionStart", "SubagentStart"} and active:
        context = message or "Independent Reconstruction role policy is active. Hooks do not certify a fresh context or provide an OS sandbox."
        return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": context}}
    if not decision.allow and event in {"PostToolUse", "PostToolUseFailure"}:
        return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": message}}
    # Claude allow is deliberately silent: normal host permission checks still
    # apply. Returning permissionDecision=allow could bypass those checks.
    return {}
