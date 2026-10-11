# Existing source exposure and honest reconstruction

Use this scenario when the user, parent agent, earlier session, or current model context already saw original source, tests, decompilation, architecture, internal tables, or an implementation plan. This is common in repair and reverse engineering; preserve the exposure rather than pretending it did not happen.

## Classify the actual work

| Exposure | Honest classification |
| --- | --- |
| Public interface documentation only | Documentation-based contract; runtime behavior may still be unobserved |
| Authorized executable/API outputs only | Black-box observations under stated environment |
| Source/decompiled code or original internal plan | Source-informed analysis/work |
| Upstream tests/fixtures seen | Test-source exposure with separate content/license provenance |
| Mixed inputs | Per-artifact mixed lineage; no universal source-unexposed claim |
| Model training history | Generally unknown; separate from declared session exposure |

Authorization to inspect/use an input is different from a claim the implementer did not see it. The process must preserve both facts.

## Two useful lanes

For ordinary source-informed engineering, implement authorized fixes/ports/replacements with accurate lineage, retained notices, and bounded claims. Do not label the work source-unexposed or automatically license-free.

For a new independent behavioral attempt, keep exposed analysts outside implementation. Collect appropriate observable evidence, write a declarative specification, perform an independent semantic firewall review, initialize a fresh run, seal a handoff, and launch an implementer with no inherited history or original access. The analyst's knowledge still exists privately; the controlled transfer must be inspectable and honest.

A description of a functional goal or an idea is not the same as receiving a protected implementation. Nevertheless, an already exposed author cannot retroactively prove they never saw an input. The plugin separates process facts from legal conclusions rather than promising that "cleanhousing" erases obligations.

## Common failure paths

- Parent sends a concise original architecture summary and calls it a behavioral specification.
- Copied upstream test code becomes the candidate's new test suite.
- Original helper names/control flow appear in a decompiled pseudocode handoff.
- Low text similarity is treated as proof that source-informed work became independent.
- Source-informed implementation is moved into a new folder/run and its exposure record disappears.
- New provider/model uses the source-exposed parent summary as its initial context.

Each path requires preserved lineage and firewall/incident review. Rewriting syntax, changing languages, or telling an agent to forget cannot reset exposure.

## Result

Return selected lane, actual exposure, accepted information boundary, preserved work, retained notices, fresh-context requirements if applicable, and claims the evidence supports. Keep confidential originals private while preserving traceability and applicable disclosure/distribution obligations.
