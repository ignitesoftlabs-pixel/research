"""Primary source versions and reading access, with no copied full texts in public repo."""
import json,time,urllib.request,urllib.parse,xml.etree.ElementTree as ET,subprocess,hashlib
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
R=Path(__file__).resolve().parents[2];P=R.parent/'tmp/v2-private';P.mkdir(exist_ok=True)
SEEDS=[
('medsentry','MedSentry','arxiv','2505.20824','empirical'),
('tacos','TACOS','doi','10.18653/v1/2025.emnlp-industry.124','empirical'),
('sdcgateway','Safety-bounded SDC-to-MCP','arxiv','2609.31358','empirical'),
('carepilot','CarePilot','arxiv','2603.24157','empirical'),
('careguard','CareGuardAI','arxiv','2604.26959','empirical'),
('tieredoversight','Tiered Agentic Oversight','arxiv','2506.12482','empirical'),
('medicalmalice','Medical Malice','arxiv','2511.21757','empirical'),
('saferx','SafeRx-Agent','arxiv','2605.29146','empirical'),
('mcpfhir','MCP-FHIR','arxiv','2506.13800','conceptual_or_implementation'),
('voiceassurance','Voice-agent ethics assurance','arxiv','2305.14182','conceptual'),
('clinicalharness','Clinical testing harnesses','doi','10.1007/s10439-026-04381-6','conceptual'),
('haarf','HAARF','doi','10.64898/2026.04.09.26350519','conceptual_preprint'),
('broadscoping','Agentic AI in medicine scoping map','arxiv','2607.25489','review_preprint'),
('prismas','PRISMA-S','doi','10.1186/s13643-020-01542-z','reporting'),
('press','PRESS 2015','doi','10.1016/j.jclinepi.2016.01.021','reporting'),
('prismatraice','PRISMA-trAIce','doi','10.2196/80247','reporting_candidate')]
def get(u):
 for n in range(3):
  try:return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ClinicalActionReview/2.0'}),timeout=45).read()
  except Exception:
   if n==2:raise
   time.sleep(2+n)
def fetch(seed):
 key,name,kind,identifier,role=seed;r={'key':key,'name':name,'kind':kind,'identifier':identifier,'stream':role,'retrieved_at':datetime.now(timezone.utc).isoformat()};ns={'a':'http://www.w3.org/2005/Atom'}
 try:
  if kind=='arxiv':
   root=ET.fromstring(get('https://export.arxiv.org/api/query?id_list='+identifier));e=root.find('a:entry',ns);r.update({'title':' '.join(e.findtext('a:title',namespaces=ns).split()),'authors':[a.findtext('a:name',namespaces=ns) for a in e.findall('a:author',ns)],'year':int(e.findtext('a:published',namespaces=ns)[:4]),'url':e.findtext('a:id',namespaces=ns),'venue':'arXiv preprint arXiv:'+identifier,'status':'preprint'});u='https://arxiv.org/pdf/'+identifier
  else:
   m=json.loads(get('https://api.crossref.org/works/'+urllib.parse.quote(identifier,safe='')))['message'];r.update({'title':m['title'][0],'authors':[(a.get('family','')+', '+a.get('given','')).strip(', ') for a in m.get('author',[])],'year':m.get('published',m.get('issued'))['date-parts'][0][0],'url':'https://doi.org/'+identifier,'venue':' '.join(m.get('container-title',[])),'status':'preprint' if m['type']=='posted-content' or key=='haarf' else 'conference' if key=='tacos' else 'journal'});r['crossref_title']=m['title'][0]
   u='https://aclanthology.org/2025.emnlp-industry.124.pdf' if key=='tacos' else 'https://link.springer.com/content/pdf/10.1007/s10439-026-04381-6.pdf' if key=='clinicalharness' else 'https://www.medrxiv.org/content/'+identifier+'v1.full.pdf' if key=='haarf' else r['url']
  r['metadata_success']=True
  try:
   data=get(u);pdf=data.startswith(b'%PDF');path=P/(key+('.pdf' if pdf else '.html'));path.write_bytes(data)
   if pdf:subprocess.run(['pdftotext','-layout',str(path),str(path.with_suffix('.txt'))],check=True,capture_output=True)
   r.update({'reading_url':u,'reading_downloaded':True,'reading_format':'pdf' if pdf else 'html','sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
  except Exception as e:r.update({'reading_downloaded':False,'reading_error':str(e)})
 except Exception as e:r.update({'metadata_success':False,'metadata_error':str(e)})
 return r
if __name__=='__main__':
 out=[]
 with ThreadPoolExecutor(max_workers=4) as p:
  for f in as_completed([p.submit(fetch,s) for s in SEEDS]):r=f.result();out.append(r);print(r['key'],r['metadata_success'],r.get('reading_downloaded'),r.get('metadata_error',''),flush=True)
 (R/'v2/evidence/focus_sources.json').write_text(json.dumps(sorted(out,key=lambda x:x['key']),indent=2,ensure_ascii=False))
