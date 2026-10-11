import json,textwrap
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1];OUT=R/'manuscript/figures'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'svg.fonttype':'none'})
def box(ax,xy,w,h,text,color='#EAF1F5',size=10):
 ax.add_patch(FancyBboxPatch(xy,w,h,boxstyle='round,pad=0.015',facecolor=color,edgecolor='#38566B',linewidth=1));ax.text(xy[0]+w/2,xy[1]+h/2,text,ha='center',va='center',fontsize=size,color='#142D3D')
counts=json.loads((R/'screening/linkage_summary.json').read_text())
fig,ax=plt.subplots(figsize=(4.2,4.5));ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
items=[('Discovery metadata\n2,877 retrieval occurrences',.78),('Administrative exact linkage\n2,397 candidate groups\n480 repeat occurrences linked',.52),('Independent eligibility screening\n0 completed; decisions pending',.26),('Provisional targeted synthesis\n23 reports; not final inclusions',.02)]
for i,(label,y) in enumerate(items):
 box(ax,(.08,y),.84,.17,label,size=10)
 if i<3:ax.annotate('',xy=(.5,y-.04),xytext=(.5,y-.005),arrowprops={'arrowstyle':'->','color':'#38566B'})
fig.tight_layout(pad=.5)
for ext in ['pdf','svg']:fig.savefig(OUT/f'discovery_status.{ext}',bbox_inches='tight')
plt.close(fig)
fig,ax=plt.subplots(figsize=(9.2,4.1));ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
labels=[('Semantic / response safety','TACOS, CareGuardAI, TAO','Labels, output judgments, scenario triage','Does not establish authorized destination effects'),('Action-sequence capability','CarePilot; trajectory benchmarks','Annotated steps, tool calls, workflow criteria','Exact sequence match differs from verified post-state'),('Restricted effect / authority tests','MedAgentBench; SDC-to-MCP','Sandbox effects or deliberately unchanged device state','Tested boundary differs from live clinical permission'),('Clinical / access consequences','Required for operational permissions','Prospective episodes, harm, omissions, workload, follow-up','Not inferred from this provisional map')]
for i,(title,ex,unit,limit) in enumerate(labels):
 y=.76-i*.24
 box(ax,(.01,y),.30,.20,title+'\n'+ex,size=9)
 box(ax,(.34,y),.64,.20,unit+'\n'+limit,color='#F8F9FA',size=9)
 ax.annotate('',xy=(.33,y+.10),xytext=(.315,y+.10),arrowprops={'arrowstyle':'->','color':'#38566B'})
fig.tight_layout(pad=.3)
for ext in ['pdf','svg']:fig.savefig(OUT/f'claim_boundaries.{ext}',bbox_inches='tight')
plt.close(fig)
