---
name: ir-dependencies
description: Inventories npm, Python, Cargo, and Go manifest dependencies and prioritizes authorized reconstruction candidates without assuming a complete license audit. Use explicitly for dependency scanning and replacement planning.
disable-model-invocation: true
---
# Inventory replacement candidates

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Identify manifests and lockfiles within the authorized repository scope. Preserve existing files and dirty work; do not fetch package sources automatically.
2. Run `scan` on each supported manifest. Inspect ecosystem, declared versions, direct/transitive distinction, registry or path origin, optional features, and unsupported syntax.
3. Reconcile scan output with lockfiles and actual consumers using an authorized inventory. A declaration scan alone does not establish resolved versions, transitive completeness, or license terms.
4. Group candidates by required public surface, usage frequency, maintenance need, integration risk, size, and available oracle evidence. Select a narrow replacement with concrete acceptance criteria.
5. Record dependency origin and existing notices privately. Preserve any obligations until an appropriately grounded review determines the candidate's own distribution terms.
6. Start a dedicated reconstruction run for each selected target/version. Shared requirements and caches require digest-based validity and explicit provenance.
7. Return an inventory and staged plan. Do not replace manifests, remove notices, or publish packages based solely on the scan.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" scan "$MANIFEST"
```

## Return

Return supported manifests, declared dependencies, resolution gaps, candidate priorities, consumer surface, required evidence, and a proposed replacement run per selected version.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
