---
name: ir-protocol
description: Reconstructs observable state machines, ordering, retries, recovery, and negotiation for stateful protocols. Use explicitly for network services, session APIs, or persistence behavior.
disable-model-invocation: true
---
# Specify state and protocol behavior

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Pin protocol/version and authorized peer or oracle. Use an isolated environment with synthetic identities, messages, and persistent state.
2. Inventory public states, operations, responses, side effects, negotiation, deadlines, and recovery behavior. Distinguish a model inferred from traces from a documented protocol contract.
3. Observe sequences: successful paths, invalid order, duplicate delivery, retry, reconnect, timeout, partial failure, restart, cancellation, and concurrent interleavings.
4. Record traces with ordering, timestamps or logical clocks, seed, starting state, and environment. Redact credentials and private payloads before any approved export.
5. Specify observable transitions, invariants, idempotency, delivery semantics, and forbidden states. Leave internal state representation and synchronization design to the implementer.
6. Send protocol requirements through `check` and the firewall. Create adapter-based sequence cases for independent conformance validation.
7. Report bounded sequence coverage, remaining races, unsupported peers, and durability limits.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" observe "$RUN" --record "$PROTOCOL_OBSERVATION_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" check "$RUN" --spec "$SPEC_JSON"
```

## Return

Return public state/transition requirements, trace IDs, tested sequence classes, timeout and recovery semantics, inferred states, unsupported cases, and adapter needs.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
