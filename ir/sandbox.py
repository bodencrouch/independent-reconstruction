"""Linux bubblewrap launch with no source/home mounts and no network."""
import os
from pathlib import Path
import shutil
import subprocess
from .storage import Invalid, read_json


def launch(run, argv):
    run.clean()
    run.verify()
    event = run.latest("handoff")
    if not event:
        raise Invalid("No sealed handoff")
    executable = shutil.which("bwrap")
    if not executable:
        raise Invalid("bubblewrap is unavailable; no unsandboxed fallback")
    if not argv:
        raise Invalid("Specify an implementation tool command")
    root = Path(event["data"]["root"])
    policy = read_json(run.private / "policy.json")
    for source in map(Path, policy["source_roots"]):
        if any(source == Path(p) or source.is_relative_to(p) or Path(p).is_relative_to(source)
               for p in ("/usr", "/bin", "/lib", "/lib64")):
            raise Invalid("A registered source overlaps trusted runtime mounts; use a separate VM image")
    args = [executable, "--die-with-parent", "--new-session", "--unshare-all", "--clearenv",
            "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "HOME", "/home/implementer",
            "--setenv", "LANG", "C.UTF-8", "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
            "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--dir", "/home/implementer"]
    for path in ("/usr", "/bin", "/lib", "/lib64"):
        if Path(path).exists():
            args += ["--ro-bind", path, path]
    # /etc and host /home are deliberately absent. System runtimes are a trusted mount.
    args += ["--dir", "/handoff"]
    for name in ("spec.json", "AGENTS.md", "manifest.json"):
        args += ["--ro-bind", str(root / name), "/handoff/" + name]
    args += ["--bind", str(root / "candidate"), "/handoff/candidate",
             "--chdir", "/handoff/candidate", "--", *argv]
    run.append("sandbox-launch", {"command_sha256": __import__("hashlib").sha256(repr(argv).encode()).hexdigest(),
                                  "network": "disabled", "source_mounts": 0})
    result = subprocess.run(args, check=False)
    run.append("sandbox-exit", {"exit_code": result.returncode})
    return {"exit_code": result.returncode, "isolation": "bubblewrap-process", "limits": "host-kernel-and-system-runtime-trusted"}
