"""Offline dependency inventory; never resolves or replaces dependencies."""
import json
from pathlib import Path
import re
import tomllib
from .storage import Invalid, file_hash


def scan(filename):
    path = Path(filename)
    rows = []
    unresolved = []
    def add(ecosystem, name, constraint, scope):
        rows.append({"ecosystem": ecosystem, "name": name, "constraint": constraint,
                     "scope": scope, "resolution": "unresolved", "license": "unknown"})
    if path.name == "package.json":
        obj = json.loads(path.read_text())
        for scope in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
            for name, version in obj.get(scope, {}).items():
                add("npm", name, version, scope)
    elif path.name == "Cargo.toml":
        obj = tomllib.loads(path.read_text())
        def tables(table, prefix=""):
            for scope in ("dependencies", "dev-dependencies", "build-dependencies"):
                for name, value in table.get(scope, {}).items():
                    add("cargo", name, value, prefix + scope)
        tables(obj)
        tables(obj.get("workspace", {}), "workspace.")
        for platform, table in obj.get("target", {}).items():
            tables(table, "target." + platform + ".")
        if "workspace" in obj:
            unresolved.append("Workspace members require individual manifests")
    elif path.name == "pyproject.toml":
        obj = tomllib.loads(path.read_text())
        project = obj.get("project", {})
        for item in project.get("dependencies", []):
            add("pypi", re.split(r"[<>=!~\[; @]", item, 1)[0], item, "dependencies")
        for group, items in project.get("optional-dependencies", {}).items():
            for item in items:
                add("pypi", re.split(r"[<>=!~\[; @]", item, 1)[0], item, "optional." + group)
        if project.get("dynamic") or obj.get("tool"):
            unresolved.append("Dynamic and tool-specific dependency declarations need review")
    elif path.name.startswith("requirements") and path.suffix == ".txt":
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("-") or line.endswith("\\"):
                unresolved.append("Include, option or continued requirement needs review")
            else:
                add("pypi", re.split(r"[<>=!~\[; @]", line, 1)[0], line, "requirements")
    elif path.name == "go.mod":
        block = False
        for raw in path.read_text().splitlines():
            line = raw.split("//", 1)[0].strip()
            if line == "require (":
                block = True
                continue
            if line == ")":
                block = False
                continue
            if line.startswith("replace") or line.startswith("exclude"):
                unresolved.append("Go replacement or exclusion needs review")
            value = line.removeprefix("require ") if line.startswith("require ") else line if block else ""
            parts = value.split()
            if len(parts) == 2:
                add("go", parts[0], parts[1], "require")
    else:
        raise Invalid("Supported manifests: package.json, Cargo.toml, pyproject.toml, requirements*.txt, go.mod")
    return {"schema_version": 1, "manifest_sha256": file_hash(path), "dependencies": rows,
            "unresolved": unresolved, "transitive_inventory": "not-established", "network": "unused"}
