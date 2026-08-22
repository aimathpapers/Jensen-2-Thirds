# Start here: Jensen two-thirds referee packet

This packet is organized for mathematical review rather than repository
archaeology.

1. Read `DISCLOSURE/TRUST_BOUNDARY.md` and
   `DISCLOSURE/KNOWN_LIMITATIONS.md`.
2. Read `PAPER/JENSEN_TWO_THIRDS_MAIN.pdf`; use the technical supplement for
   computation, formalization, and provenance details.
3. Use `FORMAL/THEOREM_MAP.md` to move from a paper claim to Lean,
   exact/interval evidence, and the remaining boundary.
4. Consult `SUPPORT/phase21/` for the full moving-saddle/contour proof and
   `SUPPORT/phase20/` for the imported-architecture firewall.
5. Run `python3 VERIFY_BUNDLE.py`, `python3 VERIFY_ANCESTRY.py`, and then the
   extraction-local commands in `REPRODUCE/EXPECTED_RESULTS.md`.

The main theorem is a two-thirds growing-degree hyperbolicity wedge for the
Jensen polynomials of Riemann's xi coefficients. It is not the Riemann
hypothesis. The Lean theorem is conditional on xi-specific analytic inputs;
the uniform saddle and contour analysis remains in the paper.

All reviews available in this project are AI reviews, not human or peer
review. The public article is explanatory material and not part of the proof.
