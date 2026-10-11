# Inventory replacement candidates: reference

## Understand scan scope

A manifest scanner identifies declarations in formats it supports. It is not a package resolver, software bill of materials generator, source fetcher, vulnerability database, or authoritative license service unless separately documented and executed as such.

## Reconcile ecosystem details

- npm: package.json ranges, package lock, aliases, workspaces, peer/optional dependencies.
- Python: pyproject/project metadata, requirements files, markers, extras, editable/path entries.
- Cargo: dependency tables, features, target-specific dependencies, renamed crates, path/git origins.
- Go: module requirements, replacements, workspaces, pinned sums, indirect dependencies.

Pin selected target versions and their oracle artifacts. Record unsupported constructs rather than inventing resolved packages.

## Prioritize by actual use

Start with the public operations consumers invoke. A small exported surface may still hide complex runtime or platform semantics. Avoid claiming a full-package replacement when only the consumer's subset is reconstructed.

## Example

A project calls two functions from a utility package. The plan targets those functions and their observed errors in a consumer-specific replacement. It preserves the old dependency until the candidate's integration evidence is complete. A later run can broaden the supported public surface.

## Keep obligations visible

Track licenses, notices, source availability requirements, and unresolved legal questions independently from behavior. A new implementation, changed language, or passing comparison does not authorize erasing a preexisting notice record.
