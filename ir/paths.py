"""Require new public outputs outside protected evidence and source roots."""
from pathlib import Path
from .storage import Invalid, read_json


def output_path(run, destination):
    raw = Path(destination).absolute()
    if raw.exists() or raw.is_symlink():
        raise Invalid("Output destination already exists; choose a new path")
    resolved = raw.resolve()
    policy = read_json(run.private / "policy.json")
    protected = [run.root, Path(__file__).resolve().parents[1], *map(Path, policy["source_roots"])]
    handoff = run.latest("handoff")
    if handoff:
        protected.append(Path(handoff["data"]["root"]))
    if any(resolved == p or resolved.is_relative_to(p) or p.is_relative_to(resolved) for p in protected):
        raise Invalid("Output destination overlaps protected evidence, source, package or handoff")
    return resolved
