"""Reproducible discovery inventory; no abstracts, no screening inference."""
import json,csv,time,urllib.request,urllib.parse,xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]/'research/searches'
Q={
'P1_agentic':'((agentic[Title/Abstract] OR "LLM agent"[Title/Abstract] OR "LLM agents"[Title/Abstract] OR "large language model agent"[Title/Abstract] OR "large language model agents"[Title/Abstract] OR "tool-using"[Title/Abstract]) AND (healthcare[Title/Abstract] OR medical[Title/Abstract] OR clinical[Title/Abstract] OR medicine[Title/Abstract] OR patient[Title/Abstract])) AND ("2022/01/01"[Date - Publication] : "2026/10/10"[Date - Publication])',
'P2_collaboration':'(("multi-agent"[Title/Abstract] OR multiagent[Title/Abstract]) AND ("large language model"[Title/Abstract] OR "large language models"[Title/Abstract] OR LLM[Title/Abstract] OR LLMs[Title/Abstract]) AND (healthcare[Title/Abstract] OR medical[Title/Abstract] OR clinical[Title/Abstract] OR medicine[Title/Abstract])) AND ("2022/01/01"[Date - Publication] : "2026/10/10"[Date - Publication])',
'A1_arxiv':'((ti:agentic OR abs:agentic OR ti:"medical agent" OR ti:"clinical agent" OR ti:"LLM agents" OR ti:"multi-agent") AND (ti:healthcare OR ti:medical OR ti:clinical OR abs:"electronic health record" OR abs:"clinical tool")) AND submittedDate:[202201010000 TO 202610102359]'}
def get(url):
 for n in range(3):
  try:return urllib.request.urlopen(url,timeout=60).read()
  except Exception:
   if n==2:raise
   time.sleep(2+n)
def text(e,path):
 n=e.find(path);return ' '.join(''.join(n.itertext()).split()) if n is not None else ''
if __name__=='__main__':
 R.mkdir(parents=True,exist_ok=True);rows=[];logs=[];errors=[]
 (R/'queries.json').write_text(json.dumps(Q,indent=2))
 for key,query in Q.items():
  started=datetime.now(timezone.utc).isoformat();before=len(rows)
  try:
   if key.startswith('P'):
    base='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';u=base+'esearch.fcgi?'+urllib.parse.urlencode({'db':'pubmed','term':query,'retmax':10000,'retmode':'json'})
    result=json.loads(get(u));(R/(key+'_esearch.json')).write_text(json.dumps(result,indent=2));ids=result['esearchresult']['idlist'];count=int(result['esearchresult']['count'])
    for start in range(0,len(ids),100):
     time.sleep(.4);root=ET.fromstring(get(base+'efetch.fcgi?'+urllib.parse.urlencode({'db':'pubmed','id':','.join(ids[start:start+100]),'retmode':'xml'})))
     for article in list(root):
      if article.tag=='PubmedArticle':
       pmid=text(article,'MedlineCitation/PMID');title=text(article,'MedlineCitation/Article/ArticleTitle');year=text(article,'MedlineCitation/Article/Journal/JournalIssue/PubDate/Year') or text(article,'MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate')[:4];venue=text(article,'MedlineCitation/Article/Journal/Title');doi=next((x.text for x in article.findall('PubmedData/ArticleIdList/ArticleId') if x.attrib.get('IdType')=='doi'),'')
      else:
       pmid=text(article,'BookDocument/PMID');title=text(article,'BookDocument/ArticleTitle') or text(article,'BookDocument/Book/BookTitle');year=text(article,'BookDocument/Book/PubDate/Year');venue=text(article,'BookDocument/Book/BookTitle');doi=''
      rows.append({'query':key,'database':'PubMed','id':pmid,'title':title,'year':year,'venue':venue,'doi':doi,'url':'https://pubmed.ncbi.nlm.nih.gov/'+pmid+'/','status':'unassessed_metadata_inventory'})
    logs.append({'query_id':key,'query':query,'started_at':started,'reported_count':count,'retrieved_count':len(rows)-before,'complete':len(rows)-before==count,'api_url':u})
   else:
    ns={'a':'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/'};count=None
    for start in range(0,10000,200):
     time.sleep(3.1);u='https://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':query,'start':start,'max_results':200,'sortBy':'submittedDate','sortOrder':'descending'});root=ET.fromstring(get(u));count=int(root.findtext('o:totalResults',namespaces=ns));entries=root.findall('a:entry',ns)
     for e in entries:
      url=e.findtext('a:id',namespaces=ns);aid=url.split('/abs/')[-1].split('v')[0];rows.append({'query':key,'database':'arXiv','id':aid,'title':' '.join(e.findtext('a:title',namespaces=ns).split()),'year':e.findtext('a:published',namespaces=ns)[:4],'venue':'arXiv','doi':'','url':'https://arxiv.org/abs/'+aid,'status':'unassessed_metadata_inventory'})
     if start+len(entries)>=count or not entries:break
    logs.append({'query_id':key,'query':query,'started_at':started,'reported_count':count,'retrieved_count':len(rows)-before,'complete':len(rows)-before==count,'api_url':u})
   print(key,len(rows)-before,flush=True)
  except Exception as e:errors.append({'query_id':key,'error':str(e),'retrieved_count':len(rows)-before})
  (R/'api_search_log.json').write_text(json.dumps({'retrieval_logs':logs,'errors':errors,'cutoff':'2026-10-10','design':'unassessed discovery inventory, not systematic screening'},indent=2))
  if rows:
   with (R/'database_records.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 unique={ (r['database'],r['id']):r for r in rows }
 if rows:
  with (R/'unique_database_records.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(unique.values())
 (R/'inventory_counts.json').write_text(json.dumps({'query_occurrences':len(rows),'unique_database_identifiers':len(unique),'duplicate_identifier_occurrences':len(rows)-len(unique),'not_article_level_deduplication':True,'selected_reports':18,'retrieved_at':datetime.now(timezone.utc).isoformat(),'errors':errors},indent=2))
 if errors:raise SystemExit(1)
