# Local release preparation and confidential evidence

Use this scenario before preparing a distributable implementation, publishing a technical claim, or opening an upstream PR. The goal is a concrete reviewable local deliverable with accurate provenance and bounded compatibility claims.

## Public/private separation

| Proposed distributable | Owner-private records |
| --- | --- |
| Independently written implementation/build files | Original/source inputs and unauthorized distributable material |
| Applicable dependency/asset/data notices | Evidence origin locators, raw/private observations |
| Reviewed public usage/compatibility docs | Provider transcripts, exposure declarations, review rationale |
| Sanitized scope/conformance/process summary | Full provenance registry, private IDs/paths/secrets |
| Synthetic independently authored allowed cases if desired | Copied upstream tests/fixtures and raw captures |

The owner can retain confidential research inputs separately without placing them in every public report. This package cannot promise that any applicable law, contract, license, or request will never require disclosure. Preserve actual obligations and do not erase provenance to conceal where inputs came from.

The plugin's inspiration is a functional description; its implementation/rules/prompts are independently authored rather than copied from the referenced projects' source. That describes the authoring method and does not grant a legal guarantee or erase third-party materials deliberately incorporated later.

## Reconcile every artifact

Inventory code, vendored modules, generated source, dependencies, assets, schemas, tables/models, fixtures, docs, archives, installers, metadata, and history-bearing bundles. Review local git history/archive manifests if those will be distributed; excluding a file from the current working tree does not remove it from a history bundle.

Retain applicable notices/licenses for content actually incorporated or distributed. Do not auto-relicense the result because original code was not passed directly, a language changed, tests passed, or text similarity is low. Legal assessment remains an appropriately qualified review of the actual facts.

Audit current run, exact handoff/candidate, mandatory specification/corpus approvals and registered reviewer bindings, validation/environment/cases, incidents, dependency inventory, and implementation context. Raw approved corpora remain private reviewer inputs unless a separate distribution/notice review permits included independently authored cases. Build success, case parity, consuming-application integration, installation, deployed/runtime proof, and platform support are separate receipts.

## Report/export commands

```text
python3 scripts/ir.py audit RUN
python3 scripts/ir.py report RUN --output REPORT
python3 scripts/ir.py export RUN --dest DEST
```

Inspect generated files before making them public. Sanitized report export is a report artifact; it is not an automatic full source/package release. Prepare the independently written implementation and required notices separately in a new local destination without overwriting existing work.

Useful claims identify exact scope and conditions: "implemented from the reviewed behavioral contract"; "matched the accepted corpus on the recorded runtime"; "raw research inputs retained privately." Do not claim exhaustive equivalence, guaranteed independent authorship, model training purity, no infringement, or license freedom.

## Approval gate

Prepare local candidate files, proposed release notes/PR text, receipts, known limitations, and exact planned external action first. Creating/opening/submitting/publishing/marking ready a PR to a popular, high-visibility, or third-party upstream requires explicit user approval in the current conversation. An instruction to build a plugin or prepare a patch does not authorize that external action.

Do not send third-party messages, upload private evidence, or publish a release without authorization. Preserve dirty work and refs while producing the local candidate.

Return candidate inventory, private-material findings, retained notices, supported claims, unresolved limits, and publication action awaiting authorization if applicable.
