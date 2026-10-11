# Compilers, interpreters, and virtual machines

Use this scenario for language implementations, bytecode tools, interpreter replacements, compiler reconstruction, and compatibility adapters. Source parsing, emitted bytes, runtime semantics, ABI behavior, and external tool integration are separate acceptance scopes.

## Establish the public contract

Record authorized language/interface documentation, original/version digest, supported grammar/features, type/coercion rules, runtime/ABI/environment, public format/wire tokens, diagnostics categories, resource bounds, and unsupported constructs.

Independently author synthetic programs that distinguish observable semantics: literals, operators, control flow, functions/closures if scoped, types, errors, exceptions, module loading, state, recursion, encoding, numeric limits, optimization-sensitive behavior, and runtime effects.

Copied upstream language/compiler tests, original fixtures, diagnostic paragraphs, decompiled passes, private IR/type architecture, internal opcode tables, and original code-generation plans remain private source-informed evidence. A mandated instruction/format constant may be transferable only through necessity/provenance review.

## Requirement matrix

| Claim | Needed evidence |
| --- | --- |
| Accepted syntax | Independently authored valid/invalid programs under supported grammar |
| Type/runtime behavior | Executed results, errors, and effects under recorded environment |
| Byte-exact compiler output | Explicit byte representation equality for accepted programs |
| Semantic equivalence | Runtime observable results under a faithful reviewed executor |
| ABI compatibility | Independent caller/callee integration receipts |
| Tool integration | Actual accepted downstream tool/runtime behavior |
| Debug/metadata compatibility | Explicit required fields/ordering and privacy review |

A differing binary can be semantically compatible; identical output for a small corpus does not prove all-language reconstruction. Define the actual required claim instead of equating these scopes.

## Independent architecture

The implementer gets the reviewed declarative contract and synthetic program descriptions, not a summarized original parser/pass/IR architecture. It chooses lexer/parser, intermediate representation, evaluation, code generation, and optimization architecture independently.

Undefined/unspecified behavior must remain explicit. Do not infer a required optimization or original control-flow structure from one observed output. Unknown diagnostics can be represented as reviewed categories unless exact wording is specifically necessary and reviewed.

## Conformance

Use analyst-side adapters to compile/interpret accepted cases and emit reviewed results as JSON. Pin original/candidate/compiler/runtime/toolchain, optimization flags, locale, filesystem behavior, seeds, and time limits. Keep synthetic source programs independently authored and raw compiler logs private.

The built-in validator does not sandbox execution or provide exhaustive grammar/fuzz coverage. Untrusted generated programs, crash inputs, external integration, and resource stress require appropriate isolated runners and separate authorization. Do not add/run filesystem test suites before the application is complete where the user's constraint applies.

Report supported features, actual corpus/environment, byte versus semantic/ABI results, downstream integration proof, diagnostics/resource limits, notices, and unobserved features. Source-informed reconstruction remains honestly classified; different syntax or low similarity is not a legal independence result.
