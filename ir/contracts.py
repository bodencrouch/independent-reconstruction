"""Strict contract validation and conservative implementation-detail screening."""
import re
from .storage import Invalid, canonical

ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,95}$")
KINDS = {"api-trace", "binary-behavior", "documentation", "source-analysis", "experiment", "user-requirement"}
CATEGORIES = {"api", "errors", "state", "file-format", "numeric", "performance", "security", "compatibility", "environment"}


def fields(obj, required, optional=()):
    if not isinstance(obj, dict) or set(obj) - set(required) - set(optional) or set(required) - set(obj):
        raise Invalid("Object has missing or unexpected fields")


def text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 16000:
        raise Invalid("Expected nonempty bounded text")


def strings(value, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise Invalid("Expected an array")
    for item in value:
        text(item)


def identifier(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise Invalid("Invalid opaque identifier")


def observation(obj):
    fields(obj, ("id", "kind", "summary", "origin", "confidence"))
    identifier(obj["id"])
    text(obj["summary"])
    if obj["kind"] not in KINDS or obj["confidence"] not in {"observed", "inferred", "unknown"}:
        raise Invalid("Invalid evidence classification")
    fields(obj["origin"], ("locator", "sha256", "license"))
    for value in obj["origin"].values():
        text(value)
    if not re.fullmatch("[0-9a-f]{64}", obj["origin"]["sha256"]):
        raise Invalid("Evidence digest must be SHA-256")


def spec(obj, evidence):
    fields(obj, ("schema_version", "target", "requirements", "interfaces", "exclusions", "unknowns"))
    if type(obj["schema_version"]) is not int or obj["schema_version"] != 1:
        raise Invalid("Unsupported contract version")
    fields(obj["target"], ("name", "version", "interface", "language", "environment"))
    for value in obj["target"].values():
        text(value)
    strings(obj["exclusions"])
    strings(obj["unknowns"])
    if not isinstance(obj["requirements"], list) or not obj["requirements"]:
        raise Invalid("At least one behavioral requirement is required")
    ids = set()
    for req in obj["requirements"]:
        fields(req, ("id", "statement", "category", "evidence", "confidence", "acceptance"))
        identifier(req["id"])
        if req["id"] in ids:
            raise Invalid("Duplicate requirement identifier")
        ids.add(req["id"])
        text(req["statement"])
        strings(req["evidence"], True)
        strings(req["acceptance"], True)
        for case_id in req["acceptance"]:
            identifier(case_id)
        if req["category"] not in CATEGORIES or req["confidence"] not in {"observed", "inferred"}:
            raise Invalid("Invalid requirement classification")
        if any(e not in evidence for e in req["evidence"]):
            raise Invalid("Requirement lacks registered evidence")
        if req["confidence"] == "observed" and any(evidence[e]["confidence"] != "observed" for e in req["evidence"]):
            raise Invalid("Observed requirement cites uncertain evidence")
    if not isinstance(obj["interfaces"], list) or not obj["interfaces"]:
        raise Invalid("At least one interface is required")
    for interface in obj["interfaces"]:
        fields(interface, ("name", "inputs", "outputs", "errors"))
        for value in interface.values():
            text(value)
    return screen(obj)


def screen(obj):
    # A screen can reject obvious leaks. A human/independent reviewer still decides.
    patterns = {
        "code-fence": r"```",
        "source-path": r"(?:/home/|/run/media/|[A-Za-z]:\\|\.git/|https?://[^\s]+/(?:blob|raw)/)",
        "implementation-prescription": r"\b(?:copy (?:the )?(?:code|implementation)|use (?:the )?same algorithm|internal (?:variable|function|class)|decompiled (?:code|pseudocode)|line [0-9]+|source code below)\b",
        "code-syntax": r"(?:\b(?:def|class)\s+\w+\s*\(|\bfunction\s*\w*\s*\(|=>\s*\{|#include\s*[<\"])",
        "credential": r"(?:-----BEGIN .*PRIVATE KEY-----|\b(?:sk|hf)_[A-Za-z0-9]{20,})",
    }
    blob = canonical(obj).decode()
    return [{"severity": "blocking", "rule": name} for name, pattern in patterns.items()
            if re.search(pattern, blob, re.I)]


def review(obj, sha, requirement_ids):
    fields(obj, ("schema_version", "spec_sha256", "reviewer", "decision", "findings", "limits"))
    if type(obj["schema_version"]) is not int or obj["schema_version"] != 1 or obj["spec_sha256"] != sha:
        raise Invalid("Review is not bound to this specification")
    fields(obj["reviewer"], ("identity", "context_id", "exposure"))
    for value in obj["reviewer"].values():
        text(value)
    if obj["reviewer"]["exposure"] not in {"review-only", "source-exposed"}:
        raise Invalid("Reviewer exposure must be recorded")
    if obj["decision"] not in {"approve", "reject"} or not isinstance(obj["findings"], list):
        raise Invalid("Invalid review decision")
    strings(obj["limits"], True)
    for finding in obj["findings"]:
        fields(finding, ("severity", "requirement_id", "reason"))
        if finding["severity"] not in {"blocking", "advisory"} or finding["requirement_id"] not in requirement_ids:
            raise Invalid("Invalid review finding")
        text(finding["reason"])
    if obj["decision"] != "approve" or any(f["severity"] == "blocking" for f in obj["findings"]):
        raise Invalid("Firewall review rejected the contract")


def cases(obj, contract):
    fields(obj, ("schema_version", "cases"))
    if type(obj["schema_version"]) is not int or obj["schema_version"] != 1 or not isinstance(obj["cases"], list) or not obj["cases"]:
        raise Invalid("Invalid conformance cases")
    reqs = {r["id"]: set(r["acceptance"]) for r in contract["requirements"]}
    seen = set()
    for case in obj["cases"]:
        fields(case, ("id", "requirement_ids", "input", "comparison"), ("tolerance",))
        identifier(case["id"])
        if case["id"] in seen:
            raise Invalid("Duplicate case identifier")
        seen.add(case["id"])
        strings(case["requirement_ids"], True)
        if any(r not in reqs or case["id"] not in reqs[r] for r in case["requirement_ids"]):
            raise Invalid("Case is not declared by its requirements")
        if case["comparison"] not in {"exact", "numeric"}:
            raise Invalid("Unknown comparison mode")
        if case["comparison"] == "numeric":
            fields(case.get("tolerance"), ("absolute", "relative"))
            for v in case["tolerance"].values():
                if type(v) not in {int, float} or v < 0:
                    raise Invalid("Invalid numeric tolerance")
        elif "tolerance" in case:
            raise Invalid("Exact comparison cannot have tolerance")
        canonical(case["input"])
    return reqs
