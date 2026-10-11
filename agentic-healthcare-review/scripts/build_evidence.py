import json,csv
from pathlib import Path
R=Path(__file__).resolve().parents[1]
# Original analytical extractions; reported quantities are not pooled.
DATA=[
('MedAgents','medagents2024','conference','offline QA','answer','accuracy','boundary comparator','Multi-agent medical reasoning; static answers do not establish executed clinical effects.','Primary ACL paper','https://aclanthology.org/2024.findings-acl.33/'),
('AgentClinic','agentclinic2026','journal','simulated patients','acquire','diagnosis','interactive diagnostic benchmark','Simulated patient conversations and information acquisition; no prospective live autonomous care established here.','Primary journal','https://www.nature.com/articles/s41746-026-02674-7'),
('MedRAX','medrax2025','conference','image-tool sandbox','tool','task answer','2500 queries','Tool use on medical images evaluates bounded benchmark outputs, not deployed radiology decisions.','Primary conference','https://proceedings.mlr.press/v267/fallahpour25a.html'),
('MedAgentBench','medagentbench2025','journal','EHR sandbox','sandbox write','task success','300 tasks; 100 profiles','Original task success concerns scripted sandbox effects.','Primary journal / preprint','https://arxiv.org/abs/2501.14654'),
('MedAgentBench v2','medagentbenchv2','conference','EHR sandbox','sandbox write','task success','91% original without memory; 98% with feedback memory; 266/300 (88.67%) new tasks','Different task sets and memory conditions must not be merged into one rate.','Sections 2.3, 3.1–3.3','https://psb.stanford.edu/psb-online/proceedings/psb26/chen_eric.pdf'),
('PhysicianBench','physicianbench2026','preprint','real-record EHR sandbox','sandbox write','pass@1','100 tasks; 670 checkpoints; average 27 calls; best 46%','Execution-grounded tasks using real records remain benchmark evaluations.','Abstract; full paper','https://arxiv.org/abs/2605.02240'),
('HealthAgentBench','healthagentbench2026','preprint','container environments','artifact','task success','54 tasks; 7 categories; best approximately 42%','Composite research and healthcare tasks; aggregate is not clinical efficacy.','Abstract; full paper','https://arxiv.org/abs/2606.31179'),
('PatientAgentBench','patientagentbench2026','preprint','simulated patients','propose','triage-quality pass','1200 scenarios; 10 models; triage-quality pass rates 32–88%','Dialogue and triage outputs do not verify downstream patient care.','Abstract; results','https://arxiv.org/abs/2607.25485'),
('MedCTA','medcta2026','preprint','tool benchmark','tool','trajectory/output','107 tasks; 5 tools','Process evaluation complements final outputs; neither alone establishes clinical utility.','Abstract; benchmark design','https://arxiv.org/abs/2606.11702'),
('MIRA','mira2026','journal','retrospective-record simulation','propose','diagnosis/management','over 500 cases; 11 tools; over 85000 action options','Retrospective evaluation and physician comparison do not establish prospective autonomous practice.','Main results; methods','https://www.nature.com/articles/s41586-026-10675-5'),
('On-premise agent','onprem2026','journal','MIMIC-derived simulation','propose','selective diagnosis','threshold 0.90: coverage 49.4%; diagnostic accuracy 98.9%','Retained diagnostic accuracy is not the unsafe committed-action rate.','Abstract; selective-autonomy results','https://www.nature.com/articles/s41591-026-04609-x'),
('AMIE diagnosis','amie2025','journal','patient actors','dialogue','diagnosis/dialogue','randomized actor-based evaluation','Boundary comparator: actor encounters do not establish autonomous ordering or patient outcomes.','Methods: study design','https://www.nature.com/articles/s41586-025-08866-7'),
('AMIE management','amiemanagement2026','journal','multivisit patient actors','propose','management quality','longitudinal actor-based evaluation','Recommendations and simulated follow-up are distinct from live execution.','Main results; methods','https://www.nature.com/articles/s41586-026-10764-5'),
('MAI-DxO','maid2025','preprint','published diagnostic cases','acquire','diagnosis/modeled cost','304 NEJM cases','Simulated testing costs are not observed healthcare expenditure or clinical outcomes.','Benchmark design','https://arxiv.org/abs/2506.22405'),
('GPTPlan','gptplan2025','journal','retrospective plan optimization','artifact','dose-plan quality','12 lung IMRT; 5 cervical VMAT','Abstract-only extraction; no claim of treatment delivery or patient benefit.','Abstract only','https://pubmed.ncbi.nlm.nih.gov/40073507/'),
('MedAgentBoard','medagentboard2025','conference','offline mixed tasks','answer','task-specific metrics','multi-agent and conventional comparators','Multiple agents do not imply benefit independent of task, budget, or comparator.','Primary conference / preprint','https://arxiv.org/abs/2505.12371'),
('MedAssist','medassist2026','journal','offline mixed benchmarks','tool','benchmark scores','vOpenManus configuration','Framework evaluation does not establish safety of an institutional workflow.','Primary journal','https://www.nature.com/articles/s41746-026-02443-6'),
('HealthAdminBench','healthadmin2026','preprint','four GUI replicas','sandbox write','task/subtask success','135 tasks; 1698 points; best task 36.3%; highest subtask 82.8%','Task best is Claude Opus 4.6 CUA; subtask best is GPT-5.4 CUA: different configurations.','Abstract; benchmark/results','https://arxiv.org/abs/2604.09937')]
rows=[]
for i,d in enumerate(DATA,1):
 row=dict(zip(['name','key','status','environment','action','endpoint','reported_anchor','interpretation_limit','source_locator','primary_url'],d));row['study_id']=f'S{i:02}';row['selection']='purposive';row['human_verification']='pending';rows.append(row)
(R/'research/evidence/studies.json').write_text(json.dumps(rows,indent=2))
for fn in ['studies.csv','selection_register.csv']:
 with (R/'research/evidence'/fn).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (R/'research/evidence/claim_links.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['claim_id','study_id','key','claim','locator','limitation','independent_human_check'])
 for row in rows:w.writerow([row['study_id']+'-anchor',row['study_id'],row['key'],row['reported_anchor'],row['source_locator'],row['interpretation_limit'],'pending'])
