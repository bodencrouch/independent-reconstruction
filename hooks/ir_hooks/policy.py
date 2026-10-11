"""Conservative procedural gates. OS isolation remains the security boundary."""
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
from .context import Context, beneath


@dataclass(frozen=True)
class Decision:
    allow: bool
    code: str
    message: str = ""


def deny(code, message):
    return Decision(False, code, message)


def resolve_path(value, cwd: Path) -> Path | None:
    if not isinstance(value, str) or not value or "\0" in value:
        return None
    path = Path(value)
    # Tilde and variable expansion belong to shells, not structured file APIs.
    if "~" in value or "$" in value:
        return None
    return (path if path.is_absolute() else cwd / path).resolve()


def check_paths(ctx: Context, inputs: dict, cwd: Path, write=False, search=False):
    if search:
        value = inputs.get("glob")
        if isinstance(value, str) and (value.startswith(("/", "~")) or ".." in value or "$" in value):
            return deny("search_escape", "Search patterns must stay relative to the permitted workspace.")
    values = []
    for key in ("file_path", "path", "notebook_path", "target_file", "relative_workspace_path"):
        if key in inputs:
            values.append(inputs[key])
    if "paths" in inputs:
        if not isinstance(inputs["paths"], list):
            return deny("invalid_path", "File access needs explicit structured paths.")
        values.extend(inputs["paths"])
    attachments = inputs.get("attachments", [])
    if not isinstance(attachments, list):
        return deny("invalid_attachment", "Attachments need explicit structured paths.")
    for attachment in attachments:
        if not isinstance(attachment, dict) or "file_path" not in attachment:
            return deny("invalid_attachment", "Attachments need explicit structured paths.")
        values.append(attachment["file_path"])
    if not values:
        if search:
            values.append(str(cwd))
        else:
            return deny("missing_path", "This file tool does not expose a supported structured path.")
    for value in values:
        path = resolve_path(value, cwd)
        if path is None:
            return deny("invalid_path", "File access needs an unambiguous structured path.")
        if any(beneath(path, src) for src in ctx.source_roots):
            return deny("restricted_source", "Implementers may only read the sealed specification and their candidate.")
        roots = ctx.write_roots if write else ctx.read_roots + ctx.write_roots
        if not any(beneath(path, root) for root in roots):
            return deny("outside_workspace", "File access exceeds this role's allowed workspace.")
        if search and path.is_dir():
            seen = 0
            for directory, directories, files in os.walk(path, followlinks=False):
                for name in directories + files:
                    seen += 1
                    if seen > 10000:
                        return deny("search_budget", "Search exceeds the hook's bounded inventory; run it through the sandbox.")
                    entry = Path(directory) / name
                    if entry.is_symlink():
                        destination = entry.resolve()
                        if not any(beneath(destination, root) for root in roots):
                            return deny("search_symlink_escape", "Search contains a symlink beyond the permitted workspace.")
    return Decision(True, "workspace_path")


def evaluate(ctx: Context, operation: str, tool: str, inputs: dict, cwd: Path) -> Decision:
    if ctx.role != "implementer":
        return Decision(True, "procedural_role")
    if operation == "observe":
        return Decision(True, "observation_only")
    if operation in {"shell", "network", "mcp"}:
        return deny("unconfined_execution", "Arbitrary execution or external retrieval is disabled in implementer hooks. Run builds through the isolated sandbox from a separate coordinator session.")
    if operation == "delegate":
        return deny("context_inheritance", "Nested agents can inherit exposed context. Start a fresh role session using only the sealed handoff.")
    if operation == "prompt":
        # Heuristic source detection cannot establish a clean prompt. Permit
        # only the fixed launch instruction sealed by the handoff workflow.
        # Changed requirements need a new reviewed handoff and fresh session.
        prompt = inputs.get("prompt")
        hashes = ctx.policy["roles"]["implementer"].get("permitted_prompt_sha256", [])
        if not isinstance(hashes, list) or not isinstance(prompt, str):
            return deny("unapproved_prompt", "This implementer prompt has not been approved by the firewall.")
        if hashlib.sha256(prompt.encode()).hexdigest() not in hashes:
            return deny("unapproved_prompt", "Additional implementer instructions require a reviewed amended handoff and a fresh role session.")
        if inputs.get("attachments"):
            return check_paths(ctx, inputs, cwd)
        return Decision(True, "approved_prompt")
    if operation == "read":
        return check_paths(ctx, inputs, cwd)
    if operation == "write":
        return check_paths(ctx, inputs, cwd, write=True)
    if operation == "search":
        pattern = inputs.get("pattern")
        if tool.lower() == "glob" and isinstance(pattern, str) and (pattern.startswith(("/", "~")) or ".." in pattern or "$" in pattern):
            return deny("search_escape", "Glob patterns must stay relative to the permitted workspace.")
        return check_paths(ctx, inputs, cwd, search=True)
    if operation == "control":
        return Decision(True, "control_only")
    return deny("unknown_tool", "This implementer tool has no information-flow adapter. Use supported structured file tools or the isolated sandbox.")
