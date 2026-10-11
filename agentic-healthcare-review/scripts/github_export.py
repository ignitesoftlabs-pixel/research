"""Prepare immutable blob payloads and expected Git SHA1s for connector upload."""
import json,hashlib,base64
from pathlib import Path
from package_project import files,R
D=R.parent/'tmp/github-upload';D.mkdir(parents=True,exist_ok=True)
ps=files()+list((R/'outputs').glob('*.zip'));manifest=[]
for i,p in enumerate(ps):
 data=p.read_bytes();sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();path='agentic-healthcare-review/'+str(p.relative_to(R));b64=base64.b64encode(data).decode();payload=D/f'{i:03}.b64';payload.write_text(b64);manifest.append({'path':path,'sha':sha,'bytes':len(data),'base64_length':len(b64),'payload':str(payload),'text':p.suffix not in ['.pdf','.zip']})
# Active root workflow in addition to portable project copy.
p=R/'.github/workflows/review-build.yml';data=p.read_bytes();payload=D/'rootworkflow.b64';payload.write_text(base64.b64encode(data).decode());manifest.append({'path':'.github/workflows/review-build.yml','sha':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),'bytes':len(data),'base64_length':len(payload.read_text()),'payload':str(payload),'text':True})
(D/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest),'manifest':str(D/'manifest.json')}))
