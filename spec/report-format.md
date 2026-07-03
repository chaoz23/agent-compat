# Report Format Specification

**Version:** pre-0.1 — OUTLINE ONLY, except §2: the no-single-score rule is already enforced by `runner/validate_report.py` and CI.

Structured output of a pairing run: per-scenario trajectories, friction points, repair metrics, distributions, provenance-weighted confidence (PRD R1, R3, R5, R6).

## 1. Envelope

<!-- Report id, spec version, runner version + backend, seeds, N runs, twin descriptors + conformance level annotation. -->

## 2. The no-single-score rule (R6) — NORMATIVE NOW

A report MUST NOT contain a top-level scalar compatibility score. There is no field for one; validation rejects any top-level numeric field whose name suggests one (`score`, `compatibility`, `match`, `rating`, and variants). Structural enforcement, not guideline.

## 3. Per-scenario results

<!-- Outcome distributions over N runs; trajectory references; friction points with transcript evidence; repair-attempt metrics. -->

## 4. Sycophancy diagnostics (R3)

<!-- Agreement-rate anomalies, position-shift tracking, suspicious-convergence flags. Rendered with the same prominence as findings. -->

## 5. Provenance and confidence (R5)

<!-- Tier-derived uncertainty widths; refusal of silent tier-mixing. -->

## 6. Transcripts and evidence

<!-- Evidence-annotation format linking every claim to trajectory locations. -->
