# Clinical actions: focused review development package

**Status: interim critical evidence map, not a completed systematic review or submission-ready manuscript.**

Main question: what empirical evidence supports safe execution of clinical or care-access actions by LLM-based agents, and which safety obligations have actually been evaluated?

The frozen amendment narrows the previous broad review. Discovery produced 2,877 query occurrences, administratively linked into 2,397 candidate groups; no independent human screening has been completed. The 23-report synthesis is a provisional purposive map. It adds seven primary safety/workflow reports, retains actual endpoint definitions, and compares existing frameworks before treating CAA as an analytical checklist. The original draft remains in the parent directory and Git history.

## Deliverables

- `outputs/Clinical_Action_Evidence_Review.pdf`: focused IEEE-style paper.
- `outputs/Clinical_Action_Review_Supplement.pdf`: search/status and report-level evidence notes.
- `outputs/Clinical_Action_Review_Workbook.xlsx`: full occurrence register and separate independent reviewer decisions; no fabricated judgments.
- `outputs/Clinical_Action_Review_Overleaf.zip`: self-contained LaTeX, bibliography, vector figures and supplement.
- `protocol/`: frozen protocol and searches requiring author access.
- `searches/`: exact executed queries, metadata exports and API logs.
- `screening/`: administrative candidate linkage and complete unscreened worklists.
- `evidence/`: primary metadata, reading-access hashes and provisional report extraction.
- `novelty/framework_crosswalk.csv`: prior-work overlap and limits.
- `audit/`: decision log, build verification, workbook decision tests and visual checks.

## Rebuild

From this directory, run `python scripts/build_worklists.py`, `python scripts/build_focused_evidence.py`, `python scripts/prepare_manuscript.py`, `python scripts/make_figures.py`, `python scripts/make_supplement.py`, then `python scripts/build_pdfs.py`. The snapshot build does not require rerunning live discovery. Dependencies: Python 3, matplotlib, pypdf, TeX Live/latexmk and IEEEtran files supplied with attribution in the parent package. Workbook authoring uses the documented `@oai/artifact-tool` runtime; the CSV worklists remain portable without that runtime.

## Required before systematic-review submission

Execute and log the remaining database searches with appropriate access; obtain librarian PRESS review; independently screen all candidates and verify extraction; adjudicate study families and versions; obtain blocked full text; apply design-appropriate appraisal with clinical expertise; freeze final inclusion set; regenerate all results and reporting flow. Complete journal fit and current indexing/quartile checks, author identity/affiliations, contributions, conflicts, funding and AI disclosures. Do not invent any completed step or infer safety from benchmark success. No journal submission was authorized or made.

Licensed reading copies, abstracts and patient data are not redistributed. Metadata, original analytical notes, process logs, figures and software are available for audit. These artifacts cannot guarantee acceptance by a Q1 journal.
