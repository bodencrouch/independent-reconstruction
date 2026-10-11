"""Private, locked storage with a hash-chained event ledger."""
import contextlib
import datetime
import hashlib
import json
import os
import re
from pathlib import Path
import tempfile
import fcntl


class Invalid(ValueError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    with open(path, encoding="utf-8") as stream:
        return parse_json(stream.read())


def parse_json(raw):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise Invalid("Duplicate JSON key")
            out[key] = value
        return out
    value = json.loads(raw, object_pairs_hook=unique,
                       parse_constant=lambda _: (_ for _ in ()).throw(Invalid("Non-finite JSON")))
    canonical(value)
    return value


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(canonical(value) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class Run:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.private = self.root / ".ir"
        if not self.private.is_dir() or self.private.is_symlink():
            raise Invalid("Run has not been initialized")

    @contextlib.contextmanager
    def lock(self):
        lock_path = self.private / "lock"
        if lock_path.is_symlink() or (lock_path.exists() and not lock_path.is_file()):
            raise Invalid("Run lock is not a regular file")
        with open(self.private / "lock", "a+b") as stream:
            os.chmod(stream.name, 0o600)
            fcntl.flock(stream, fcntl.LOCK_EX)
            self.events()
            yield self

    def events(self):
        path = self.private / "audit.jsonl"
        previous = "0" * 64
        events = []
        if not path.exists() or path.is_symlink() or not path.is_file():
            raise Invalid("Missing audit ledger")
        for line in path.read_text(encoding="utf-8").splitlines():
            item = parse_json(line)
            stamp = item.pop("hash", None)
            if item.get("previous") != previous or item.get("sequence") != len(events) + 1 or digest(item) != stamp:
                raise Invalid("Audit chain is invalid")
            item["hash"] = stamp
            events.append(item)
            previous = stamp
        if not events or events[0]["kind"] != "init":
            raise Invalid("Missing initialization event")
        return events

    def append(self, kind, data):
        events = self.events() if (self.private / "audit.jsonl").exists() else []
        event = {"sequence": len(events) + 1,
                 "previous": events[-1]["hash"] if events else "0" * 64,
                 "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 "kind": kind, "data": data}
        event["hash"] = digest(event)
        with open(self.private / "audit.jsonl", "ab") as stream:
            os.chmod(stream.name, 0o600)
            stream.write(canonical(event) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        return event

    def artifact(self, value):
        sha = digest(value)
        path = self.private / "objects" / (sha + ".json")
        if path.is_symlink() or path.parent.is_symlink() or (path.exists() and not path.is_file()):
            raise Invalid("Artifact must be a private regular file")
        if path.exists():
            if digest(read_json(path)) != sha:
                raise Invalid("Content-addressed artifact changed")
        else:
            write_json(path, value)
        return sha

    def object(self, sha):
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
            raise Invalid("Invalid artifact digest")
        path = self.private / "objects" / (sha + ".json")
        if path.is_symlink() or not path.is_file() or path.parent.is_symlink():
            raise Invalid("Artifact must be a private regular file")
        obj = read_json(path)
        if digest(obj) != sha:
            raise Invalid("Content-addressed artifact changed")
        return obj

    def latest(self, kind):
        return next((e for e in reversed(self.events()) if e["kind"] == kind), None)

    def clean(self):
        if self.latest("incident"):
            raise Invalid("Run is quarantined; create a fresh run and review unaffected evidence")

    def verify(self):
        events = self.events()
        for e in events:
            for key, value in e["data"].items():
                if key.endswith("_object"):
                    self.object(value)
        policy_event = next((e for e in reversed(events) if "policy_object" in e["data"]), None)
        if not policy_event or digest(read_json(self.private / "policy.json")) != policy_event["data"]["policy_object"]:
            raise Invalid("Run policy differs from the recorded policy")
        handoff = self.latest("handoff")
        if handoff:
            root = Path(handoff["data"]["root"])
            candidate = root / "candidate"
            if root.is_symlink() or root.resolve() != root or candidate.is_symlink() or not candidate.is_dir():
                raise Invalid("Handoff or candidate directory was replaced")
            if file_hash(root / "manifest.json") != handoff["data"]["manifest_sha256"]:
                raise Invalid("Handoff manifest changed")
            manifest = read_json(root / "manifest.json")
            if set(manifest.get("files", {})) != {"spec.json", "AGENTS.md"}:
                raise Invalid("Handoff inventory differs from the required sealed files")
            for relative, expected in manifest["files"].items():
                path = root / relative
                if path.is_symlink() or path.resolve().parent != root or file_hash(path) != expected:
                    raise Invalid("Sealed handoff changed")
        return {"events": len(events), "head": events[-1]["hash"],
                "quarantined": bool(self.latest("incident")),
                "integrity": "verified-local-chain", "external_anchor": "not-established"}
