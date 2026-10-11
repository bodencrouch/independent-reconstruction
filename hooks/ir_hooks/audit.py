"""Owner-private, payload-free hook receipts, separate from the run ledger."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat


def record(run: Path, role: str, host: str, event: str, payload: bytes, decision: str, code: str):
    directory = run / ".ir"
    if directory.is_symlink() or not directory.is_dir():
        raise OSError("Private hook registry is unavailable.")
    directory_stat = directory.stat()
    if hasattr(os, "getuid") and directory_stat.st_uid != os.getuid():
        raise OSError("Private hook registry has an unexpected owner.")
    if directory_stat.st_mode & 0o077:
        raise OSError("Private hook registry must be owner-only.")
    item = {
        "schema_version": 1,
        "time": datetime.now(timezone.utc).isoformat(),
        "host": host,
        "event": event,
        "role": role,
        "payload_sha256": hashlib.sha256(payload).hexdigest(),
        "decision": decision,
        "reason_code": code,
    }
    raw = (json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n").encode()
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(directory / "hook-events.jsonl", flags, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077:
            raise OSError("Hook registry is not an owner-private regular file.")
        if hasattr(os, "getuid") and info.st_uid != os.getuid():
            raise OSError("Hook registry has an unexpected owner.")
        try:
            import fcntl
        except ImportError:
            fcntl = None
        if fcntl:
            fcntl.flock(fd, fcntl.LOCK_EX)
        if os.write(fd, raw) != len(raw):
            raise OSError("Hook receipt was not fully written.")
        os.fsync(fd)
    finally:
        os.close(fd)
