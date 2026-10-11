"""Public summaries contain measured claims and counts, never private evidence."""
from pathlib import Path
import difflib
import hashlib
from .storage import Invalid, digest, file_hash, read_json, write_json
from .conformance import tree_hash
from .paths import output_path


def report(run):
    integrity = run.verify()
    event = run.latest("validation")
    validation = run.object(event["data"]["report_object"]) if event else None
    handoff = run.latest("handoff")
    current = None
    if handoff:
        current, _ = tree_hash(Path(handoff["data"]["root"]) / "candidate")
    stale = bool(validation and current != validation["candidate_tree_sha256"])
    if validation:
        for files in validation.get("adapter_artifacts", {}).values():
            for path, sha in files.items():
                if not Path(path).is_file() or file_hash(path) != sha:
                    stale = True
    status = "quarantined" if integrity["quarantined"] else "unmeasured" if not validation else "stale-candidate" if stale else validation["status"]
    return {"schema_version": 1, "run_id": run.events()[0]["data"]["run_id"],
            "technical_status": status,
            "integrity": integrity, "observations_registered": sum(e["kind"] == "observation" for e in run.events()),
            "specification": "review-approved" if run.latest("approval") else "not-approved",
            "handoff": "sealed" if handoff else "not-created",
            "conformance": None if not validation else {k: validation[k] for k in
              ("passed", "total", "spec_sha256", "cases_sha256", "candidate_tree_sha256")},
            "legal_status": "undetermined",
            "independent_authorship": "not-established-by-tooling",
            "model_training_exposure": "unknown",
            "session_records": sum(e["kind"] == "session" for e in run.events()),
            "limits": ["Local hashes do not prove that records were never rewritten by their owner",
                       "Review identity and context separation are self-attested",
                       "Conformance applies only to reviewed cases, declared adapter files and candidate snapshot",
                       "Wrapper fidelity and dynamic dependency closure remain unestablished",
                       "Public export excludes private evidence; retain required notices separately"]}


def export(run, dest):
    result = report(run)
    if result["technical_status"] in {"quarantined", "stale-candidate"}:
        raise Invalid("Cannot export a quarantined or stale result")
    dest = output_path(run, dest)
    dest.mkdir(parents=True, mode=0o700, exist_ok=False)
    write_json(dest / "report.json", result)
    notice = ("This report describes a bounded engineering measurement. It does not determine licensing, "
              "copyright independence, ownership, or permission to omit notices. No source code, private "
              "observations, adapter commands or model transcripts are included. Retain applicable "
              "licenses, notices and a private provenance record when distributing an implementation.\n")
    (dest / "NOTICE.txt").write_text(notice, encoding="utf-8")
    write_json(dest / "manifest.json", {"schema_version": 1,
               "files": {name: file_hash(dest / name) for name in ("report.json", "NOTICE.txt")}})
    run.append("public-export", {"report_object": run.artifact(result)})
    return {"files": 3, "technical_status": result["technical_status"], "legal_status": "undetermined"}


def compare(left, right):
    a, b = Path(left).read_bytes(), Path(right).read_bytes()
    if max(len(a), len(b)) > 1024 * 1024:
        raise Invalid("Similarity input exceeds the bounded 1 MiB limit")
    # No snippets or source text are returned. This is a triage signal only.
    ratio = difflib.SequenceMatcher(None, a.decode("utf-8", errors="replace").splitlines(),
                                    b.decode("utf-8", errors="replace").splitlines(), autojunk=True).ratio()
    return {"method": "line-sequence-similarity", "ratio": round(ratio, 6),
            "left_sha256": hashlib.sha256(a).hexdigest(), "right_sha256": hashlib.sha256(b).hexdigest(),
            "claim": "triage-only", "legal_status": "undetermined",
            "limits": "Low textual similarity does not establish independence; no nonliteral analysis"}
