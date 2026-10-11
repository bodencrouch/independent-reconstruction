# Identify boundary failures

| Failure | Guardrail | Remaining limit |
| --- | --- | --- |
| Prior source in conversation | New context and sealed launch packet | Context freshness is attested |
| Source mounted in shared workspace | Bubblewrap or separate VM | Kernel and runtime mounts trusted |
| Analyst copies internal algorithm into prose | Restricted schema, screen, independent review | Semantic leakage needs judgment |
| Copied tests disclose code or expression | Original reviewer-side cases | External values may still need rights review |
| Source arrives through network/MCP/search | Implementer hook denial and no-network sandbox | Hosted tools outside hook coverage |
| Session memory, plugins or hidden instructions | Minimal fresh host profile | Host and opaque model internals trusted |
| Package manager downloads reference | No network and controlled toolchain image | Preinstalled caches must be inventoried |
| Symbolic link crosses candidate root | Snapshot and hook path checks | Same-user races require VM ownership boundaries |
| Model's training includes target | Training exposure recorded unknown | Tooling cannot inspect opaque training |
| Hook disabled, role env changed or tool bypass | Sandbox and owner-controlled policy | Hooks alone are advisory enforcement |
| Arbitrary patch writes multiple paths | Deny broad tools unless structured paths reviewed | Host wire formats can change |
| Audit files rewritten by owner | Chained hashes, content-addressed artifacts | External anchor not implemented |
| Conformance answers overfit corpus | Held-out cases and independent adapter review | Complete equivalence not proved |
| Candidate edited after measurement | Tree hash and stale report | Dynamic dependencies not fully captured |
| Sensitive provenance published | Explicit public report allowlist | Required notices need separate review |
| Similarity score treated as clearance | Reports never declare legal clearance | Counsel/legal analysis outside package |

Containment records are facts, not accusations. Preserve contaminated work privately,
mark it unfit for independent implementation claims, and rebuild in a fresh run.
Deletion of logs or source is not a remediation strategy.

For strong adversarial separation use different users/machines, distinct credentials,
minimal signed runtime images, a reviewed broker, independently anchored audit heads,
and bounded role output channels. Those are deployment recipes. This release supplies
local artifact controls and an offline Linux sandbox, not remote attestation.
