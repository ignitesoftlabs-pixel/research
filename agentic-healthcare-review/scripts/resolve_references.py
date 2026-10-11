import json,time,urllib.request,urllib.parse,xml.etree.ElementTree as ET,unicodedata
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
DOIS='''wooldridge1995 10.1017/S0269888900008122
singhal2023 10.1038/s41586-023-06291-2
moor2023 10.1038/s41586-023-05881-4
hager2024 10.1038/s41591-024-03097-1
goh2024 10.1001/jamanetworkopen.2024.40969
medagents2024 10.18653/v1/2024.findings-acl.33
agentclinic2026 10.1038/s41746-026-02674-7
medagentbench2025 10.1056/AIdbp2500144
medagentbenchv2 10.1142/9789819824755_0025
mira2026 10.1038/s41586-026-10675-5
onprem2026 10.1038/s41591-026-04609-x
amie2025 10.1038/s41586-025-08866-7
amiemanagement2026 10.1038/s41586-026-10764-5
gptplan2025 10.1088/1361-6560/adbff1
medassist2026 10.1038/s41746-026-02443-6
medicalagentsbench2026 10.1016/j.patter.2026.101610
leeinjection2025 10.1001/jamanetworkopen.2025.49963
qfire2026 10.64898/2026.06.04.26354950
xu2026survey 10.1016/j.jbi.2026.105045
collaco2026review 10.1038/s41746-026-02517-5
vatsal2026taxonomy 10.1109/ACCESS.2026.3651218
hu2026survey 10.1109/RBME.2026.3704162
sanra2019 10.1186/s41073-019-0064-8
prisma2020 10.1136/bmj.n71
prismascr2018 10.7326/M18-0850
decideai2022 10.1038/s41591-022-01772-9
consortai2020 10.1038/s41591-020-1034-x
spiritai2020 10.1038/s41591-020-1037-7
tripodllm2025 10.1038/s41591-024-03425-5
stardai2025 10.1038/s41591-025-03953-8
consort2025 10.1136/bmj-2024-081123
mimiciv2023 10.1038/s41597-022-01899-x
semanticentropy2024 10.1038/s41586-024-07421-0
nist2023 10.6028/NIST.AI.100-1
nist2024 10.6028/NIST.AI.600-1'''
ARXIV='''react2023 2210.03629
toolformer2023 2302.04761
reflexion2023 2303.11366
rag2020 2005.11401
medrax2025 2502.02673
physicianbench2026 2605.02240
healthagentbench2026 2606.31179
patientagentbench2026 2607.25485
medcta2026 2606.11702
maid2025 2506.22405
medagentboard2025 2505.12371
healthadmin2026 2604.09937
mpib2026 2602.06268
calibration2017 1706.04599
selective2017 1705.08500'''
OVERRIDES={'wooldridge1995':{'year':1995},'medagentbenchv2':{'year':2026},'nist2024':{'authors':['{National Institute of Standards and Technology}'],'title':'Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile'}}
for key,year,venue in [('react2023',2023,'International Conference on Learning Representations'),('toolformer2023',2023,'Advances in Neural Information Processing Systems'),('reflexion2023',2023,'Advances in Neural Information Processing Systems'),('rag2020',2020,'Advances in Neural Information Processing Systems'),('medrax2025',2025,'Proceedings of the 42nd International Conference on Machine Learning'),('medagentboard2025',2025,'Advances in Neural Information Processing Systems'),('calibration2017',2017,'Proceedings of the 34th International Conference on Machine Learning'),('selective2017',2017,'Advances in Neural Information Processing Systems')]:OVERRIDES[key]={'year':year,'venue':venue,'type':'inproceedings'}
MANUAL=[('who2024','World Health Organization','Ethics and governance of artificial intelligence for health: Guidance on large multi-modal models',2024,'https://www.who.int/publications/i/item/9789240084759'),('smart2024','HL7 International','SMART App Launch, version 2.2.0',2024,'https://hl7.org/fhir/smart-app-launch/STU2.2/'),('fhir2019','HL7 International','FHIR Release 4, version 4.0.1: Security, AuditEvent and Provenance',2019,'https://hl7.org/fhir/R4/security.html'),('governingagents2023','OpenAI','Practices for Governing Agentic AI Systems',2023,'https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf')]
def get(url):
 for n in range(3):
  try:return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HealthcareReview/1.0'}),timeout=40).read()
  except Exception:
   if n==2:raise
   time.sleep(n+1)
