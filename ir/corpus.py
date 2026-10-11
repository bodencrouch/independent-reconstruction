"""Digest-bound semantic approval of reviewer-side conformance corpora."""
from . import contracts, workflow
from .storage import Invalid, digest


def _choice(value, allowed, message):
    if not isinstance(value, str) or value not in allowed:
        raise Invalid(message)


def _registered_reviewer(run, reviewer):
    for event in run.events():
        if event["kind"] != "session":
            continue
        session = run.object(event["data"]["record_object"])
        if not isinstance(session, dict):
            raise Invalid("Registered session record is invalid")
        if session.get("context_id") != reviewer["context_id"]:
            continue
        if session.get("role") != "firewall-reviewer":
            raise Invalid("Corpus reviewer context has a different registered role")
        if session.get("exposure") != reviewer["exposure"]:
            raise Invalid("Corpus reviewer exposure differs from its registered session")
        return
    raise Invalid("Register the firewall reviewer session before corpus approval")


def _validate_review(run, corpus, contract, review):
    contracts.fields(review, ("schema_version", "spec_sha256", "cases_sha256", "reviewer",
                             "corpus_origin", "decision", "findings", "limits"))
    if type(review["schema_version"]) is not int or review["schema_version"] != 1:
        raise Invalid("Unsupported corpus review version")
    if review["spec_sha256"] != digest(contract) or review["cases_sha256"] != digest(corpus):
        raise Invalid("Corpus review is not bound to the exact specification and cases")
    contracts.fields(review["reviewer"], ("identity", "context_id", "exposure"))
    for value in review["reviewer"].values():
        contracts.text(value)
    _choice(review["reviewer"]["exposure"], {"review-only", "source-exposed"},
            "Invalid corpus reviewer exposure")
    _choice(review["corpus_origin"], {"original", "authorized-reference"},
            "Invalid corpus provenance classification")
    _choice(review["decision"], {"approve", "reject"}, "Invalid corpus review decision")
    contracts.strings(review["limits"], True)
    if not isinstance(review["findings"], list):
        raise Invalid("Corpus review findings must be an array")
    case_ids = {case["id"] for case in corpus["cases"]}
    for finding in review["findings"]:
        contracts.fields(finding, ("severity", "case_id", "reason"))
        _choice(finding["severity"], {"blocking", "advisory"}, "Invalid corpus finding severity")
        contracts.identifier(finding["case_id"])
        if finding["case_id"] not in case_ids:
            raise Invalid("Corpus finding cites an absent case")
        contracts.text(finding["reason"])
    _registered_reviewer(run, review["reviewer"])
    if review["decision"] != "approve" or any(f["severity"] == "blocking" for f in review["findings"]):
        raise Invalid("Firewall reviewer rejected the conformance corpus")


def approve(run, corpus, review):
    """Record approval after an actual semantic review; identity is attested."""
    run.clean()
    contract = workflow.approved(run)
    contracts.cases(corpus, contract)
    _validate_review(run, corpus, contract, review)
    cases_sha = run.artifact(corpus)
    review_sha = run.artifact(review)
    run.append("corpus-approval", {"cases_object": cases_sha, "review_object": review_sha})
    return {"approved_cases_sha256": cases_sha, "spec_sha256": digest(contract),
            "review_sha256": review_sha}


def require_approved(run, corpus):
    """Require a current exact-corpus approval before adapter execution."""
    run.clean()
    contract = workflow.approved(run)
    contracts.cases(corpus, contract)
    cases_sha = digest(corpus)
    spec_sha = digest(contract)
    for event in reversed(run.events()):
        if event["kind"] != "corpus-approval" or event["data"].get("cases_object") != cases_sha:
            continue
        approved_cases = run.object(event["data"]["cases_object"])
        if digest(approved_cases) != cases_sha:
            raise Invalid("Approved corpus artifact differs from its receipt")
        review = run.object(event["data"]["review_object"])
        if isinstance(review, dict) and review.get("spec_sha256") != spec_sha:
            continue
        _validate_review(run, corpus, contract, review)
        return {"cases_sha256": cases_sha, "spec_sha256": spec_sha,
                "review_sha256": event["data"]["review_object"]}
    raise Invalid("Approve the exact conformance corpus before validation")
