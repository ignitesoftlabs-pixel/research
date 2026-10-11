import zipfile,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
EXCLUDE={'.aux','.bbl','.blg','.log','.out','.fls','.fdb_latexmk','.pyc'}
def files():
 return [p for p in sorted(R.rglob('*')) if p.is_file() and p.suffix not in EXCLUDE and '__pycache__' not in p.parts and '.venv' not in p.parts and p.suffix!='.zip' and not (p.parent==R/'manuscript' and p.suffix=='.pdf')]
if __name__=='__main__':
 manifest=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files() if p.name!='package_manifest.json'];(R/'research/audit/package_manifest.json').write_text(json.dumps(manifest,indent=2))
 for name,paths in [('Agentic_AI_Healthcare_FullResearchPackage.zip',files()),('Agentic_AI_Healthcare_Overleaf.zip',[p for p in files() if 'manuscript' in p.relative_to(R).parts])]:
  with zipfile.ZipFile(R/'outputs'/name,'w',zipfile.ZIP_DEFLATED) as z:
   for p in paths:z.write(p,p.relative_to(R) if 'FullResearch' in name else p.relative_to(R/'manuscript'))
  print(name,(R/'outputs'/name).stat().st_size)
