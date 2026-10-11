"""Deterministic local distribution without private research or run artifacts."""
import hashlib
import json
from pathlib import Path
import zipfile
from .storage import Invalid

PUBLIC_DIRS = {"ir", "scripts", "schemas", "examples", "docs", "skills", "agents", "commands", "rules",
               "hooks", "integrations", ".codex-plugin", ".cursor-plugin", ".claude-plugin"}
PUBLIC_FILES = {"README.md", "AGENTS.md", "LICENSE.txt", ".gitignore", "plugin.json"}
EXCLUDED = {"private", "runs", "handoffs", "candidate", "exports", ".ir", ".git", "__pycache__",
            ".independent-reconstruction", "node_modules", ".venv", "target", "dist"}


def inventory(root):
    root = Path(root).resolve()
    files = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED for part in relative.parts):
            continue
        if relative.parts[0] not in PUBLIC_DIRS and str(relative) not in PUBLIC_FILES:
            continue
        if path.is_symlink():
            raise Invalid("Distribution inventory cannot include symbolic links")
        if path.is_file():
            files.append((relative, path))
    return files


def bundle(root, destination):
    root = Path(root).resolve()
    dest = Path(destination).absolute()
    if dest.exists() or dest.is_symlink() or dest.resolve().is_relative_to(root):
        raise Invalid("Bundle must have a new destination outside the package")
    files = inventory(root)
    manifest = {"schema_version": 1, "files": {str(rel): hashlib.sha256(path.read_bytes()).hexdigest() for rel, path in files},
                "private_records": "excluded", "legal_status": "undetermined"}
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("xb") as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for relative, path in files:
                info = zipfile.ZipInfo(str(relative), (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = ((0o755 if path.stat().st_mode & 0o111 else 0o644) | 0o100000) << 16
                raw = path.read_bytes()
                if hashlib.sha256(raw).hexdigest() != manifest["files"][str(relative)]:
                    raise Invalid("Package changed during bundling; preserve the partial archive and choose a new destination")
                archive.writestr(info, raw)
            info = zipfile.ZipInfo("BUNDLE-MANIFEST.json", (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100644) << 16
            archive.writestr(info, json.dumps(manifest, sort_keys=True, indent=2) + "\n")
    return {"files": len(files) + 1, "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(), "private_records": "excluded"}
