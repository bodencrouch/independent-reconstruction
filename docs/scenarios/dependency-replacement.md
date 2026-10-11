# Dependency replacement across ecosystems

Use this scenario for reducing or replacing selected dependencies in npm, Python, Rust, Go, or another ecosystem supported by a reviewed adapter. The task is a set of behavioral reconstructions and integration changes, not an automatic license-removal operation.

## Inventory

`python3 scripts/ir.py scan MANIFEST` reports declared dependencies for supported manifest formats. It does not download or execute packages, resolve every transitive version, determine the full license graph, or prove which APIs the application uses.

Reconcile manifests against lockfiles, workspace members, vendored directories, optional/peer/dev/build groups, target-platform conditions, runtime imports, plugin loading, dynamic entry points, and installation scripts through bounded authorized inspection. Record scanner limitations and unsupported formats.

## Select lanes

For each candidate replacement, record dependency/version, required consumer behavior, integration surface, authorization/exposure, notices, and acceptance criteria. Prioritize actual needed behavior while stating omitted exports/features.

Give each independently scoped package/version a separate private run and fresh handoff. Dependencies between replacements must be explicit contracts. Do not pass one source-exposed analyst's summaries into another lane's implementer.

Do not assume a replacement is independent if it imports the original transitively, vendors its tables, includes its generated files, or preserves source-derived fixtures. Inventory new dependencies as carefully as removed ones.

## Workflow

1. Observe the relevant public API behavior with synthetic consumer inputs.
2. Create a reviewed specification and sealed handoff for the lane.
3. Implement from a fresh restricted context and record independently selected dependencies.
4. Conform the accepted behavior when authorized.
5. Prepare consumer manifest/import changes in isolated preserved work; review lockfile effects and conditional features.
6. Record consumer integration and deployment separately from library-level case agreement.

Upstream test code can be analyst-side evidence only when authorized and classified. Its code/license cannot be silently laundered into the replacement's test suite or implementation. Independently author transferred cases from approved behavior.

## Deliverable

Provide a reconciled dependency inventory, completed lane receipts, selected replacements, actual consumer edits, retained notices, unsupported behavior, and remaining transitives/platform unknowns. Removing a manifest entry does not establish removal of every dependency obligation, runtime path, or included third-party artifact.
