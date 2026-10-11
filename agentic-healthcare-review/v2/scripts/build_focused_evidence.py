import json,csv,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R.parent
old=json.loads((P/'research/evidence/studies.json').read_text());new={x['key']:x for x in json.loads((R/'evidence/focus_sources.json').read_text())}
core=[dict(x,selection='provisional focused evidence map; human eligibility pending',scope_reason='Interactive tool, workflow, management or safety evaluation; not a completed search-derived inclusion set') for x in old if x['study_id'] not in ['S01','S12']]
cards=[
 ('medsentry','Adversarial multi-agent simulation','Attack/defense responses','5,000 prompts; 25 threat categories; four topologies','Abstract; benchmark and experimental sections','Threat coverage and attack-response behavior do not establish an unsafe committed-action rate.'),
 ('tacos','Korean clinical intent classification','Intent and tool-selection labels','21 classes','Sections 6.1–6.3; Tables 1–2; Limitations','Private dataset; Korean-only experiments; real-workflow error cascades and clinician utility not yet evaluated.'),
 ('sdcgateway','Synthetic devices and software SDC providers','No-execution invariant and controlled state lifecycle','12 resources; seven tool interactions; 14 ordered-event cases; 28 task–scenario pairs','Sections 5.1–5.4, 6.2–6.4; Tables 5–11','Zero operation attempts and unchanged state digests support the restricted no-execution boundary, not safe actuation, authentication or clinical timing.'),
 ('carepilot','Annotated healthcare GUI workflows','Exact annotated step/sequence match','1,100 tasks; required sequences span 8–24 actions','Dataset section; Evaluation Metrics; Tables 2–5','Task accuracy requires all annotated actions in order. Execution-oriented motivation is not itself a verified committed-state or patient outcome endpoint.'),
 ('careguard','Patient-facing response benchmarks','Risk/hallucination judgments and release threshold','SRA and HRA release thresholds ≤2','Abstract; Fig. 1; benchmark evaluation','Response gating is not transaction authorization. LLM-based safety ratings need independent clinical adjudication and calibration.'),
 ('tieredoversight','Offline safety benchmarks and clinician scenario study','Safety output scores and triage correctness','Five doctors; 20 scenarios; 8/20 correct without and 12/20 with feedback','Section 4; Fig. 7; benchmark methods','Scenario correctness is not live patient benefit. Expert confidence agreement was weak: reported ICC(3,k) −0.101; requires methodological review.'),
 ('saferx','Retrospective MIMIC-III/IV medication recommendation','Medication-set prediction and safety surrogates','Fourth-level ATC generation; interaction/contraindication checks','Abstract; methods and experimental sections','Predicted medication sets and interaction metrics do not establish correctness of transmitted prescriptions or observed adverse events.')]
for n,(key,env,endpoint,anchor,locator,limit) in enumerate(cards,19):
 m=new[key];core.append(dict(study_id=f'S{n:02d}',name=m['name'],key=key,status=m['status'],environment=env,action='safety/tool workflow',endpoint=endpoint,reported_anchor=anchor,source_locator=locator,primary_url=m['url'],interpretation_limit=limit,selection='targeted primary-source retrieval; provisional focused map',human_verification='pending',scope_reason='Action or agent-safety experiment; not a completed search-derived inclusion set'))
assert len(core)==23
(R/'evidence/focused_reports.json').write_text(json.dumps(core,indent=2))
with (R/'evidence/focused_reports.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in core for k in x)));w.writeheader();w.writerows(core)
shutil.copy2(P/'manuscript/references.bib',R/'manuscript/references.bib')
for f in ['IEEEtran.cls','IEEEtran.bst']:shutil.copy2(P/'manuscript'/f,R/'manuscript'/f)
def safe(s):return str(s).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#')
with (R/'manuscript/references.bib').open('a') as f:
 for key,m in new.items():
  if key=='prismatraice':continue
  authors=' and '.join(safe(a) for a in m['authors'] if a) or '{Unverified author metadata}'
  f.write('\n@misc{'+key+',\n author={'+authors+'},\n title={'+safe(m['title'])+'},\n year={'+str(m['year'])+'},\n note={'+safe(m['venue'] or m['status'])+'},\n url={'+m['url']+'}'+(',\n doi={'+m['identifier']+'}' if m['kind']=='doi' else '')+'\n}\n')
rows=[]
for x in core:rows.append(safe(x['name'])+' & '+safe(x['status'])+' & '+safe(x['endpoint'])+' & '+safe(x['interpretation_limit'])+r' \\')
(R/'manuscript/evidence_rows.tex').write_text('\n'.join(rows))
print('23 provisional reports; inherited sample plus seven safety/workflow additions. No human eligibility adjudication.')
