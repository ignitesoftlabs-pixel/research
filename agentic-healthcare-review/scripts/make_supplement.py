import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def tex(s):
 s=s.replace('–','--').replace('—','---')
 for a,b in [('&',r'\&'),('%',r'\%'),('_',r'\_')]:s=s.replace(a,b)
 return s
rows=json.loads((R/'research/evidence/studies.json').read_text());counts=json.loads((R/'research/searches/inventory_counts.json').read_text());qs=json.loads((R/'research/searches/queries.json').read_text());logs=json.loads((R/'research/searches/api_search_log.json').read_text())
s=r'''\documentclass[journal,10pt]{IEEEtran}
\usepackage[T1]{fontenc}
\usepackage{lmodern,cite,booktabs,tabularx,array,listings}
\usepackage[hyphens]{url}
\usepackage[hidelinks]{hyperref}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\lstset{basicstyle=\ttfamily\scriptsize,breaklines=true,columns=fullflexible,keepspaces=true,breakatwhitespace=false}
\setlength{\emergencystretch}{2em}
\title{Supplementary Research Methods and Evidence Register\\Agentic AI in Healthcare}
\author{Companion to the AI-assisted critical review draft}
\begin{document}\maketitle\raggedbottom\bstctlcite{IEEEcontrol}
\section{Purpose and Provenance}
This supplement records discovery queries, extraction boundaries, the selected evidence register, and a synthetic software demonstration. It is a methodological companion to a purposive critical integrative review, not a PRISMA flow or evidence of independent dual screening. Literature cutoff: 10 October 2026. The current exports were rebuilt and retrieved after the original temporary workspace was lost; timestamps in the repository are authoritative for this refreshed snapshot. No historical inventory was reconstructed as raw data.
\section{Discovery Inventory}
Database queries retrieve metadata for discovery. All unselected records remain unassessed. PubMed uses publication dates; arXiv uses submitted dates. Identifier duplicate removal does not adjudicate article/preprint versions or establish scientific deduplication. No reported count is a prevalence denominator or a completed screening count.
\begin{table}[h]\caption{Refreshed discovery snapshot}\centering\footnotesize
\begin{tabularx}{\columnwidth}{@{}Yr@{}}\toprule
Quantity & Count\\\midrule
'''
for l in logs['retrieval_logs']:s+=tex(l['query_id'])+' retrieved occurrences & '+str(l['retrieved_count'])+r'\\'+'\n'
for label,k in [('All query occurrences','query_occurrences'),('Unique database identifiers','unique_database_identifiers'),('Duplicate identifier occurrences','duplicate_identifier_occurrences'),('Purposively selected reports','selected_reports')]:s+=label+' & '+str(counts[k])+r'\\'+'\n'
s+=r'''\bottomrule\end{tabularx}\end{table}
\subsection{Exact reproducible queries}
'''
for k,q in qs.items():s+='\\subsubsection{'+tex(k)+'}\n\\begin{lstlisting}\n'+q+'\n\\end{lstlisting}\n'
s+=r'''\section{Selection, Extraction, and Access}
Selection spans reasoning, dialogue, imaging tools, EHR task execution, management, planning, and administrative workflows. Eighteen reports provide analytical anchors: eight journal, four conference, and six preprint reports under the cited versions; two are boundary comparators. This is a purposive map, not exhaustive selection from the discovery inventory. Older conceptual, reporting, uncertainty, interoperability, and governance sources provide context.

Fields include source key and persistent identifier, publication status, environment, action/effect, task/sample unit, endpoint, quantitative anchor, source locator, and interpretation limit. Primary PDF/landing retrieval status and hashes are logged separately. Reading copies are kept outside the public project. GPTPlan is abstract-only. Bibliographic resolution does not verify a scientific claim. AI-assisted extraction and targeted source checks do not substitute for independent clinical verification; every register row marks that author check as pending.
\section{Selected Empirical Register}
'''
for row in rows:
 s+='\\subsection{'+row['study_id']+': '+tex(row['name'])+'}\n'
 s+='\\textbf{Status/environment:} '+tex(row['status']+'; '+row['environment'])+'. \\textbf{Action/endpoint:} '+tex(row['action']+'; '+row['endpoint'])+'.\n\n'
 s+='\\textbf{Reported anchor:} '+tex(row['reported_anchor'])+' \\cite{'+row['key']+'}. \\textbf{Locator:} '+tex(row['source_locator'])+'. \\textbf{Limit:} '+tex(row['interpretation_limit'])+'\n\n'
s+=r'''\section{Synthetic Reference Implementation}
The implementation demonstrates an in-memory gate for one operation: creation of a follow-up review task. It contains no LLM, patient record, production clinical rule set, or authenticated reviewer service. Subject and encounter strings are synthetic. The trusted policy, evidence timestamps, resource version, payload digest, approval expiry, and idempotency registry are explicit and testable. A lock illustrates atomic check/write behavior within one process; it does not solve distributed clinical transactions.

Negative tests cover wrong patient, wrong encounter, adapter mismatch, prohibited operation, changed resource version, changed evidence version, missing approval, mutated approved arguments, wrong reviewer, expiry, future evidence, stale evidence, duplicate identical retry, duplicate-key conflict, mismatched receipt, revoked scope, and changed policy. A valid execution test verifies the destination receipt. Tests run against software invariants only. They cannot establish clinical appropriateness, identity security, prompt-injection robustness, clinician review quality, interoperability, or patient benefit. A receipt mismatch after a committed write triggers escalation; the demonstration does not erase the effect or claim universal rollback.

\section{Before Author Submission}
Submitting authors should independently verify numerical anchors and publication versions, complete names/affiliations/contributions/conflicts/funding, obtain clinical and methodological review, and assess overlap with recent reviews. Confirm the target journal's current scope, initial submission format, AI disclosure policy, reference and figure rules, and current JCR category/quartile. Replace anonymous draft declarations only with true statements. Clinical systems require validation beyond the included illustrative tests. The accompanying cover letter is unsent and needs author completion. No journal acceptance is promised.
\bibliographystyle{IEEEtran}\bibliography{references}
\end{document}
'''
(R/'manuscript/supplement.tex').write_text(s)
