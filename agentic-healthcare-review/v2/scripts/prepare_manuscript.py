"""Build v2 derived sections without modifying the archived v1 manuscript."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[1];P=R.parent
(R/'manuscript/sections').mkdir(exist_ok=True);(R/'manuscript/figures').mkdir(exist_ok=True)
e=(P/'manuscript/sections/04_evidence.tex').read_text()
start=e.index('\\begin{figure*}');end=e.index('\\end{figure*}',start)+len('\\end{figure*}')
e=e[:start]+e[end:]
e=e.replace('Figure~\\ref{fig:evidence} maps the selected reports by publication status, environment, action, and endpoint. It is categorical: neither rows nor colors define a performance ranking. The central pattern is a progression from answers and dialogue toward verifiable benchmark effects, with persistent separation between simulation and live patient care.','The inherited evidence anchors below are retained to preserve the distinction between knowledge, simulated interaction, and destination effects. MedAgents and diagnostic AMIE are background comparators; the other 16 reports form the inherited part of the 23-report provisional map. Seven additional safety/workflow reports are analyzed in Section~\\ref{sec:new}. This subset is not the inclusion set of a completed systematic search.')
e=e.replace('The central pattern','The provisional pattern').replace('selected evidence','provisional evidence')
(R/'manuscript/sections/inherited_evidence.tex').write_text(e)
f=(P/'manuscript/sections/05_failures.tex').read_text();f=f[:f.index('\\subsection{Long horizons and omissions}')]
f+='''\\subsection{Omission and unresolved effects}
Action correctness also misses harmful inaction. A system can complete every attempted operation while failing to notice a critical task, deferring beyond its deadline, or escalating without effective follow-through. Safety analysis must include omissions and availability of the human fallback. A destination timeout should be classified as an unresolved effect until a reconciliation procedure identifies whether the operation committed. It must not be scored as an ordinary harmless failed attempt.
'''
(R/'manuscript/sections/failures.tex').write_text(f)
c=(P/'manuscript/sections/06_framework.tex').read_text().replace('\\section{Clinical Action Assurance Framework}','\\section{An Analytical Checklist for Action Assurance}')
c=c.replace('CAA is a proposed reference framework for connecting clinical evidence, institutional authority, bounded execution, and verified effects.','CAA is used here as an analytical checklist connecting clinical evidence, institutional authority, bounded execution, and verified effects. The overlapping contributions in Table~\\ref{tab:overlap} rule out an assertion that these controls are first proposed here.')
c=c.replace('Proposed Clinical Action Assurance architecture.','Analytical Clinical Action Assurance checklist rendered as a possible architecture.').replace('The diagram is a proposed design, not a clinically validated system.','The diagram synthesizes existing obligations; it is not a novel or clinically validated safety intervention.')
(R/'manuscript/sections/checklist.tex').write_text(c)
t=(P/'manuscript/sections/07_evaluation.tex').read_text().replace('Figure~\\ref{fig:translation} proposes six stages.','Figure~\\ref{fig:translation} summarizes six familiar stages of evaluation; the clinical-harness literature likewise argues for staged evidence \\cite{clinicalharness}.')
t=t.replace('Proposed staged translation,','Analytical summary of staged translation,')
(R/'manuscript/sections/evaluation.tex').write_text(t)
for name in ['fig3_caa_framework.pdf','fig5_translation.pdf']:
 shutil.copy2(P/'manuscript/figures'/name,R/'manuscript/figures'/name)
print('Prepared derived sections; v1 preserved.')
