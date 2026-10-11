import json,re,hashlib,csv,sys
from pathlib import Path
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];issues=[]
meta=json.loads((R/'research/evidence/reference_metadata.json').read_text());studies=json.loads((R/'research/evidence/studies.json').read_text());refs={r['key'] for r in meta['records']};tex='\n'.join(p.read_text() for p in [R/'manuscript/main.tex',*sorted((R/'manuscript/sections').glob('*.tex'))]);cited={k for s in re.findall(r'\\cite\{([^}]+)\}',tex) for k in s.split(',')}
if cited-refs:issues.append('unknown citations '+str(cited-refs))
if refs-cited:issues.append('uncited references '+str(refs-cited))
if meta['errors']:issues.append('metadata retrieval errors')
if len(studies)!=18 or len(refs)!=54:issues.append('unexpected evidence/reference count')
abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S)[1];words=len(abstract.split())
if words>200:issues.append('abstract exceeds 200 words')
if tex.count('\\begin{figure')!=5 or tex.count('\\begin{table')!=5:issues.append('unexpected figure/table count')
if not json.loads((R/'research/audit/software_test_report.json').read_text())['success']:issues.append('synthetic tests failed')
counts=json.loads((R/'research/searches/inventory_counts.json').read_text());logs=json.loads((R/'research/searches/api_search_log.json').read_text())
if counts['errors'] or not all(x['complete'] for x in logs['retrieval_logs']):issues.append('discovery inventory incomplete')
for p in [R/'manuscript/main.log',R/'manuscript/supplement.log']:
 s=p.read_text();warnings=[l for l in s.splitlines() if 'Overfull' in l or 'undefined' in l]
 if warnings:issues.append(p.name+': '+str(warnings))
output=[]
for p in (R/'outputs').glob('*.pdf'):
 r=PdfReader(p);text=' '.join(x.extract_text() for x in r.pages)
 if len(text)<1000 or '??' in text:issues.append('PDF extraction/unresolved marker '+p.name)
 output.append({'name':p.name,'pages':len(r.pages),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
report={'issues':issues,'passed':not issues,'abstract_words':words,'references':len(refs),'selected_reports':len(studies),'original_figures':5,'tables':5,'equations':tex.count('\\begin{equation}')+2,'discovery':counts,'outputs':output,'limitations':'technical checks only; independent clinical and author verification pending'}
(R/'research/audit/validation_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if issues:sys.exit(1)
