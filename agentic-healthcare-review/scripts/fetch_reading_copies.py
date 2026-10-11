"""Download primary reading copies outside the public repository; log hashes, not texts."""
import json,urllib.request,subprocess,hashlib,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];DEST=R.parent/'tmp/reading-copies';DEST.mkdir(parents=True,exist_ok=True)
rows=json.loads((R/'research/evidence/studies.json').read_text())
def fetch(r):
 u=r['primary_url']
 if 'arxiv.org/abs/' in u:u=u.replace('/abs/','/pdf/')
 elif u.startswith('https://www.nature.com/articles/'):u+='.pdf'
 elif u.endswith('fallahpour25a.html'):u='https://proceedings.mlr.press/v267/fallahpour25a/fallahpour25a.pdf'
 elif 'aclanthology.org' in u:u=u.rstrip('/')+'.pdf'
 out={'study_id':r['study_id'],'url':u,'retrieved_at':datetime.now(timezone.utc).isoformat()}
 try:
  data=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Research/1.0'}),timeout=60).read();pdf=data.startswith(b'%PDF');path=DEST/(r['study_id']+('.pdf' if pdf else '.html'));path.write_bytes(data)
  if pdf:subprocess.run(['pdftotext','-layout',str(path),str(path.with_suffix('.txt'))],check=True,capture_output=True)
  out.update({'downloaded':True,'format':'pdf' if pdf else 'html','sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'access_level':'full text downloaded' if pdf or r['study_id']=='S15' else 'html requires inspection'})
 except Exception as e:out.update({'downloaded':False,'error':str(e),'access_level':'primary abstract/landing page fallback'})
 return out
if __name__=='__main__':
 out=[]
 with ThreadPoolExecutor(max_workers=4) as p:
  for f in as_completed([p.submit(fetch,r) for r in rows]):r=f.result();out.append(r);print(r['study_id'],r.get('downloaded'),r.get('error',''),flush=True)
 (R/'research/evidence/reading_access_log.json').write_text(json.dumps(sorted(out,key=lambda x:x['study_id']),indent=2))