def cross(pair):
 key,doi=pair;m=json.loads(get('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')))['message']
 authors=[(a.get('family','')+', '+a.get('given','')).strip(', ') if a.get('family') else '{'+a.get('name','Organization')+'}' for a in m.get('author',[])]
 r={'key':key,'doi':doi,'title':m['title'][0],'authors':authors or ['{'+m.get('publisher','Author to verify')+'}'],'year':m.get('published',m.get('issued'))['date-parts'][0][0],'venue':(m.get('container-title') or [m.get('publisher','')])[0],'volume':m.get('volume',''),'number':m.get('issue',''),'pages':m.get('page',m.get('article-number','')),'url':'https://doi.org/'+doi,'type':'inproceedings' if m['type'] in ('book-chapter','proceedings-article') else 'article','retrieved_at':datetime.now(timezone.utc).isoformat()}
 r['original_title']=r['title'];r['original_year']=r['year'];r.update(OVERRIDES.get(key,{}));return r
def tex(s):
 s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode()
 for c,v in [('&',r'\&'),('%',r'\%'),('_',r'\_'),('#',r'\#')]:s=s.replace(c,v)
 return s
if __name__=='__main__':
 out=[];errors=[]
 with ThreadPoolExecutor(max_workers=5) as p:
  fs={p.submit(cross,x.split()):x.split()[0] for x in DOIS.splitlines()}
  for f in as_completed(fs):
   try:r=f.result();out.append(r);print(r['key'],r['title'][:70],flush=True)
   except Exception as e:errors.append({'key':fs[f],'error':str(e)})
 try:
  ns={'a':'http://www.w3.org/2005/Atom'};pairs=[x.split() for x in ARXIV.splitlines()];root=ET.fromstring(get('https://export.arxiv.org/api/query?id_list='+','.join(x[1] for x in pairs)));es={e.findtext('a:id',namespaces=ns).split('/abs/')[-1].split('v')[0]:e for e in root.findall('a:entry',ns)}
  for key,aid in pairs:
   if aid not in es:
    time.sleep(3.1)
    one=ET.fromstring(get('https://export.arxiv.org/api/query?id_list='+aid))
    es[aid]=one.find('a:entry',ns)
   e=es[aid];r={'key':key,'arxiv':aid,'title':' '.join(e.findtext('a:title',namespaces=ns).split()),'authors':[a.findtext('a:name',namespaces=ns) for a in e.findall('a:author',ns)],'year':int(e.findtext('a:published',namespaces=ns)[:4]),'venue':'arXiv preprint arXiv:'+aid,'url':'https://arxiv.org/abs/'+aid,'version_url':e.findtext('a:id',namespaces=ns),'type':'misc','retrieved_at':datetime.now(timezone.utc).isoformat()};r.update(OVERRIDES.get(key,{}));out.append(r)
 except Exception as e:errors.append({'key':'arxiv','error':str(e)})
 for k,a,t,y,u in MANUAL:out.append({'key':k,'title':t,'authors':['{'+a+'}'],'year':y,'venue':a,'url':u,'type':'misc','metadata_method':'manual primary source'})
 out.sort(key=lambda r:r['key']);(ROOT/'research/evidence/reference_metadata.json').write_text(json.dumps({'records':out,'errors':errors,'editorial_overrides':OVERRIDES},indent=2,ensure_ascii=False))
 bib=[r'@IEEEtranBSTCTL{IEEEcontrol, CTLuse_forced_etal={yes}, CTLmax_names_forced_etal={6}, CTLnames_show_etal={1}, CTLuse_url={yes}}']
 for r in out:
  fields={'author':' and '.join(r['authors']),'title':'{'+r['title']+'}','year':r['year'],'journal' if r['type']=='article' else 'booktitle' if r['type']=='inproceedings' else 'howpublished':r['venue'],'url':r['url']}
  fields.update({k:r[k] for k in ('doi','volume','number','pages') if r.get(k)})
  bib.append('@'+r['type']+'{'+r['key']+',\n'+',\n'.join('  '+k+' = {'+(str(v) if k=='url' else tex(v))+'}' for k,v in fields.items())+'\n}')
 (ROOT/'manuscript/references.bib').write_text('\n\n'.join(bib)+'\n');print('Resolved',len(out),'errors',errors)
 if errors:raise SystemExit(1)
