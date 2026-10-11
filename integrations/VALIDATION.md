# Integration receipts

Recorded after the package's main implementation on 2026-10-10. All inputs were synthetic and temporary. Validation used inline Python and actual adapter/installer subprocesses; no filesystem test suite or persistent test files were added.

| Check | Receipt |
| --- | --- |
| Python hook and installer modules parsed | 10 |
| Direct adapter wire cases | 31 passed |
| Owner-private hook records inspected | 27 |
| Shell bootstrap cases with Python unavailable in PATH | 5 passed |
| Project installer scenarios | 4 passed |
| Files installed in the observed package snapshot | 277 |
| Skills linked across three hosts in that snapshot | 54 |

Adapter cases covered passive sessions, sealed specification reads, candidate writes, restricted source denial, shell/MCP/delegation/unknown tool denial, unapproved prompts, Codex patch paths and move escape denial, unsealed extra-file denial, and denial of a broadened read-root policy. Outputs and private receipts were checked for synthetic path and prompt leakage.

Installer scenarios covered a mutation-free dry run, installation preserving unrelated host settings and AGENTS.md, an unchanged repeat with zero new files/links/config merges and byte-identical settings, and collision rejection preserving settings. Three pre-existing host configurations received exact backups with mode 0600. Private and runtime directories were absent from the installed snapshot. Inventory counts describe the observed snapshot and can grow with later package changes.

The shell bootstrap emitted valid neutral responses without Python for inactive sessions. Python and POSIX sh were available in the local execution environment; hook entry scripts are executable.

These are direct protocol and installer receipts. Native host discovery, exact hook trust, plugin activation, host version compatibility, hosted inference, and real host event delivery were not exercised. No result in this file certifies OS isolation, application conformance, copyright independence, or license eligibility.

## Final consistency receipts

After the runtime standardized its role names and sealed launch instruction, 20 additional inline cases passed: all nine canonical roles, four legacy hook aliases, three duplicate-key JSON rejections, two boolean schema-version rejections, and two prompt cases (the runtime's exact sealed launch instruction allowed; an altered instruction denied). Hook policy and manifest parsing reject ambiguous duplicate keys without echoing their names or contents. New instructions require a reviewed amended handoff/run; manually changing policy invalidates the run's recorded policy digest.
