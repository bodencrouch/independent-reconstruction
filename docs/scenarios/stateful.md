# Stateful, asynchronous, and concurrent systems

Use this scenario for stores, queues, agents, transactional APIs, network sessions, background services, and other components whose output depends on operation history. Stateless happy-path parity does not establish compatibility for these systems.

## Observable model

Record initial conditions, reset/restart behavior, public handles, allowed operations, observable states, side effects, error transitions, cancellation, retry, idempotency, visibility, and durability. Independently name logical handles in synthetic traces; do not transfer original internal object IDs, queue structures, state classes, or helper names.

Describe state requirements as externally observable relations. For a store, a successful acknowledged write followed by an authorized read may establish one visibility condition; crash recovery, simultaneous clients, and replica behavior are additional requirements requiring their own evidence.

## Distinguishing sequences

| Sequence | Question |
| --- | --- |
| Create → read → update → read | What does each operation make observable? |
| Fail operation → retry → inspect | What survives failure and retry? |
| Start → cancel → inspect | Which effects occurred before cancellation? |
| Write → restart → read | What durability condition is supported? |
| Duplicate request → inspect | Is duplicate handling idempotent under these conditions? |
| Concurrent operations → observe | Which orders/results are permitted? |
| Disconnect → reconnect → inspect | How does session recovery behave? |

Use disposable synthetic state and explicitly controlled scheduling where possible. Repeat only where variability affects an accepted requirement. Distinguish directly observed outcomes, inferred allowed sets, and unknown interleavings. An absence of a race in a small sample does not prove the race impossible.

## Contract and implementation

Specify legal operation sequences, observable invariants, failure boundaries, nondeterministic permitted outcomes, reset semantics, and unsupported combinations. A source-informed internal state machine must not become the implementer's design through paraphrase.

The implementer selects its own state representation, transaction/scheduling architecture, and dependencies. Questions return as requirement IDs; source-informed coordinator feedback stays outside implementation until a new reviewed handoff exists.

## Runtime comparison limits

The built-in validator starts fresh processes per case. Encode one bounded sequence into each input and let a reviewed adapter execute it, emit observable results, and clean up state. This can cover local sequential semantics, but does not automatically exercise distributed deployments or adversarial concurrency.

Exact JSON comparison preserves array order. Permitted unordered outcomes, trace partial orders, or repeated sampling need an independently designed comparator/adapter and approved policy. Do not sort away a real ordering requirement. Distributed crash/load scheduling, persistence verification, and process/network isolation need external tooling with recorded receipts.

Report accepted transition and sequence coverage, observed scheduling, durability conditions, untested interleavings, resource limits, and deployed behavior separately. No finite trace set establishes all-state equivalence or absence of concurrency bugs.
