import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R.parent
def esc(s):
 for a,b in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('_',r'\_'),('#',r'\#'),('$',r'\$')]:s=str(s).replace(a,b)
 return s.replace('≤',r'$\leq$').replace('−',r'$-$')
reports=json.loads((R/'evidence/focused_reports.json').read_text());queries={**json.loads((P/'research/searches/queries.json').read_text()),**json.loads((R/'searches/queries_v2.json').read_text())}
parts=[r'''\documentclass[journal,onecolumn,10pt]{IEEEtran}
\usepackage[T1]{fontenc}\usepackage{lmodern,booktabs,longtable,array,graphicx}
\usepackage[hyphens]{url}\usepackage[hidelinks]{hyperref}
\setlength{\emergencystretch}{3em}\Urlmuskip=0mu plus 1mu
\title{Supplementary Research Record: Clinical Action Evidence Review}
\author{Interim development package; independent screening and appraisal pending}
\begin{document}\maketitle
\section{Status and count definitions}
The cutoff is 10 October 2026; the supplementary retrieval occurred on 11 October UTC. A protocol amendment was frozen after exploratory work, not prospectively preregistered. There are 2,877 retrieval occurrences, 2,397 administrative candidate groups and 480 linked repeat occurrences. Exact DOI/title/database-ID linkage is not scientific study-family deduplication. No independent human eligibility decisions have been recorded. The main paper's 23-report map is purposive and provisional, not a completed systematic inclusion set.
\section{Executed queries}
Exact strings follow. Crossref queries use a relevance-ranked limit of 200 each and publication-date filters from 2022-01-01 through 2026-10-10; they are not exhaustive. Europe PMC overlaps PubMed and preprint indexes. Full API URLs, date semantics, reported totals, retrieved counts and errors are in the repository search logs.
''']
for k,q in queries.items():parts.append('\\subsection*{'+esc(k)+'}\n\\begin{quote}\\small\\raggedright '+esc(q)+'\\end{quote}\n\n')
parts.append(r'''\section{Searches and review work not completed}
Scopus, Embase, IEEE Xplore and ACM Digital Library are planned searches, not executed searches. Ready-to-run strings are in the author-access protocol file. Librarian PRESS review, independent dual screening and extraction verification, clinical adjudication, blocked full-text retrieval, version/study-family linkage, and design-appropriate formal appraisal remain pending. The workbook starts with blank reviewer fields. No agreement statistic is calculated from machine priorities.
\section{Provisional report-level extraction}
The following notes identify observations and interpretation limits. They are AI-assisted provisional extraction, not completed formal risk-of-bias judgments. Publication status is report status, not a quality ranking. Access and source-version checks are preserved in the evidence metadata and reading logs. Original 16 report IDs are retained; S01 and S12 are background comparators. New reports retain stable IDs S19--S25.
''')
for x in reports:
 parts.append('\\subsection*{'+esc(x['study_id']+': '+x['name'])+'}\n')
 for label,key in [('Publication status','status'),('Environment','environment'),('Endpoint','endpoint'),('Reported anchor','reported_anchor'),('Source locator','source_locator'),('Interpretation boundary','interpretation_limit')]:parts.append('\\noindent\\textbf{'+label+':} '+esc(x[key])+r'\par'+'\n')
 parts.append('\\noindent\\textbf{Primary source:} \\url{'+x['primary_url']+'}\\par\n\\noindent\\textbf{Human verification:} pending.\n')
parts.append(r'''\section{Appraisal interface and completion rules}
For each final included report, reviewers must record the action object and authority, environment fidelity, ground-truth definition, sample/denominator, comparator and resource budget, judge validation, failure and omission handling, version dependence and prospective outcome evidence. Each domain receives a supported, partially supported, not-assessed-in-this-extraction or unclear value, with a reason and page/section locator. Not assessed must never be interpreted as source absence. Do not generate a composite quality score or apply trial risk-of-bias tools to engineering benchmarks.

Actual clinical investigations require appropriate design-specific appraisal and clinical expertise. Related benchmark datasets, preprint/journal versions and repeated stochastic runs require linkage before any count or confidence interval is interpreted. The final search-derived inclusion set must replace the provisional map; all figure/table denominators and the inclusion flow must then be regenerated.
\section{Conceptual overlap and access limits}
The novelty register compares MedSentry, TACOS, the SDC-to-MCP gateway, clinical testing harnesses, voice-agent ethics assurance, HAARF and existing reviews. HAARF full reading access was blocked. The clinical-testing-harness source is a conceptual letter. Calling a proposal a standard does not establish official regulatory endorsement. A recently published F1000 governance review requires full-text and peer-review-status assessment. CAA is an analytical checklist, not a claimed first framework or evaluated safety intervention.

PRISMA-trAIce is not treated as an endorsed PRISMA extension. A primary JMIR letter, DOI \url{https://doi.org/10.2196/104210}, challenges that endorsement. AI-assisted work is disclosed directly; reporting guidance does not turn incomplete review procedures into completed ones.
\section{Synthetic software and reproducibility}
The parent package's in-memory reference implementation contains one synthetic follow-up task operation with patient/encounter checks, state versions, exact-payload approval, idempotency and receipt verification. Its 18 negative/retry tests are software examples. They contain no LLM, live EHR, authenticated clinical identities or clinical validation. They support no efficacy or patient-safety claim in this review.

The snapshot can be rebuilt using the scripts documented in the v2 README. No patient-level data, full copyrighted reading copies or abstracts are redistributed. Public files contain primary metadata, original extraction notes, search logs, worklists, figures, manuscript sources and build records. Author identity, contributions, conflicts, funding and journal-specific disclosures remain uncompleted.
\end{document}''')
(R/'manuscript/supplement.tex').write_text('\n'.join(parts));print('Supplement generated.')
