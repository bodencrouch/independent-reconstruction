#!/usr/bin/env python3
"""Opt-in project installation with collision checks and private config backups."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import shlex
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".ir", ".venv", "__pycache__", "node_modules", "target", "dist", ".independent-reconstruction", "private", "runs", "handoffs", "candidate", "exports"}
PACKAGE_DIRS = {"ir", "scripts", "schemas", "examples", "docs", "skills", "agents", "commands", "rules", "hooks", "integrations", ".codex-plugin", ".cursor-plugin", ".claude-plugin"}
PACKAGE_FILES = {"AGENTS.md", "README.md", "LICENSE", "LICENSE.txt", ".gitignore", "plugin.json"}


class InstallError(Exception):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def safe_parent(path: Path, project: Path):
    if path == project or project not in path.parents:
        raise InstallError("Installation path exceeds the chosen project.")
    for part in [path] + list(path.parents):
        if part == project:
            break
        if part.is_symlink():
            raise InstallError("An installation destination contains a symlink; review it before installing.")
        if part.exists() and part != path and not part.is_dir():
            raise InstallError("An installation parent is not a directory.")


def source_files():
    for directory, names, files in os.walk(PACKAGE, followlinks=False):
        names[:] = sorted(name for name in names if name not in EXCLUDED)
        if Path(directory) == PACKAGE:
            names[:] = [name for name in names if name in PACKAGE_DIRS]
            files = [name for name in files if name in PACKAGE_FILES]
        if any((Path(directory) / name).is_symlink() for name in names):
            raise InstallError("Package contains a directory symlink; provide a reviewed regular-file package.")
        for name in sorted(files):
            source = Path(directory) / name
            if source.is_symlink():
                raise InstallError("Package contains a symlink; provide a reviewed regular-file package.")
            yield source.relative_to(PACKAGE), source


def merge_hooks(existing, incoming, cursor=False):
    if not isinstance(existing, dict):
        raise InstallError("Existing host settings must be a JSON object.")
    merged = dict(existing)
    if cursor:
        if merged.get("version", 1) != 1:
            raise InstallError("Existing Cursor hook schema is unsupported.")
        merged["version"] = 1
    hooks = merged.get("hooks", {})
    if not isinstance(hooks, dict):
        raise InstallError("Existing hooks must be a JSON object.")
    hooks = dict(hooks)
    for event, additions in incoming["hooks"].items():
        entries = hooks.get(event, [])
        if not isinstance(entries, list):
            raise InstallError("Existing hook event must contain an array.")
        entries = list(entries)
        for item in additions:
            if item not in entries:
                entries.append(item)
        hooks[event] = entries
    merged["hooks"] = hooks
    return merged


def claude_rule(raw):
    # Cursor's alwaysApply/globs schema does not belong in Claude rules. These
    # project rules deliberately apply throughout this opt-in project.
    text = raw.decode("utf-8")
    if text.startswith("---\n"):
        marker = text.find("\n---\n", 4)
        if marker < 0:
            raise InstallError("Rule frontmatter is incomplete.")
        text = text[marker + 5:].lstrip("\n")
    return text.encode("utf-8")


class Plan:
    def __init__(self, project):
        self.project = project
        self.files = {}
        self.links = {}
        self.configs = {}
        self.unchanged = 0

    def add(self, relative, raw, mode=0o644):
        path = self.project / relative
        safe_parent(path, self.project)
        if path.exists():
            if not path.is_file() or path.read_bytes() != raw:
                raise InstallError("A destination file differs; no package files were changed. Review the collision or install into a fresh project.")
            self.unchanged += 1
            return
        if path in self.files and self.files[path][0] != raw:
            raise InstallError("Installation plan contains conflicting files.")
        self.files[path] = (raw, mode)

    def link(self, relative, target):
        path = self.project / relative
        target_path = self.project / target
        link_value = os.path.relpath(target_path, path.parent)
        if path.is_symlink():
            if os.readlink(path) == link_value and path.resolve() == target_path.resolve():
                self.unchanged += 1
                return
            raise InstallError("An existing skill symlink differs; nothing was changed.")
        safe_parent(path, self.project)
        if path.exists():
            raise InstallError("An existing skill directory would be overwritten; nothing was changed.")
        self.links[path] = link_value

    def settings(self, relative, incoming, cursor=False, host="claude"):
        path = self.project / relative
        safe_parent(path, self.project)
        old = path.read_bytes() if path.exists() else None
        try:
            existing = json.loads(old) if old is not None else {}
        except (ValueError, UnicodeError) as exc:
            raise InstallError("Existing host settings are invalid JSON; nothing was changed.") from exc
        value = merge_hooks(existing, incoming, cursor)
        # Preserve exact bytes and formatting on a repeated installation.
        if old is not None and value == existing:
            self.unchanged += 1
            return
        if old is not None:
            backup = Path(".independent-reconstruction/backups") / (host + "-" + digest(old) + ".json")
            self.add(backup, old, 0o600)
        self.configs[path] = (encoded(value), old)

    def apply(self):
        created = []
        replaced = []
        try:
            for path, (raw, mode) in self.files.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                if "backups" in path.parts:
                    path.parent.chmod(0o700)
                with path.open("xb") as handle:
                    os.chmod(path, mode)
                    handle.write(raw)
                    handle.flush()
                    os.fsync(handle.fileno())
                created.append(path)
            for path, target in self.links.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                os.symlink(target, path, target_is_directory=True)
                created.append(path)
            for path, (raw, old) in self.configs.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                # Detect changes since planning instead of overwriting another
                # process's settings update.
                current = path.read_bytes() if path.exists() else None
                if current != old:
                    raise InstallError("Host settings changed during installation; package changes are being rolled back.")
                atomic_write(path, raw)
                replaced.append((path, old))
        except Exception:
            for path, old in reversed(replaced):
                # Preserve an independent writer's later update during rollback.
                if path.is_file() and path.read_bytes() == self.configs[path][0]:
                    if old is None:
                        path.unlink()
                    else:
                        atomic_write(path, old)
            for path in reversed(created):
                path.unlink()
            raise


def atomic_write(path, raw):
    old_mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    fd, temporary = tempfile.mkstemp(prefix=".ir-install-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            os.fchmod(handle.fileno(), old_mode)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="Existing project directory")
    parser.add_argument("--host", required=True, action="append", choices=("codex", "cursor", "claude", "all"))
    parser.add_argument("--dry-run", action="store_true", help="Inspect collisions and show aggregate counts without writing")
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        raise InstallError("Python 3.11 or later is required by the package runtime.")
    project = args.project.expanduser().resolve()
    if not project.is_dir() or project == PACKAGE or PACKAGE in project.parents:
        raise InstallError("Choose an existing project outside the package tree.")
    if shutil.which("python3") is None:
        raise InstallError("python3 is required in the host hook environment.")
    if shutil.which("sh") is None:
        raise InstallError("A POSIX sh executable is required by the hook bootstrap.")
    hosts = {"codex", "cursor", "claude"} if "all" in args.host else set(args.host)
    plan = Plan(project)
    snapshot = Path(".independent-reconstruction/package")
    inventory = list(source_files())
    for rel, source in inventory:
        mode = 0o755 if source.stat().st_mode & 0o111 else 0o644
        plan.add(snapshot / rel, source.read_bytes(), mode)
    for host in sorted(hosts):
        host_root = Path({"codex": ".agents", "cursor": ".cursor", "claude": ".claude"}[host])
        skills = sorted({rel.parts[1] for rel, _ in inventory if len(rel.parts) >= 3 and rel.parts[0] == "skills"})
        for name in skills:
            plan.link(host_root / "skills" / name, snapshot / "skills" / name)
        for rel, source in inventory:
            if host in {"cursor", "claude"} and rel.parts[0] in {"agents", "commands"}:
                plan.add(host_root / rel, source.read_bytes())
            if rel.parts[0] == "rules" and rel.suffix == ".mdc":
                if host == "cursor":
                    plan.add(host_root / rel, source.read_bytes())
                elif host == "claude":
                    plan.add(host_root / "rules" / (rel.stem + ".md"), claude_rule(source.read_bytes()))
        if host in {"cursor", "claude", "codex"}:
            hook_root = Path(".codex") if host == "codex" else host_root
            for rel, source in inventory:
                if rel.parts[0] == "hooks" and rel.name != "hooks.json":
                    plan.add(hook_root / "hooks/independent-reconstruction" / Path(*rel.parts[1:]), source.read_bytes(), 0o755 if source.stat().st_mode & 0o111 else 0o644)
            template_name = {"cursor": "hooks.json", "claude": "settings.json", "codex": "hooks.json"}[host]
            template = PACKAGE / "integrations" / host / template_name
            incoming = json.loads(template.read_bytes())
            if host == "codex":
                # Project hooks run from session cwd. Use an exactly quoted
                # absolute path so subdirectory launches also work; native
                # plugin templates retain PLUGIN_ROOT instead.
                script = shlex.quote(str(project / hook_root / "hooks/independent-reconstruction/entry.sh"))
                for entries in incoming["hooks"].values():
                    for entry in entries:
                        for hook in entry["hooks"]:
                            hook["command"] = hook["command"].replace('"${PLUGIN_ROOT}/hooks/entry.sh"', script)
            plan.settings(hook_root / ("settings.json" if host == "claude" else "hooks.json"), incoming, host == "cursor", host)
    # Skill scripts and docs use a stable launcher lookup, documented in the
    # installed instruction fragment. Do not overwrite or edit AGENTS.md.
    fragment = "# Independent Reconstruction\n\nUse `.independent-reconstruction/package/README.md` and its `scripts/ir.py` CLI.\nResolve skill symlinks to the complete package snapshot for shared resources.\nCodex hooks require review and trust in /hooks; installation does not prove activation.\nRead role prompts from the package `agents/` directory and use fresh sessions for implementers.\n"
    plan.add(Path(".agents/independent-reconstruction.md"), fragment.encode())
    receipt = {"schema_version": 1, "hosts": sorted(hosts), "new_files": len(plan.files), "new_skill_links": len(plan.links), "merged_configs": len(plan.configs), "unchanged_files": plan.unchanged, "dry_run": args.dry_run, "host_activation": "restart_or_reload_and_confirm_in_host"}
    if not args.dry_run:
        plan.apply()
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (InstallError, OSError, ValueError) as exc:
        # Deliberately omit paths, existing configuration contents and payloads.
        message = str(exc) if isinstance(exc, InstallError) else "Installation failed; review permissions and package structure."
        print(json.dumps({"error": message}), file=sys.stderr)
        raise SystemExit(1)
