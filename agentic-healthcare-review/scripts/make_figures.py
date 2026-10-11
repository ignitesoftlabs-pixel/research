"""Original vector figures generated from the evidence register and explicit toy model."""
import json,textwrap
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
R=Path(__file__).resolve().parents[1];D=R/'manuscript/figures';D.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'pdf.fonttype':42,'svg.fonttype':'none'})
NAVY='#16334c';TEAL='#086f72';GOLD='#986614';CORAL='#a74436';PALE='#eef4f6'
def canvas(w,h):
 f=plt.figure(figsize=(w,h));a=f.add_axes([.015,.015,.97,.97]);a.set_xlim(0,1);a.set_ylim(0,1);a.axis('off');return f,a
def box(a,x,y,w,h,title,body='',color=TEAL,fs=8):
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.008,rounding_size=.012',edgecolor=color,facecolor=PALE,lw=1))
 if body:
  a.text(x+w/2,y+h*.73,title,ha='center',va='center',weight='bold',color=color,fontsize=fs)
  a.text(x+w/2,y+h*.34,body,ha='center',va='center',fontsize=fs-.5,color=NAVY)
 else:a.text(x+w/2,y+h/2,title,ha='center',va='center',fontsize=fs,color=color,weight='bold')
def arrow(a,xy1,xy2):a.annotate('',xy=xy2,xytext=xy1,arrowprops={'arrowstyle':'->','color':NAVY,'lw':1})
def save(f,name):
 for ext in ['pdf','svg']:f.savefig(D/(name+'.'+ext),bbox_inches='tight',pad_inches=.025)
 plt.close(f)
f,a=canvas(3.45,2.65)
a.text(.02,.96,'Capability',weight='bold',color=NAVY);a.text(.54,.96,'Required effect boundary',weight='bold',color=NAVY)
for i,(t,b) in enumerate([('Generate','Answer / label'),('Acquire','Bound, current evidence'),('Propose','Typed, reviewable intent'),('Execute','Permitted, verified effect')]):
 y=.74-i*.19;box(a,.02,y,.4,.14,t,fs=8);box(a,.55,y,.42,.14,b,fs=7.4);arrow(a,(.43,y+.07),(.54,y+.07))
a.text(.5,.04,'Greater capability does not confer permission.',ha='center',fontsize=7,color=CORAL)
save(f,'fig1_agency_authority')
rows=json.loads((R/'research/evidence/studies.json').read_text());f,a=canvas(7.15,4.5)
xs=[.015,.275,.36,.63,.805];headers=['Selected report','Status','Environment','Action','Endpoint']
for x,h in zip(xs,headers):a.text(x,.97,h,weight='bold',color=NAVY,fontsize=8.2)
for i,r in enumerate(rows):
 y=.915-i*.049
 if i%2==0:a.add_patch(plt.Rectangle((.005,y-.017),.99,.046,color=PALE,ec='none'))
 vals=[r['study_id']+'  '+r['name'],{'journal':'J','conference':'C','preprint':'P'}[r['status']],r['environment'],r['action'],r['endpoint']]
 for x,v in zip(xs,vals):a.text(x,y,v,va='center',fontsize=7.1,color=NAVY)
save(f,'fig2_evidence_map')
f,a=canvas(7.15,3.35)
box(a,.02,.74,.96,.2,'Trusted institutional context','Principal • purpose • patient • encounter • scopes • policy version',NAVY,9)
for x,t,b in [(.025,'Evidence workspace','Source / time / version'),(.355,'Planner','Typed proposals'),(.685,'Admission gate','Identity • policy • evidence')]:box(a,x,.43,.29,.22,t,b,fs=8.6)
arrow(a,(.315,.54),(.345,.54));arrow(a,(.645,.54),(.675,.54));arrow(a,(.83,.74),(.83,.66))
box(a,.355,.15,.29,.20,'Clinician approval','Exact contract • expiry',GOLD,8.6);arrow(a,(.50,.43),(.50,.36));arrow(a,(.65,.32),(.69,.43));arrow(a,(.83,.43),(.83,.36))
box(a,.685,.15,.29,.20,'Bounded execution','Preconditions • idempotency',TEAL,8.6)
box(a,.025,.15,.29,.20,'Verify destination','Receipt • post-state',CORAL,8.6)
arrow(a,(.83,.14),(.83,.10));arrow(a,(.83,.10),(.17,.10));arrow(a,(.17,.10),(.17,.14))
a.text(.5,.035,'Audit • monitored escalation • suspension • domain-specific recovery',ha='center',color=NAVY,fontsize=8)
save(f,'fig3_caa_framework')
f,a=plt.subplots(figsize=(3.45,2.55));t=np.arange(1,41)
for p,c in [(.99,TEAL),(.98,GOLD),(.95,CORAL)]:a.plot(t,p**t,label=f'p = {p:.2f}',c=c,lw=1.8)
a.set(xlabel='Number of steps T',ylabel='Toy all-steps probability',xlim=(1,40),ylim=(0,1.03));a.spines[['top','right']].set_visible(False);a.grid(alpha=.18);a.legend(frameon=False,fontsize=7);f.tight_layout();save(f,'fig4_horizon_toy')
f,a=canvas(7.15,2.5)
stages=[('1  Specify task','Eligible cases / effects\nHuman ownership'),('2  Offline stress tests','Task and adverse states\nSecurity / omission'),('3  Shadow evaluation','Real timing, no effects\nFailure and workload'),('4  Approved pilot','Bounded real effects\nMonitored fallback'),('5  Prospective comparison','Patient / access outcomes\nWorkload / resources'),('6  Monitor and revalidate','Drift and version changes\nSuspend / recover')]
for i,(t,b) in enumerate(stages):
 x=.025+(i%3)*.33;y=.56 if i<3 else .11;box(a,x,y,.29,.32,t,b,fs=8.5)
 if i%3<2:arrow(a,(x+.30,y+.16),(x+.32,y+.16))
arrow(a,(.84,.55),(.84,.49));arrow(a,(.84,.49),(.17,.49));arrow(a,(.17,.49),(.17,.44))
save(f,'fig5_translation')
print('Five original PDF/SVG figure pairs generated.')
