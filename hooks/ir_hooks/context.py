"""Load explicit run context and verify the implementer's sealed handoff."""
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re

ROLES = {"observer", "spec-writer", "firewall-reviewer", "implementer", "conformance-reviewer", "coordinator", "provenance-auditor", "contamination-responder", "release-reviewer"}
ROLE_ALIASES = {"analyst": "spec-writer", "firewall": "firewall-reviewer", "verifier": "conformance-reviewer", "auditor": "provenance-auditor"}
MAX_DOCUMENT = 16 * 1024 * 1024


class PolicyError(Exception):
    """A policy cannot be used; messages never contain paths or payloads."""


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PolicyError("JSON contains an ambiguous duplicate object key.")
        result[key] = value
    return result


def strict_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object)


def beneath(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def read_json(path: Path):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_DOCUMENT:
        raise PolicyError("Run policy or sealed artifact is unavailable.")
    try:
        return strict_json(path.read_bytes())
    except (ValueError, UnicodeError, OSError) as exc:
        raise PolicyError("Run policy or sealed artifact is invalid.") from exc


def absolute(value) -> Path:
    if not isinstance(value, str) or not value or not Path(value).is_absolute():
        raise PolicyError("Run policy requires explicit absolute directories.")
    return Path(value).resolve()


@dataclass
class Context:
    run: Path
    role: str
    policy: dict
    read_roots: tuple[Path, ...] = ()
    write_roots: tuple[Path, ...] = ()
    source_roots: tuple[Path, ...] = ()
    handoff: Path | None = None


def active() -> bool:
    # Partial activation is an error, never a way to silently disable policy.
    return bool(os.environ.get("IR_RUN") or os.environ.get("IR_ROLE"))


def load() -> Context | None:
    if not active():
        return None
    run = absolute(os.environ.get("IR_RUN"))
    role = os.environ.get("IR_ROLE")
    role = ROLE_ALIASES.get(role, role)
    if role not in ROLES:
        raise PolicyError("Set both IR_RUN and a supported IR_ROLE before using this session.")
    policy = read_json(run / ".ir" / "policy.json")
    if not isinstance(policy, dict) or type(policy.get("schema_version")) is not int or policy["schema_version"] != 1:
        raise PolicyError("Run policy has an unsupported schema.")
    ctx = Context(run, role, policy)
    if role != "implementer":
        return ctx
    roles = policy.get("roles")
    spec = roles.get("implementer") if isinstance(roles, dict) else None
    seal = policy.get("sealed_handoff")
    if not isinstance(spec, dict) or not isinstance(seal, dict):
        raise PolicyError("Implementer access requires an approved sealed handoff.")
    for key in ("read_roots", "write_roots"):
        if not isinstance(spec.get(key), list) or not spec[key]:
            raise PolicyError("Implementer policy needs explicit read and write roots.")
    ctx.read_roots = tuple(absolute(p) for p in spec["read_roots"])
    ctx.write_roots = tuple(absolute(p) for p in spec["write_roots"])
    if not isinstance(policy.get("source_roots", []), list):
        raise PolicyError("Source roots must be an explicit list.")
    ctx.source_roots = tuple(absolute(p) for p in policy.get("source_roots", []))
    ctx.handoff = absolute(seal.get("root"))
    candidate = ctx.handoff / "candidate"
    if candidate.is_symlink() or not candidate.is_dir():
        raise PolicyError("Candidate workspace must be a regular directory.")
    # Narrow policy to the actual exported pack and generated workspace. An
    # accidentally broad administrative allowlist must not expose the archive.
    if any(not beneath(p, ctx.handoff) for p in ctx.read_roots):
        raise PolicyError("Implementer read roots exceed the sealed handoff.")
    if any(not beneath(p, candidate) for p in ctx.write_roots):
        raise PolicyError("Implementer write roots exceed the candidate workspace.")
    allowed = ctx.read_roots + ctx.write_roots
    if any(beneath(p, src) or beneath(src, p) for p in allowed for src in ctx.source_roots):
        raise PolicyError("Implementer roots overlap restricted source material.")
    if any(beneath(p, run / ".ir") or beneath(run / ".ir", p) for p in allowed):
        raise PolicyError("Implementer roots overlap private run metadata.")
    expected = seal.get("manifest_sha256")
    if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
        raise PolicyError("Handoff seal is invalid.")
    manifest_path = ctx.handoff / "manifest.json"
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
        raise PolicyError("Handoff manifest has an unsupported schema.")
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != expected:
        raise PolicyError("Handoff manifest changed; reseal through the firewall workflow.")
    files = manifest.get("files") if isinstance(manifest, dict) else None
    if not isinstance(files, dict) or not {"spec.json", "AGENTS.md"} <= files.keys():
        raise PolicyError("Handoff manifest does not cover required artifacts.")
    immutable_paths = {manifest_path}
    for name, digest in files.items():
        rel = Path(name) if isinstance(name, str) else None
        if rel is None or rel.is_absolute() or ".." in rel.parts or not rel.parts:
            raise PolicyError("Handoff manifest contains an invalid artifact path.")
        target = ctx.handoff / rel
        if not beneath(target.resolve(), ctx.handoff) or beneath(target.resolve(), candidate):
            raise PolicyError("Handoff manifest exceeds the immutable export.")
        if target.is_symlink() or not target.is_file() or target.stat().st_size > MAX_DOCUMENT:
            raise PolicyError("A sealed artifact is unavailable or unsafe.")
        if not isinstance(digest, str) or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise PolicyError("A sealed artifact changed; reseal through the firewall workflow.")
        immutable_paths.add(target.resolve())
    if any(root not in immutable_paths for root in ctx.read_roots):
        raise PolicyError("Implementer read roots must name exact sealed files.")
    return ctx
