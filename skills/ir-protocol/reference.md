# Specify state and protocol behavior: reference

## Model observable states

Define states by behavior visible to a caller: disconnected, negotiated, authenticated, transaction open, committed, aborted, or another justified public condition. Do not replicate private enum names or internal state decomposition solely because source exposes them.

## Specify invariants

Examples include a duplicate request returning the prior result, a reset clearing a documented session property, a commit becoming durable before acknowledgement, or an invalid message leaving state unchanged. Each requires evidence and explicit environmental assumptions.

A single response test cannot establish sequence behavior. The validation adapter needs deterministic starting state, a sequence of actions, expected responses, and observable state checks. Logical time or an approved clock adapter can make timeout behavior reproducible.

## Observe failure boundaries

- Disconnect before request, after request, and after response.
- Duplicate message with the same and a different request ID.
- Negotiation with unsupported versions or optional capabilities.
- Restart around a durable operation.
- Partial writes, malformed frames, and cancellation.
- Interleavings under a recorded scheduling policy.

## Keep the feedback boundary

A protocol mismatch returns a reviewed message sequence and expected public transition. Private storage keys, source stack traces, implementation locks, and original retry loops stay in the restricted lane.

## Completion evidence

Report sequence families, version matrix, state coverage, known timing assumptions, durable/restart checks, and unresolved races. A simulator pass supports the simulator environment; label live-peer interoperability separately.
