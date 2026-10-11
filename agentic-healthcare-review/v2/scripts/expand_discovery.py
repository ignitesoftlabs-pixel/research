"""Supplementary primary metadata discovery. No licensed abstracts in public output."""
import sys,json,csv,time,urllib.request,urllib.parse,xml.etree.ElementTree as ET,hashlib
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'v2/searches';PRIVATE=ROOT.parent/'tmp/v2-private';PRIVATE.mkdir(parents=True,exist_ok=True)
QUERIES={
'P3_action_safety':'(("large language model"[Title/Abstract] OR "large language models"[Title/Abstract] OR LLM[Title/Abstract] OR agentic[Title/Abstract]) AND (agent[Title/Abstract] OR agents[Title/Abstract] OR agentic[Title/Abstract] OR "tool use"[Title/Abstract] OR "computer use"[Title/Abstract]) AND (healthcare[Title/Abstract] OR clinical[Title/Abstract] OR medical[Title/Abstract] OR patient[Title/Abstract]) AND (safety[Title/Abstract] OR safe[Title/Abstract] OR risk[Title/Abstract] OR execution[Title/Abstract] OR oversight[Title/Abstract] OR authorization[Title/Abstract] OR "prompt injection"[Title/Abstract])) AND ("2022/01/01"[Date - Publication] : "2026/10/10"[Date - Publication])',
'E1_action_safety':'(TITLE_ABS:"large language model" OR TITLE_ABS:LLM OR TITLE_ABS:agentic) AND (TITLE_ABS:agent OR TITLE_ABS:agents OR TITLE_ABS:"tool use" OR TITLE_ABS:"computer use") AND (TITLE_ABS:healthcare OR TITLE_ABS:clinical OR TITLE_ABS:medical OR TITLE_ABS:patient) AND (TITLE_ABS:safety OR TITLE_ABS:execution OR TITLE_ABS:oversight OR TITLE_ABS:authorization OR TITLE_ABS:"prompt injection") AND FIRST_PDATE:[2022-01-01 TO 2026-10-10]',
'C1_crossref':'agentic healthcare clinical safety',
'C2_crossref':'large language model medical agent execution safety'}
def now():return datetime.now(timezone.utc).isoformat()
def get(u):
 for n in range(3):
  try:return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ActionSafetyReview/2.0'}),timeout=60).read()
  except Exception:
   if n==2:raise
   time.sleep(n+2)
def tx(e,p):
 n=e.find(p);return ' '.join(''.join(n.itertext()).split()) if n is not None else ''
def pubmed():
 key='P3_action_safety';q=QUERIES[key];base='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';u=base+'esearch.fcgi?'+urllib.parse.urlencode({'db':'pubmed','term':q,'retmax':10000,'retmode':'json'});result=json.loads(get(u));(D/(key+'_esearch.json')).write_text(json.dumps(result,indent=2));ids=result['esearchresult']['idlist'];rows=[]
 for start in range(0,len(ids),100):
  time.sleep(.4);xml=get(base+'efetch.fcgi?'+urllib.parse.urlencode({'db':'pubmed','id':','.join(ids[start:start+100]),'retmode':'xml'}));(PRIVATE/f'pubmed_{start:05}.xml').write_bytes(xml);root=ET.fromstring(xml)
  for a in root.findall('PubmedArticle'):
   pmid=tx(a,'MedlineCitation/PMID');doi=next((e.text for e in a.findall('PubmedData/ArticleIdList/ArticleId') if e.attrib.get('IdType')=='doi'),'');rows.append({'query':key,'database':'PubMed','id':pmid,'doi':doi,'title':tx(a,'MedlineCitation/Article/ArticleTitle'),'year':tx(a,'MedlineCitation/Article/Journal/JournalIssue/PubDate/Year'),'venue':tx(a,'MedlineCitation/Article/Journal/Title'),'url':'https://pubmed.ncbi.nlm.nih.gov/'+pmid+'/','date_basis':'PubMed publication date'})
 return rows,{'query_id':key,'query':q,'reported_count':int(result['esearchresult']['count']),'retrieved_count':len(rows),'complete':len(rows)==int(result['esearchresult']['count']),'retrieved_at':now(),'api_url':u}
def europe():
 key='E1_action_safety';q=QUERIES[key];cursor='*';rows=[];total=None
 for page in range(100):
  u='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':q,'format':'json','pageSize':100,'cursorMark':cursor,'resultType':'core'});raw=get(u);(PRIVATE/f'europe_{page:03}.json').write_bytes(raw);data=json.loads(raw);total=data['hitCount'];results=data['resultList']['result']
  for r in results:rows.append({'query':key,'database':'EuropePMC','id':r['source']+':'+r['id'],'doi':r.get('doi',''),'title':r.get('title',''),'year':r.get('pubYear',''),'venue':r.get('journalInfo',{}).get('journal',{}).get('title',''),'url':'https://europepmc.org/article/'+r['source']+'/'+r['id'],'date_basis':'EuropePMC first publication date'})
  nxt=data.get('nextCursorMark')
  if not results or len(rows)>=total or not nxt or nxt==cursor:break
  cursor=nxt;time.sleep(.4)
 return rows,{'query_id':key,'query':q,'reported_count':total,'retrieved_count':len(rows),'complete':len(rows)==total,'retrieved_at':now(),'api_url':u,'overlap_note':'MED includes PubMed; PPR includes preprints; not independent coverage'}
def crossref(key):
 q=QUERIES[key];u='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':q,'filter':'from-pub-date:2022-01-01,until-pub-date:2026-10-10','rows':200});data=json.loads(get(u))['message'];rows=[]
 for r in data['items']:
  if not r.get('title'):continue
  rows.append({'query':key,'database':'Crossref','id':r['DOI'],'doi':r['DOI'],'title':' '.join(r['title']),'year':r.get('published',r.get('issued',{})).get('date-parts',[['']])[0][0],'venue':' '.join(r.get('container-title',[])),'url':'https://doi.org/'+r['DOI'],'date_basis':'Crossref publication date filter'})
 return rows,{'query_id':key,'query':q,'reported_count':data['total-results'],'retrieved_count':len(rows),'complete':False,'retrieval_limit':200,'retrieved_at':now(),'api_url':u,'restriction':'relevance-ranked metadata discovery; deliberately bounded, not exhaustive search'}
if __name__=='__main__':
 D.mkdir(exist_ok=True);(D/'queries_v2.json').write_text(json.dumps(QUERIES,indent=2));rows=[];logs=[];errors=[]
 with ThreadPoolExecutor(max_workers=4) as p:
  fs={p.submit(fun,*args):name for name,fun,args in [('PubMed',pubmed,()),('EuropePMC',europe,()),('Crossref1',crossref,('C1_crossref',)),('Crossref2',crossref,('C2_crossref',))]}
  for f in as_completed(fs):
   try:r,l=f.result();rows+=r;logs.append(l);print(l['query_id'],l['retrieved_count'],flush=True)
   except Exception as e:errors.append({'source':fs[f],'error':str(e)})
 with (D/'supplementary_records.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=['query','database','id','doi','title','year','venue','url','date_basis']);w.writeheader();w.writerows(rows)
 (D/'search_log_v2.json').write_text(json.dumps({'logs':logs,'errors':errors,'cutoff':'2026-10-10','retrieved_at':now(),'private_raw_retained_outside_public_repo':True},indent=2))
 print('New query occurrences',len(rows),'errors',errors)
 if errors:raise SystemExit(1)
