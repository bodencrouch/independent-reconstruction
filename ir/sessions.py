"""Session attestations and source-free implementation launch packets."""
from pathlib import Path
from .storage import Invalid, canonical, digest, file_hash, write_json
from .contracts import fields, strings, text
from .workflow import approved, LAUNCH_PROMPT
from .paths import output_path
import re

ROLES = {"observer", "spec-writer", "firewall-reviewer", "implementer", "conformance-reviewer",
         "coordinator", "provenance-auditor", "contamination-responder", "release-reviewer"}


def register(run, item):
    fields(item, ("role", "provider", "model", "context_id", "exposure", "artifacts", "training_history"))
    if item["role"] not in ROLES or item["exposure"] not in {"source-exposed", "review-only", "sealed-spec-only", "unknown"}:
        raise Invalid("Invalid session role or exposure")
    for key in ("provider", "model", "context_id", "training_history"):
        text(item[key])
    strings(item["artifacts"])
    if any(not re.fullmatch(r"[0-9a-f]{64}", sha) for sha in item["artifacts"]):
        raise Invalid("Session artifacts must be SHA-256 digests")
    if item["role"] == "implementer" and item["exposure"] != "sealed-spec-only":
        raise Invalid("Implementation session must attest sealed-spec-only exposure")
    for event in run.events():
        if event["kind"] == "session":
            previous = run.object(event["data"]["record_object"])
            if previous["context_id"] == item["context_id"]:
                raise Invalid("Context identifier was reused; use a genuinely fresh session")
    run.clean()
    run.append("session", {"record_object": run.artifact(item)})
    return {"role": item["role"], "record_sha256": digest(item), "attestation": "self-reported"}


def require_session(run, role, context_id=None, exposure=None):
    for event in reversed(run.events()):
        if event["kind"] != "session":
            continue
        item = run.object(event["data"]["record_object"])
        if item["role"] == role and (context_id is None or item["context_id"] == context_id):
            if exposure is not None and item["exposure"] != exposure:
                raise Invalid("Review exposure differs from the registered context")
            return item
    raise Invalid("Required role context has not been registered")


def packet(run, dest):
    run.clean()
    run.verify()
    event = run.latest("handoff")
    if not event:
        raise Invalid("Create a sealed handoff first")
    contract = approved(run)
    # No private source locators, reviewer identities, provider secrets, or transcripts.
    packet = {"schema_version": 1, "role": "implementer", "spec_sha256": digest(contract),
              "instruction": LAUNCH_PROMPT,
              "context": "new-session-required", "spec": contract,
              "training_exposure": "unknown", "legal_claim": "none"}
    dest = output_path(run, dest)
    root = Path(event["data"]["root"])
    if dest.is_relative_to(root) or dest.is_relative_to(run.root):
        raise Invalid("Launch packet must be outside sealed handoff and private run")
    write_json(dest, packet)
    run.append("launch-packet", {"packet_object": run.artifact(packet)})
    return {"packet_sha256": file_hash(dest), "context": "new-session-required", "role": "implementer"}
