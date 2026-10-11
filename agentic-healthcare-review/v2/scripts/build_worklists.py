"""Administrative linkage, not eligibility screening or scientific study deduplication."""
import csv,json,re,unicodedata,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]; P=R.parent
def read(p):
 with p.open(newline='') as f:return list(csv.DictReader(f))
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
rows=read(P/'research/searches/database_records.csv')+read(R/'searches/supplementary_records.csv')
parent=list(range(len(rows)))
def find(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
seen={};edges=[]
for i,r in enumerate(rows):
 keys=[('title',norm(r['title']))]
 if r.get('doi'):keys.append(('doi',r['doi'].lower().strip().removeprefix('https://doi.org/')))
 keys.append(('dbid',r['database']+':'+r['id']))
 for k in keys:
  if not k[1]:continue
  if k in seen:
   parent[find(i)]=find(seen[k]);edges.append(dict(left_occurrence=f'O{i+1:05d}',right_occurrence=f'O{seen[k]+1:05d}',reason='exact_'+k[0],matched_value=k[1]))
  else:seen[k]=i
groups=collections.defaultdict(list)
for i,r in enumerate(rows):groups[find(i)].append(r)
work=[];occ=[]
for n,g in enumerate(groups.values(),1):
 r=g[0]; cid=f'C{n:05d}'; t=r['title'].lower()
 priority='focused retrieval' if re.search(r'agent|tool.use|computer.use',t) and re.search(r'clinical|health|medical|patient|ehr|hospital|radiotherapy',t) else 'standard review'
 work.append(dict(candidate_id=cid,title=r['title'],year=r['year'],doi=next((x['doi'] for x in g if x.get('doi')),''),url=r['url'],databases='; '.join(sorted({x['database'] for x in g})),occurrences=len(g),machine_priority=priority,reviewer_A='',reviewer_B='',consensus='',exclusion_reason='',source_locator='',notes='Administrative candidate group; study-family and version linkage unresolved.'))
 for x in g:occ.append(dict(occurrence_id=f'O{len(occ)+1:05d}',candidate_id=cid,**{k:x.get(k,'') for k in ['query','database','id','doi','title','year','url']}))
def write(name,data):
 with (R/'screening'/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
write('candidate_register.csv',work);write('occurrence_linkage.csv',occ)
write('linkage_edges.csv',edges)
(R/'screening/candidates.json').write_text(json.dumps(work,indent=2))
(R/'screening/occurrences.json').write_text(json.dumps(occ,indent=2))
counts={'retrieval_occurrences':len(rows),'administrative_candidate_groups':len(work),'linked_repeat_occurrences':len(rows)-len(work),'by_query':dict(collections.Counter(x['query'] for x in rows)),'human_screened':0,'full_text_eligibility_adjudicated':0,'method':'Union exact DOI, normalized exact title, or database identifier; candidate groups are not scientific studies. No exclusions performed.'}
(R/'screening/linkage_summary.json').write_text(json.dumps(counts,indent=2));print(counts)
