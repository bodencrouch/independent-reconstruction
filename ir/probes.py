"""Capture original behavioral observations through a caller-owned adapter."""
from .conformance import execute
from .storage import Invalid, digest
from .workflow import observe
from .contracts import fields, identifier, text


def probe(run, plan, adapter, timeout):
    fields(plan, ("schema_version", "probes"))
    if type(plan["schema_version"]) is not int or plan["schema_version"] != 1 or not isinstance(plan["probes"], list) or not plan["probes"]:
        raise Invalid("Probe plan must contain observations")
    run.clean()
    registered = 0
    for item in plan["probes"]:
        fields(item, ("id", "input", "summary", "license"))
        identifier(item["id"])
        text(item["summary"])
        text(item["license"])
        output = execute(adapter, item["input"], timeout)
        if output["status"] != "ok":
            raise Invalid("Oracle probe failed; completed observations remain registered")
        receipt = {"input": item["input"], "result": output, "adapter_sha256": digest(adapter)}
        sha = run.artifact(receipt)
        observation = {"id": item["id"], "kind": "experiment", "summary": item["summary"],
                       "origin": {"locator": "private-object:" + sha, "sha256": sha, "license": item["license"]},
                       "confidence": "observed"}
        observe(run, observation)
        run.append("probe", {"receipt_object": sha})
        registered += 1
    return {"observations_registered": registered, "scope": "supplied-probes", "legal_status": "undetermined"}
