# Measure resource behavior: reference

## Define the requirement first

Functional output compatibility and resource behavior are distinct. A candidate may produce the right output while violating memory, latency, streaming, or cancellation requirements. Conversely, faster execution does not establish correct output.

## Control the environment

Record CPU/architecture, memory, operating system, runtime/toolchain, build settings, power mode, storage, warm/cold cache, network dependencies, background load, seed, and input size distribution. An unavailable or unstable environment limits the claim.

## Measure failure behavior

Include bounded input size, overload, timeout, cancellation, exhausted resources, and recovery if these are in scope. Hostile workloads need a suitable operating-system boundary and caps. A timeout is a failed or inconclusive measurement, not proof of correctness.

## Use honest statistics

Define warmup and repetition counts, retain samples, report variability, and disclose exclusions. Distinguish total latency, service time, and throughput. Avoid a single best run or an aggregate hiding catastrophic tail behavior.

## Example

The acceptance contract requires processing a defined record stream within a memory bound while preserving outputs. The collector measures public behavior under pinned inputs. The implementer chooses its own buffering design. The validator reports output conformance and memory evidence separately.

No requirement should prescribe the original cache layout, allocation pool, or optimization algorithm solely because those details appear in source.
