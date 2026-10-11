# Agentic AI in healthcare: research and manuscript
**From Clinical Reasoning to Authorized Action: A Critical Review of Agentic AI in Healthcare and a Clinical Action Assurance Framework**

An AI-assisted critical review draft with an action-centered evidence map, proposed Clinical Action Assurance (CAA) framework, original vector figures, IEEE-style LaTeX, compiled PDFs, and a synthetic action-gate reference implementation.

Literature cutoff: 10 October 2026. Metadata refresh/rebuild: 11 October 2026. This is a purposive critical integrative review, not a systematic/scoping review. Author identity, independent clinical verification, complete bibliographic checks, and final journal requirements must be confirmed before submission. Acceptance and current Q1 classification are not guaranteed.

## Contents
- `manuscript/`: LaTeX, bibliography, original figures/tables.
- `research/`: protocol, discovery metadata, evidence/claim registers, audit and journal fit.
- `scripts/`: reproducible retrieval, figures, compilation, synthetic invariants, validation.
- `outputs/`: main manuscript, supplement, and portable submission archives.
- `submission/`: author completion and submission checklist; unsent cover letter draft.

## Reproduce
Install Python dependencies in `requirements.txt` and TeX Live with IEEEtran, latexmk, lmodern, and Poppler. Run `make all`, `make test`, then `make validate`. Network retrieval is separate: `make search` and `make references`; rerunning retrieval creates a new snapshot and can change counts. Original publisher PDFs/abstracts and patient data are excluded from this public repository.

## Status
Rebuilt sources are committed incrementally after an interrupted upload. See `research/audit/recovery.md` for provenance. Synthetic software checks illustrate invariants and do not validate clinical use. No external journal submission has been performed.
