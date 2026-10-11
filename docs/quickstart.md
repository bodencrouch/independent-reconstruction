# Create a reconstruction run

These commands use a fictional counter interface authored for this package.
`IR_PACKAGE` below is a shell variable chosen for this workflow, not a host magic variable.

```bash
IR_PACKAGE=/home/brunner56/plugins/independent-reconstruction
python3 "$IR_PACKAGE/scripts/ir.py" init /home/brunner56/ir-runs/counter --target counter-protocol --language Python
python3 "$IR_PACKAGE/scripts/ir.py" observe /home/brunner56/ir-runs/counter --record "$IR_PACKAGE/examples/observation.json"
python3 "$IR_PACKAGE/scripts/ir.py" check /home/brunner56/ir-runs/counter --spec "$IR_PACKAGE/examples/spec.json"
python3 "$IR_PACKAGE/scripts/ir.py" digest "$IR_PACKAGE/examples/spec.json"
```

Replace the example observation's zero digest with a real digest when collecting
external evidence. The zero digest labels this synthetic contract only; it is not
a receipt that reference software was observed.

The firewall reviewer works in a separate context. It reads the candidate contract
and authorized private provenance, checks each requirement, and fills a review based
on `examples/review-template.json`. Set `spec_sha256` to the digest printed above;
record the real reviewer/context and findings. Do not auto-approve a template.
Register the actual reviewer first with `session --record REVIEWER_SESSION.json`;
use role `firewall-reviewer` and make its context/exposure match the review exactly.

```bash
python3 "$IR_PACKAGE/scripts/ir.py" approve /home/brunner56/ir-runs/counter --spec "$IR_PACKAGE/examples/spec.json" --review /home/brunner56/ir-runs/counter-review.json
python3 "$IR_PACKAGE/scripts/ir.py" handoff /home/brunner56/ir-runs/counter --dest /home/brunner56/ir-handoffs/counter
python3 "$IR_PACKAGE/scripts/ir.py" packet /home/brunner56/ir-runs/counter --dest /home/brunner56/ir-handoffs/counter-launch.json
```

Start a new implementation context from only the sealed handoff. A source-exposed
coordinator must not implement from the original conversation. Record actual model
metadata with `session --record SESSION.json`. The empty candidate folder is the
implementer's destination. The CLI prepares evidence; it does not silently buy
provider access or start a cloud model.

On Linux, a controller can launch an installed offline tool inside the sandbox:

```bash
python3 "$IR_PACKAGE/scripts/ir.py" sandbox /home/brunner56/ir-runs/counter -- /usr/bin/python3 /handoff/candidate/tool.py
```

Create reviewer-owned reference and candidate adapters according to docs/adapters.md.
They are supplied by the workflow owner, not downloaded from the reference project.
The candidate adapter points to candidate code; keep oracle access away from the
implementation context. After implementation is ready, the reviewer runs:
Review case contents using `examples/corpus-review-template.json`, bind it to both
the specification and case digests, and approve that corpus. Record the actual fresh
implementer session before validation. These records are attestations, not authentication.

```bash
python3 "$IR_PACKAGE/scripts/ir.py" approve-cases /home/brunner56/ir-runs/counter --cases "$IR_PACKAGE/examples/cases.json" --review /home/brunner56/ir-runs/counter-corpus-review.json
python3 "$IR_PACKAGE/scripts/ir.py" validate /home/brunner56/ir-runs/counter --cases "$IR_PACKAGE/examples/cases.json" --oracle '["/usr/bin/python3","/absolute/reviewer/oracle_adapter.py"]' --candidate '["/usr/bin/python3","/absolute/handoff/candidate/adapter.py"]'
python3 "$IR_PACKAGE/scripts/ir.py" audit /home/brunner56/ir-runs/counter
python3 "$IR_PACKAGE/scripts/ir.py" report /home/brunner56/ir-runs/counter
python3 "$IR_PACKAGE/scripts/ir.py" export /home/brunner56/ir-runs/counter --dest /home/brunner56/ir-exports/counter
```

Arguments are JSON arrays, not shell strings. Add timeout explicitly for slow
adapters. A timeout or invalid adapter output fails the case. Candidate changes
after measurement make the report stale. Exporting an unmeasured summary is allowed
and explicitly labeled; it does not manufacture a passing result.

For actual package replacement, use `$ir-replace-dependency` and the relevant
scenario skill. Do not rewrite a consumer manifest merely because a candidate compiles.
