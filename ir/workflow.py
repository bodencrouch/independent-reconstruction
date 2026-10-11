"""Evidence intake, specification firewall, sealed handoff and incidents."""
import os
import hashlib
from pathlib import Path
import shutil
import uuid
from . import contracts
from .storage import Invalid, Run, digest, file_hash, read_json, write_json

IMPLEMENTER_GUIDANCE = """# Implement from the sealed behavioral contract

This directory is an implementation handoff. Read only spec.json and this file.
Write original code in candidate/. Keep architecture decisions independent.
Do not retrieve the reference project, its source, histories, plans, test code,
private observations, model sessions, or analyst transcripts. Do not use network,
MCP, inherited conversation, or source-exposed helpers to fill unknown behavior.
Ask for a new behavioral requirement using opaque requirement IDs. Do not accept
free-form analyst replies; changes require a new firewall-reviewed handoff.
Record model/provider/context, toolchain, unknowns and your own design decisions.
Stop and report any unexpected source exposure. A passing conformance corpus
does not establish complete compatibility or legal independence.
"""
LAUNCH_PROMPT = "Implement the behavioral contract in spec.json using only the sealed handoff. Read AGENTS.md. Work in candidate/. Report unknown behavior by requirement ID. Do not retrieve source or inherit analyst context."


def initialize(root, target, language, source_roots):
    root = Path(root).resolve()
    source_roots = [str(Path(p).resolve()) for p in source_roots]
    if any(root == Path(p) or root.is_relative_to(p) or Path(p).is_relative_to(root) for p in source_roots):
        raise Invalid("Run and source roots must be separate")
    root.mkdir(parents=True, exist_ok=True)
    private = root / ".ir"
    private.mkdir(mode=0o700, exist_ok=False)
    os.chmod(private, 0o700)
    (private / "objects").mkdir(mode=0o700)
    run = Run(root)
    run_id = str(uuid.uuid4())
    policy = {"schema_version": 1, "source_roots": source_roots, "roles": {}}
    write_json(private / "policy.json", policy)
    run.append("init", {"run_id": run_id, "target": target, "language": language,
                        "policy_object": run.artifact(policy)})
    return {"run_id": run_id, "phase": "observation", "source_roots_registered": len(source_roots)}


def evidence(run):
    out = {}
    for event in run.events():
        if event["kind"] == "observation":
            item = run.object(event["data"]["record_object"])
            if item["id"] in out:
                raise Invalid("Duplicate evidence identifier in ledger")
            out[item["id"]] = item
    return out


def observe(run, item):
    run.clean()
    contracts.observation(item)
    if item["id"] in evidence(run):
        raise Invalid("Evidence identifier already exists; use a new identifier")
    sha = run.artifact(item)
    run.append("observation", {"record_object": sha})
    return {"registered": item["id"], "record_sha256": sha}


def check(run, contract):
    findings = contracts.spec(contract, evidence(run))
    init = run.events()[0]["data"]
    if contract["target"]["name"] != init["target"] or contract["target"]["language"] != init["language"]:
        raise Invalid("Contract target differs from initialized run")
    return {"spec_sha256": digest(contract), "findings": findings,
            "status": "rejected" if findings else "requires-independent-review"}


def approve(run, contract, review):
    run.clean()
    if run.latest("handoff"):
        raise Invalid("Run already handed off; create a new run for revised contracts")
    receipt = check(run, contract)
    if receipt["findings"]:
        raise Invalid("Automatic firewall rejected implementation details")
    contracts.review(review, receipt["spec_sha256"], {r["id"] for r in contract["requirements"]})
    from .sessions import require_session
    require_session(run, "firewall-reviewer", review["reviewer"]["context_id"], review["reviewer"]["exposure"])
    run.append("approval", {"spec_object": run.artifact(contract), "review_object": run.artifact(review)})
    return {"approved_sha256": receipt["spec_sha256"], "review_identity_is": "self-attested"}


def approved(run):
    event = run.latest("approval")
    if not event:
        raise Invalid("No approved behavioral specification")
    contract = run.object(event["data"]["spec_object"])
    review = run.object(event["data"]["review_object"])
    if check(run, contract)["findings"]:
        raise Invalid("Approved artifact fails firewall")
    contracts.review(review, digest(contract), {r["id"] for r in contract["requirements"]})
    return contract


def handoff(run, dest):
    run.clean()
    run.verify()
    if run.latest("handoff"):
        raise Invalid("One sealed handoff per run; resume verifies the existing handoff")
    contract = approved(run)
    dest = Path(dest).resolve()
    policy = read_json(run.private / "policy.json")
    excluded = [run.root, Path(__file__).resolve().parents[1], *map(Path, policy["source_roots"])]
    if any(dest == p or dest.is_relative_to(p) or p.is_relative_to(dest) for p in excluded):
        raise Invalid("Handoff must be separate from source, package, and private run roots")
    dest.mkdir(parents=True, mode=0o700, exist_ok=False)
    try:
        write_json(dest / "spec.json", contract)
        (dest / "AGENTS.md").write_text(IMPLEMENTER_GUIDANCE, encoding="utf-8")
        os.chmod(dest / "AGENTS.md", 0o600)
        (dest / "candidate").mkdir(mode=0o700)
        manifest = {"schema_version": 1, "run_id": run.events()[0]["data"]["run_id"],
                    "spec_sha256": digest(contract),
                    "files": {name: file_hash(dest / name) for name in ("spec.json", "AGENTS.md")}}
        write_json(dest / "manifest.json", manifest)
        seal = {"root": str(dest), "manifest_sha256": file_hash(dest / "manifest.json")}
        policy["sealed_handoff"] = seal
        policy["roles"]["implementer"] = {"read_roots": [str(dest / name) for name in ("spec.json", "AGENTS.md", "manifest.json")],
                                           "write_roots": [str(dest / "candidate")],
                                           "permitted_prompt_sha256": [hashlib.sha256(LAUNCH_PROMPT.encode()).hexdigest()]}
        write_json(run.private / "policy.json", policy)
        run.append("handoff", {**seal, "policy_object": run.artifact(policy)})
    except BaseException:
        # Keep partial output for forensic recovery; never silently delete work.
        raise
    return {"sealed": True, "spec_sha256": digest(contract), "files": len(manifest["files"]),
            "isolation": "artifact-boundary-only-until-sandbox-launch"}


def incident(run, record):
    contracts.fields(record, ("kind", "summary", "affected_roles", "evidence_ids", "containment", "recovery"))
    for key in ("kind", "summary", "containment", "recovery"):
        contracts.text(record[key])
    contracts.strings(record["affected_roles"], True)
    contracts.strings(record["evidence_ids"])
    run.append("incident", {"record_object": run.artifact(record)})
    return {"phase": "quarantined", "recovery": "fresh-run-required"}
