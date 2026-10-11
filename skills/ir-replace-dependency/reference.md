# Integrate a replacement: reference

## Prove the intended consumer

Package compatibility includes imports, names, signatures, error semantics, asynchronous behavior, installation, optional features, platform binaries, and consumer expectations. A library-level pass does not establish a consumer workflow or installed package path.

## Keep the migration reversible

Record the original manifest/lockfile state and preserve dirty work. Integrate on an isolated branch or worktree when appropriate. Do not delete the original package, overwrite source, or remove notices as a shortcut. Use a controlled feature flag or adapter when that makes rollback concrete.

## Version honestly

Use a distinct candidate name and a documented compatibility range. Pin oracle and candidate versions in the report. Do not advertise complete support from a subset-specific reconstruction.

## Example

A consumer needs a parser's streaming API, although scalar parse cases passed. Add streaming behavior to the scope, observe chunk boundaries and errors, review the new contract, then validate the consumer's real import and streaming workflow. Record scalar corpus and consumer proof separately.

## Distribution evidence

A release inventory lists authored candidate files, approved contract artifact, own dependency notices, private evidence excluded, and unresolved obligations. A technical report can support a review; it cannot resolve distribution rights by assertion.

Never create or open a public upstream pull request without the user's explicit approval in the current conversation. A local branch, proposed patch, and PR text remain preparatory artifacts.
