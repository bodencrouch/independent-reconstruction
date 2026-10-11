---
name: ir-performance
description: Defines observable resource, latency, throughput, and failure constraints with controlled comparison environments. Use explicitly when performance or bounded resource behavior is part of reconstruction acceptance.
disable-model-invocation: true
---
# Measure resource behavior

Resolve this `SKILL.md` real path; the package root is `Path(SKILL_PATH).resolve().parents[2]`. Set `PLUGIN_ROOT` to that directory and `RUN` to the private run path used by the controller. These variables are examples, not built-in host variables. Execute only commands authorized for this stage. Use package schemas for machine records; preserve unrelated work.

## Workflow

1. Confirm performance is an explicit compatibility requirement or user-requested comparison. Define workloads, hardware/runtime, resource caps, warmup, repetitions, and allowed variability before measurement.
2. Pin oracle and candidate artifacts and relevant toolchain settings. Use identical approved inputs and record caches, persistent state, background activity, and external services.
3. Observe public resource behavior: completion time, throughput, peak memory, allocation limits, concurrency, cancellation, and response to overload. Keep original optimization techniques restricted.
4. Specify only justified resource requirements and tolerances. Preserve fresh implementation design freedom.
5. In an authorized validation phase, run the agreed controlled measurements through suitable adapters. The basic conformance runner alone does not certify resource behavior.
6. Investigate outliers and failed runs separately. Do not discard unfavorable samples without an agreed reason or compare mismatched environments as if controlled.
7. Report the measured environment, workloads, samples, variance, limits, unsupported workload classes, and effect on acceptance.

## Execute

```bash
python3 "$PLUGIN_ROOT/scripts/ir.py" observe "$RUN" --record "$PERFORMANCE_OBSERVATION_JSON"
python3 "$PLUGIN_ROOT/scripts/ir.py" audit "$RUN"
```

## Return

Return workload/environment digests, measured samples, resource thresholds, failure counts, variance, justified acceptance decision, and unmeasured behavior.

Read [reference.md](reference.md) for the decisions, boundaries, and examples used by this skill.
