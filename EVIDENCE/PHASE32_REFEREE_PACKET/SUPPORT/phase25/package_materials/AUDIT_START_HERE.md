# Start here: Jensen two-thirds full audit archive

This archive contains the referee packet plus the complete relevant source
snapshot, phase notes, exact outputs, mutations, AI review history,
environment records, and an offline Git history bundle.

Begin with the same paper and trust-boundary documents as a referee. Then use:

- `AUDIT/repository/ground_zero_work/phase25/PHASE25_STATUS.md` for the
  chronological verification campaign;
- `AUDIT/repository/ground_zero_work/phase25/reviews_phase_l/` for unedited AI
  reports, scripts, and author dispositions;
- `AUDIT/repository/reproduce/VERIFY_ALL.sh` for the authoritative serial
  repository verifier;
- `AUDIT/CANDIDATE_HISTORY.bundle` for an offline reconstruction of the exact
  candidate and its checkpoint ancestry.

Run the extraction-local checks in `REPRODUCE/EXPECTED_RESULTS.md` before
using any evidence. The `quick` and `full` modes reconstruct the repository
from the included history bundle in a private temporary directory. They do
not depend on a private checkout outside this archive.

Third-party papers are indexed by official location, exact version, consumed
statement, and hash rather than redistributed without permission. All review
is AI review, not human or peer review.
