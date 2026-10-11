# Define the run boundary: reference

## Capture the brief

Use these fields in a human review brief; serialize machine records according to the package schemas.

- Target: identity, exact version, artifact digest, executable environment.
- Outcome: interfaces and workflows the candidate must support.
- Access: authorized oracle, documentation, source, binary, and network channels.
- Exposure: what each participant has already seen; include supplied conceptual references.
- Isolation: separate process/workspace, available sandbox, shared tools, and network policy.
- Acceptance: required cases, application integrations, performance bounds, excluded behavior.
- Disclosure: public artifact contents, private evidence retention, known notices, approval gates.

## Avoid silent scope changes

A request to replace a dependency authorizes local preparation within the requested repository. It does not automatically authorize sending private source to a hosted model, querying an account with side effects, changing an upstream license notice, or opening a public upstream pull request.

Record a change to the target version, supported interface, authorized evidence channel, or implementation exposure as a new scope decision. Reassess existing approvals and cached results.

## Example

Target: a versioned CLI that transforms JSON records. Required scope: stdin/stdout behavior, exit status, documented flags, Linux execution, and one consumer integration. Excluded scope: its original internal modules and undocumented performance optimizations. Oracle calls use synthetic records. Source-assisted analysis is available only to the collector.

If the original source is already present in the implementing agent's context, record that exposure. Use a different fresh participant for the clean-room lane; retain the existing work as an explicitly exposed lane when useful.

## Initialize the actual run

`init RUN --target NAME --language LANGUAGE` records the target identity and chosen implementation language. Add `--source-root ABSOLUTE_PATH` for each authorized source directory that must stay outside the implementation lane. Registration is an access boundary declaration; it does not mount, clone, inspect, or authorize the source. A supplied conceptual brief remains a known exposure even when no source repository was examined.
