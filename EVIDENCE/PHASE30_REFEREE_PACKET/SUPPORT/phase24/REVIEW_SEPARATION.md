# Review separation and conflict-of-interest protocol

The Phase-24 review packets identify the candidate by an immutable source
commit. A first-pass reviewer should receive only:

- the unified manuscript and relevant proof/source files;
- the exact/numerical verifier scripts and environment locks;
- primary-source hashes and retrieval instructions;
- the appropriate analytic or algebraic packet.

Do **not** include prior verdicts, author responses, finding dispositions, or
the other reviewer's report in a first pass. Reviewers must reconstruct high-
risk calculations from definitions and must not use packet-generated
symbolic outputs as independent inputs.

Any AI system used for this purpose must be identified as an AI reviewer.
Its report is an AI pre-review, not human review and not peer review. The
review report should disclose model/provider, tools, access to prior work,
any relationship to the authors, and whether its scripts were independently
entered.

Document separation is not sufficient if the reviewer retains prior-review
context. A first-pass reviewer must also disclose whether the same model or
session reviewed an earlier freeze. If it did, classify the result as a
correlated re-review, not a separated first pass. Use a different provider or
a genuinely context-free session for the next separated gate.
