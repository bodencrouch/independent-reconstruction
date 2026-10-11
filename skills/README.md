# Use the skill collection

Every skill is explicitly invoked. Resolve the loaded `SKILL.md` real path and set `PLUGIN_ROOT` to `Path(SKILL_PATH).resolve().parents[2]`; set `RUN` to the controller's private run path. These are example shell variables, not native host variables. Read the installed engine's help and the package schemas before preparing machine records. The commands operate on a run; they do not grant access to an oracle or source repository.

| Skill | Responsibility |
| --- | --- |
| ir-orchestrate | Coordinate roles, approved handoffs, validation, and reports |
| ir-intake | Define target, access, exposure, scope, and acceptance |
| ir-observe | Capture reproducible observations with provenance |
| ir-specify | Write evidence-linked behavioral requirements |
| ir-firewall | Review information transfer and approve an exact digest |
| ir-implement | Implement from an approved pack in a fresh lane |
| ir-conformance | Compare approved cases and report bounded compatibility |
| ir-protocol | Reconstruct public state machines and sequence behavior |
| ir-binary | Define ABI contracts and binary interoperability evidence |
| ir-file-format | Specify readers, writers, preservation, and malformed inputs |
| ir-port | Preserve defined semantics across programming languages |
| ir-dependencies | Inventory manifest declarations and select replacement scope |
| ir-replace-dependency | Integrate a candidate and preserve rollback |
| ir-recover | Record exposure and create an honest recovery lane |
| ir-audit | Check provenance, integrity, approvals, caches, and claims |
| ir-release | Prepare a local evidence packet with bounded claims |
| ir-model-risk | Record training uncertainty and tool/provider exposures |
| ir-performance | Specify and measure resource behavior separately |

Each directory contains `SKILL.md` and a directly linked `reference.md`. A skill teaches a workflow; its text alone is not a filesystem, process, model, or network security boundary. The engine's deterministic checks and actual sandbox capabilities remain separate evidence. Preserve private provenance and known notices. Never equate case success or code dissimilarity with a legal verdict.

For a complete reconstruction, begin with `ir-intake` or `ir-orchestrate`. Use the domain skills only when that surface is in scope. During implementation-only work, prepare the validation plan and follow the session's test timing constraints; an explicit validation request authorizes the selected conformance phase.

## Resolve the package path

The agent substitutes the actual loaded skill path. Resolving symlinks keeps commands attached to the installed package snapshot.

```bash
SKILL_PATH=/absolute/path/to/skills/ir-intake/SKILL.md
PLUGIN_ROOT="$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve().parents[2])' "$SKILL_PATH")"
RUN=/absolute/private/path/to/run
```

`session` records participant/model/exposure metadata. `probe` captures supported JSON oracle observations. `packet` exports approved sanitized implementation inputs. Schemas under the package's `schemas/` directory define these records. Controller commands operate outside the implementation lane; the implementer receives only approved artifacts and its candidate workspace.

## Require reviewed cases and registered contexts

Specification and corpus reviews must identify the exact registered `firewall-reviewer` context and exposure. The case corpus needs its own digest-bound approval with `approve-cases`, using `schemas/corpus-review.schema.json`. Validation also requires a registered fresh implementer context. Case IDs, schema validity, and provider/model labels are insufficient substitutes. Context records remain self-attested, and training history may remain unknown.
