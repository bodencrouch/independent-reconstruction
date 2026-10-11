---
name: ir-specify
description: Converts restricted observations into a testable behavioral specification with evidence links, uncertainty, and compatibility scope. Use explicitly before an implementation handoff.
disable-model-invocation: true
---
# Write a behavioral contract

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Read the run brief and observation receipts as the designated specification author. Maintain access separation from the eventual implementer.
2. Define the public interface and observable outcomes: accepted input, output, error categories, state changes, side effects, and ordering guarantees.
3. Give each requirement a stable ID, evidence basis, confidence or uncertainty, acceptance case mapping, and explicit scope. Mark inferred behavior and unsupported cases.
4. Express behavior in neutral terms. Exclude source excerpts, comments, private identifiers, control-flow translations, module graphs, original implementation tests, and design instructions derived from the original.
5. Include only public symbols, constants, schemas, and exact messages whose compatibility need is documented. Route each necessity through the firewall review.
6. Choose implementation freedom deliberately. Preserve externally required constraints while allowing fresh algorithms and internal architecture.
7. Run `check` on the draft. Repair structural findings and send the exact revised specification to a registered `firewall-reviewer` context. Acceptance IDs are a plan, not approval of case contents; the exact eventual corpus needs a separate review and `approve-cases` receipt before validation.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" check "$RUN" --spec "$SPEC_JSON"
```

## Return

Return the specification path and digest, requirement count, evidence coverage, remaining uncertainties, compatibility necessities requiring review, and checker result.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
