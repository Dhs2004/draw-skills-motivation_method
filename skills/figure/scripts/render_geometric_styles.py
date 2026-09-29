#!/usr/bin/env python3
"""Two geometric academic plot styles, using explicit synthetic data.
Requires numpy and matplotlib; --data replays the bundled JSON.
"""

from pathlib import Path

import argparse,json,csv

import numpy as np

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt


from matplotlib.ticker import PercentFormatter,FuncFormatter

BLUE='#1585d4';RED='#f33b3e';ORANGE='#ff8a22';GREEN='#569a68'
NAMES={3: 'annular_pastel_radar', 4: 'paired_grayscale_hatched_bars'}

def make_data(seed):
 r=np.random.default_rng(seed)
 radar=np.clip(r.normal(62,18,(7,6)),15,96);radar[0]=r.uniform(82,96,6)
 bars1=r.uniform(43,87,(2,4))
 return dict(synthetic=True,seed=seed,radar=radar,bars1=bars1)

def serial(x):
 if isinstance(x,np.ndarray):return x.tolist()
 if isinstance(x,np.generic):return x.item()
 raise TypeError(type(x))

def style():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,'axes.titlesize':10,'legend.fontsize':8,'xtick.labelsize':8,'ytick.labelsize':8,'axes.linewidth':.65,'lines.linewidth':1.4,'pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})

def save(fig,out,num):
 fig.text(.988,.012,'SYNTHETIC DATA · style demonstration',ha='right',va='bottom',color='#777777',fontsize=6.8)
 stem=NAMES[num]+'_synthetic'
 for ext in ['png','pdf','svg']:fig.savefig(out/(stem+'.'+ext),dpi=300)
 fig.savefig(out/(NAMES[num]+'_preview.png'),dpi=120);plt.close(fig)

def radar(d,out):
 fig=plt.figure(figsize=(5.3,5.3));ax=fig.add_axes([.10,.22,.8,.74],projection='polar')
 n=6;angles=np.linspace(0,2*np.pi,n,endpoint=False);ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1)
 pastels=['#cfe7f0','#cfdded','#edcbd3','#f3d0ac','#f1e19e','#d1e3c8']
 ax.bar(angles,np.full(n,11),width=2*np.pi/n*.97,bottom=91,color=pastels,edgecolor='white',linewidth=1,align='center',zorder=0)
 colors=[RED,'#b6a0c4','#57a9b3','#789877','#999999','#e7a675','#bad6ac']
 for i,(a,c) in enumerate(zip(d['radar'],colors)):
  vals=np.r_[a,a[0]];th=np.r_[angles,angles[0]];ax.plot(th,vals,color=c,lw=1.7 if i==0 else .9,label='Candidate' if i==0 else f'Baseline {i}');ax.fill(th,vals,color=c,alpha=.028)
 for th,label in zip(angles,['Task A','Task B','Task C','Task D','Task E','Task F']):ax.text(th,96.5,label,ha='center',va='center',fontsize=8)
 ax.set_ylim(0,103);ax.set_yticks([20,40,60,80]);ax.tick_params(axis='y',labelsize=7);ax.set_xticks(angles,['']*n);ax.grid(alpha=.27,lw=.55);ax.spines['polar'].set_color('#666666')
 fig.legend(*ax.get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.068),ncol=4,frameon=False,fontsize=7.1,columnspacing=1.1)
 save(fig,out,3)

def bars(d,out,num,key):
 fig,axs=plt.subplots(1,2,figsize=(7.8,3.1));fig.subplots_adjust(left=.09,right=.975,bottom=.28,top=.93,wspace=.28)
 colors=['#eee4cc','#c6b9b9','#b8b4b3','#9793a4'];hatches=['///','|||','\\\\','---']
 for j,ax in enumerate(axs):
  vals=d[key][j]
  for k,(v,c,h) in enumerate(zip(vals,colors,hatches)):
   ax.bar(k,v,.64,color=c,edgecolor='#777777',lw=.6,hatch=h);ax.text(k,v+2,f'{v:.1f}',ha='center',fontsize=8)
  labels=['Base','Variant A','Variant B','Candidate'] if num==5 else ['Baseline A','Baseline B','Baseline C','Candidate']
  ax.set_xticks(range(4),labels,rotation=18,ha='right');ax.set_ylim(0,105);ax.set_ylabel('Success rate (%)');ax.set_yticks(range(0,101,20));ax.grid(axis='y',ls=':',color='#dddddd');ax.set_axisbelow(True)
  ax.text(.025,.97,('Task '+chr(65+j)) if num==4 else ('Backbone '+chr(65+j)),transform=ax.transAxes,ha='left',va='top',fontsize=8,bbox=dict(boxstyle='square,pad=.13',facecolor='#e1e5e6',edgecolor='#777777',lw=.6))
 save(fig,out,num)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--seed',type=int,default=20260930);ap.add_argument('--data',type=Path);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 d=json.loads(args.data.read_text()) if args.data else make_data(args.seed)
 if d.get('synthetic') is not True:raise ValueError('Only synthetic example data supported by this renderer.')
 d={k:v for k,v in d.items() if k in ['synthetic','seed','radar','bars1']}
 (args.out/'geometric_styles_data.json').write_text(json.dumps(d,default=serial,indent=2))
 # Long-format export includes every raw numerical array with unambiguous indices.
 rows=[]
 def flatten(v,key,indices=()):
  if isinstance(v,(list,np.ndarray)):
   for i,a in enumerate(v):flatten(a,key,indices+(i,))
  else:rows.append([key,'.'.join(map(str,indices)),v])
 for k,v in d.items():
  if k not in ['synthetic','seed']:flatten(v,k)
 with (args.out/'geometric_styles_values.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['array','zero_based_index','value']);w.writerows(rows)
 style();radar(d,args.out);bars(d,args.out,4,'bars1')
 print('Rendered 2 geometric figure styles to',args.out)

if __name__=='__main__':main()
