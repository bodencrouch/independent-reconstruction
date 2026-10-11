# Numerical and scientific software

Use this scenario for numerical libraries, scientific solvers, tensor APIs, automatic differentiation, signal processing, and numerical compatibility layers. The goal is an explicit mathematical/runtime contract with independently selected algorithms and bounded comparisons.

## Scope inventory

| Area | Required distinctions |
| --- | --- |
| Numbers | Integer/float widths, rounding, overflow, signed zero, finite/nonfinite handling |
| Arrays | Shape, layout, broadcasting, strides, mutation/aliasing, empty values |
| Operations | Domain boundaries, singularities, stability, accumulation order |
| Gradients | Differentiability conditions, shape, higher-order behavior if supported |
| Runtime | Device, kernel/runtime version, precision mode, determinism, threads |
| Failure | Invalid shape/type/device, resource limits, cancellation |

Observe independently authored synthetic cases, analytical identities, numerical invariants, and finite-difference checks where authorized. Label an invariant result separately from oracle parity. Agreement with the original does not establish mathematical correctness if both share an error.

## Data and implementation boundary

Original numerical kernels, pass structure, internal buffer/graph architecture, copied test code, tables, weights, training data, and proprietary scientific inputs retain their own provenance and distribution constraints. Do not assume that translating a tensor library permits copying its model data or constants.

Approve externally required mathematical constants and interface tokens individually. Specify mathematical effects, accepted precision, supported dtypes/devices, determinism, aliasing, and errors without transferring original implementation prescriptions. The implementer chooses algorithms and numerical libraries independently.

## Comparison policy

Define absolute/relative error limits before validation and justify them by accepted behavior, magnitude, dtype, and problem conditions. An aggressive tolerance that hides a required discontinuity or boundary difference is not conformity. Track residual/error distributions when relevant through an independently designed external runner.

The built-in `numeric` mode compares scalar finite JSON numbers. It does not recursively compare tensors, NaN/infinity, gradients, distributions, sparse layouts, or devices. A reviewed adapter can encode richer semantics into exact JSON or a scalar metric with an explicit accepted contract, but that encoding and reduction require their own fidelity review.

Seeds, device/runtime, thread count, precision modes, input generation, and nondeterministic permitted outputs must be recorded privately. Benchmark timing/performance claims require separate scoped measurement; the runtime's per-process elapsed time is not a statistical performance benchmark.

## Deliverable

Provide supported mathematical/runtime contract, scoped operation/dtype/device matrix, conformance/invariant evidence, numerical tolerances, reproducibility conditions, model/table/dependency provenance, and unknown gradients/performance/platform behavior. Do not claim total framework replacement from a limited operation set or legal independence from low textual similarity.
