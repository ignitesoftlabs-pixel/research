import subprocess,json,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];out=[]
for name,dest in [('main','Clinical_Action_Evidence_Review.pdf'),('supplement','Clinical_Action_Review_Supplement.pdf')]:
 p=subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=R/'manuscript',capture_output=True,text=True)
 (R/'audit'/f'{name}_build_console.txt').write_text(p.stdout+p.stderr)
 if p.returncode:raise RuntimeError(p.stdout[-6000:])
 log=(R/'manuscript'/f'{name}.log').read_text()
 defects=[line for line in log.splitlines() if 'Overfull' in line or 'undefined' in line.lower()]
 if defects:raise RuntimeError('\n'.join(defects))
 target=R/'outputs'/dest;shutil.copy2(R/'manuscript'/f'{name}.pdf',target)
 out.append({'file':dest,'pages':len(PdfReader(target).pages),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'undefined_or_overfull':defects})
(R/'audit/build_report.json').write_text(json.dumps({'built_at':datetime.now(timezone.utc).isoformat(),'outputs':out},indent=2));print(out)
