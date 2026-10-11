"""Differential JSON adapter runner. Outputs remain in the private run."""
import json
import math
from decimal import Decimal
import os
from pathlib import Path
import resource
import signal
import subprocess
import shutil
import tempfile
import time
from .contracts import cases
from .storage import Invalid, canonical, digest, file_hash, parse_json
from .workflow import approved


def command(value):
    if not isinstance(value, list) or not value or any(not isinstance(v, str) or not v or "\x00" in v for v in value):
        raise Invalid("Adapter command must be a JSON array of arguments")
    return value


def limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def execute(argv, data, timeout):
    started = time.monotonic()
    env = {key: value for key, value in os.environ.items() if key in {"PATH", "LANG", "LC_ALL", "TZ"}}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        proc = subprocess.Popen(command(argv), stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                env=env, start_new_session=True, preexec_fn=limits)
        timed_out = False
        try:
            proc.communicate(canonical(data) + b"\n", timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGKILL)
            proc.communicate()
        stdout.seek(0)
        raw = stdout.read(1024 * 1024 + 1)
        stderr.seek(0)
        error = stderr.read(1024 * 1024 + 1)
    result = {"exit_code": proc.returncode, "timeout": timed_out,
              "elapsed_seconds": round(time.monotonic() - started, 6),
              "stdout_sha256": __import__("hashlib").sha256(raw).hexdigest(),
              "stderr_sha256": __import__("hashlib").sha256(error).hexdigest()}
    if timed_out or proc.returncode != 0 or len(raw) > 1024 * 1024:
        result["status"] = "adapter-failure"
    else:
        try:
            output = parse_json(raw)
            canonical(output)
            result.update(status="ok", output=output)
        except (ValueError, UnicodeError):
            result["status"] = "invalid-json-output"
    return result


def equal(left, right, case):
    if case["comparison"] == "exact":
        return canonical(left) == canonical(right)
    if type(left) not in {int, float} or type(right) not in {int, float}:
        return False
    a, b = Decimal(str(left)), Decimal(str(right))
    absolute = Decimal(str(case["tolerance"]["absolute"]))
    relative = Decimal(str(case["tolerance"]["relative"]))
    return abs(a - b) <= max(absolute, relative * max(abs(a), abs(b)))


def tree_hash(root):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise Invalid("Candidate snapshot root must be a real directory")
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise Invalid("Candidate snapshot cannot contain symbolic links")
        if path.is_file():
            from .storage import file_hash
            files[str(path.relative_to(root))] = file_hash(path)
    return digest(files), len(files)


def validate(run, corpus, oracle, candidate, timeout):
    run.clean()
    run.verify()
    contract = approved(run)
    reqs = cases(corpus, contract)
    handoff = run.latest("handoff")
    if not handoff:
        raise Invalid("Seal an implementation handoff before conformance validation")
    root = Path(handoff["data"]["root"]) / "candidate"
    from .sessions import require_session
    require_session(run, "implementer")
    from .corpus import require_approved
    require_approved(run, corpus)
    oracle, candidate = command(oracle), command(candidate)
    if oracle == candidate:
        raise Invalid("Reference and candidate commands must be distinct")
    pinned = {}
    candidate_refs = []
    for role, argv in (("oracle", oracle), ("candidate", candidate)):
        executable = shutil.which(argv[0])
        if not executable:
            raise Invalid("Adapter executable cannot be resolved")
        files = [Path(executable).resolve()]
        for value in argv[1:]:
            path = Path(value)
            if path.is_absolute() and path.exists():
                if path.is_symlink() or not path.is_file():
                    raise Invalid("Adapter file references must be regular non-symlink files")
                files.append(path.resolve())
                if role == "candidate" and path.resolve().is_relative_to(root):
                    candidate_refs.append(str(path.resolve()))
        if role == "candidate" and files[0].is_relative_to(root):
            candidate_refs.append(str(files[0]))
        pinned[role] = {str(path): file_hash(path) for path in files}
    if not candidate_refs:
        raise Invalid("Candidate command must reference an absolute implementation file inside candidate/")
    before, file_count = tree_hash(root)
    if file_count == 0:
        raise Invalid("Candidate has no implementation artifacts")
    results = []
    for case in corpus["cases"]:
        reference = execute(oracle, case["input"], timeout)
        built = execute(candidate, case["input"], timeout)
        passed = reference["status"] == built["status"] == "ok" and equal(reference["output"], built["output"], case)
        results.append({"id": case["id"], "requirement_ids": case["requirement_ids"],
                        "passed": passed, "oracle": reference, "candidate": built})
    after, _ = tree_hash(root)
    if before != after:
        raise Invalid("Candidate changed during conformance execution; rerun on a stable snapshot")
    if any(file_hash(path) != sha for files in pinned.values() for path, sha in files.items()):
        raise Invalid("Adapter artifacts changed during conformance execution")
    coverage = {req: {r["id"] for r in results if r["passed"] and req in r["requirement_ids"]} for req in reqs}
    missing = {req: sorted(expected - coverage[req]) for req, expected in reqs.items() if expected - coverage[req]}
    report = {"schema_version": 1, "spec_sha256": digest(contract), "cases_sha256": digest(corpus),
              "candidate_tree_sha256": after, "candidate_files": file_count,
              "adapter_commands": {"oracle": oracle, "candidate": candidate},
              "adapter_artifacts": pinned, "candidate_binding": "declared-command-artifact",
              "results": results, "missing_or_failing_acceptance": missing,
              "passed": sum(r["passed"] for r in results), "total": len(results),
              "status": "corpus-conformant" if not missing and all(r["passed"] for r in results) else "incomplete-or-divergent",
              "limits": ["Only the supplied corpus was measured", "Adapter fidelity is not established by this runner",
                         "Candidate binding covers declared command files, not wrapper fidelity or dynamic dependencies",
                         "Stateful sessions must be a sequence inside one adapter input", "No legal determination"]}
    run.append("validation", {"report_object": run.artifact(report)})
    return {k: report[k] for k in ("passed", "total", "status", "missing_or_failing_acceptance", "candidate_tree_sha256")}
