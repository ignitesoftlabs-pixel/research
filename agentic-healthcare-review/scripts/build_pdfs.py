import subprocess,json,shutil,hashlib
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]
if not (R/'manuscript/supplement.tex').exists():subprocess.run(['python3',str(R/'scripts/make_supplement.py')],check=True)
report=[]
for source,out in [('main','Agentic_AI_Healthcare_Review.pdf'),('supplement','Agentic_AI_Healthcare_Supplement.pdf')]:
 p=subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',source+'.tex'],cwd=R/'manuscript',text=True,capture_output=True)
 (R/'research/audit'/f'{source}_build_console.txt').write_text(p.stdout+p.stderr)
 if p.returncode:print(p.stdout[-5000:]);raise SystemExit(p.returncode)
 dest=R/'outputs'/out;shutil.copy2(R/'manuscript'/(source+'.pdf'),dest);report.append({'file':out,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size})
(R/'research/audit/build_report.json').write_text(json.dumps({'built_at':datetime.now(timezone.utc).isoformat(),'outputs':report},indent=2))
print(report)
