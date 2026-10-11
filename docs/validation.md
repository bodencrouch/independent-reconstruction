# Record the package checks

The package was checked locally after all initial components were implemented.
No filesystem test suite was added. Checks used inline Python, temporary synthetic
workspaces, real CLI commands, direct hook JSON and a bubblewrap process.

## Observe the results

| Check | Result | Claim supported |
| --- | --- | --- |
| Runtime and syntax checks | 59 passed | Local CLI lifecycle and selected failure handling |
| Differential counter example | 3 cases passed | The synthetic adapters matched that corpus |
| Linux bubblewrap checks | 6 passed | Sealed files readable/read-only, candidate writable, host home/private run/unsealed files absent |
| Hook adapters | 31 cases passed | Cursor, Claude and Codex wire decisions in direct invocation |
| Passive bootstrap | 5 cases passed | Inactive contexts emit neutral output even without Python on PATH |
| Project installer | 4 initial scenarios and 8 final checks passed | Three hosts, dry run, preservation, 54 links, exact repeat, three private backups and collision rejection |
| Hook consistency follow-up | 20 cases passed | Canonical roles, aliases, duplicate JSON rejection, typed versions and sealed prompt hashes |
| Manifest inventory | 5 manifests passed | 10 declarations in npm, Cargo, PyPI and Go examples; no resolution/network |
| JSON schemas/examples | 13 checks passed | Draft 2020-12 schema validity and valid synthetic examples |
| Component metadata/links | Passed | 18 skills, 9 agents, 27 commands, 8 rules, 17 scenario guides and native hook paths |

Runtime checks exercised registered evidence and reviewer context, contract leak
screening, wrong review digests, exact corpus review, missing acceptance coverage,
distinct adapter commands, candidate artifact references, duplicate session IDs,
duplicate JSON output keys, timeouts, large numbers, changed candidate snapshots,
protected output paths, symlinked candidate denial, probes, resume and quarantine.

The sandbox used `--unshare-all`, an empty home, read-only runtime mounts and an
allowlist of sealed files. It succeeded on this host. Network isolation was configured
by bubblewrap; no external model/provider operation was attempted. Six filesystem
observations were made inside the process. The temporary fixtures were removed.

Hook checks used synthetic payloads, not a host chat session. See
[integration receipts](../integrations/VALIDATION.md) for details. Installation
does not prove hook activation or trust. Actual Codex/Cursor/Claude loading and
fresh end-to-end model orchestration remain unverified in this release.

The synthetic reviewer and implementer records exercised schema and ordering;
they do not represent independently run AI implementations or authenticated identities.
The reference/candidate adapters were written for the check. No third-party source
or live application was reimplemented. These results establish local package behavior,
not production scale, full compatibility, independent authorship or legal clearance.

## Reproduce the receipts

Use `scripts/ir.py --help` and docs/quickstart.md for the lifecycle. For negative
cases, change a digest, omit a declared acceptance case, alter a measured candidate,
or replace a candidate directory with a symlink in a disposable synthetic run.
The expected result is exit 2 with a rejected, stale or quarantined status. Preserve
real user work; use temporary fixtures for these demonstrations.

Use `scripts/install.py --project SYNTHETIC_PROJECT --host all --dry-run`, then
install twice and verify unchanged settings bytes and private backups. Invoke
hooks/entry.sh with host/event and a synthetic JSON stdin payload to inspect the
adapter without claiming native host loading. Use scripts/bundle.py to build a
distribution and inspect BUNDLE-MANIFEST.json for excluded private/runtime paths.

Personal skill installation created 18 symlinks in the shared user skill directory.
Discovery in a newly refreshed host session remains distinct from filesystem installation.
The runtime needs only Python standard-library modules; optional schema checks used the
system jsonschema package with user-site packages disabled because the user-site copy
was missing its rpds dependency. No environment packages were installed or changed.
