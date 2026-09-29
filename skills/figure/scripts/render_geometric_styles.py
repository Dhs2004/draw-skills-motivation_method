#!/usr/bin/env python3
"""Four geometric academic plot styles, using explicit synthetic data.
Requires numpy and matplotlib; --data replays the bundled JSON.
"""

from pathlib import Path

import argparse,json,csv

import numpy as np

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from matplotlib.collections import PolyCollection

from matplotlib.ticker import PercentFormatter,FuncFormatter

BLUE='#1585d4';RED='#f33b3e';ORANGE='#ff8a22';GREEN='#569a68'
NAMES={3: 'annular_pastel_radar', 4: 'paired_grayscale_hatched_bars', 6: 'perspective_normalized_3d_bars', 7: 'perspective_3d_ribbon_dynamics'}

def make_data(seed):
 r=np.random.default_rng(seed);x=np.arange(1,151)
 def noisy(y,scale):
  z=r.normal(0,scale,len(x));z=np.convolve(np.pad(z,(2,2),mode='edge'),np.ones(5)/5,'valid');return np.asarray(y)+z
 def rise(low,high,rate,delay=0):return low+(high-low)*(1-np.exp(-np.maximum(x-delay,0)/rate))
 radar=np.clip(r.normal(62,18,(7,6)),15,96);radar[0]=r.uniform(82,96,6)
 bars1=r.uniform(43,87,(2,4))
 # Keep the original example RNG stream after removing its other bar demo.
 r.uniform(62,91,(2,4));r.uniform(16,27,2)
 sensitivity=r.uniform(45,96,(4,4));sensitivity[:,2]+=4;sensitivity=np.minimum(sensitivity,98)
 ribbons=np.array([noisy(rise(.04,.94,58),.035),noisy(rise(.02,.64,92),.028),noisy(rise(.01,.36,100,22),.02)])
 return dict(synthetic=True,seed=seed,steps=x,radar=radar,bars1=bars1,sensitivity=sensitivity,ribbons=np.clip(ribbons,0,1))

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

def bars3d(d,out):
 fig=plt.figure(figsize=(7.6,5.25));ax=fig.add_subplot(111,projection='3d');fig.subplots_adjust(left=.04,right=.91,bottom=.11,top=.96)
 values=np.array(d['sensitivity']);heights=values/values.max(axis=1,keepdims=True)
 for j,c in enumerate(['#cbcbb9','#aac0a0','#6186a6','#c45a58']):
  for k in range(4):
   h=heights[j,k];ax.bar3d(k*1.15,j*1.25,0,.32,.32,h,color=c,edgecolor='#303030',linewidth=.55,shade=True);ax.text(k*1.15+.16,j*1.25+.16,h+.035,f'{values[j,k]:.1f}',ha='center',va='bottom',fontsize=7,color='#9c2828',zorder=100,bbox=dict(facecolor='white',edgecolor='none',alpha=.80,pad=.4))
 ax.set_xticks(np.arange(4)*1.15+.16,['0','5','10','20']);ax.set_yticks(np.arange(4)*1.25+.16,['Metric A','Metric B','Metric C','Metric D']);ax.tick_params(axis='y',pad=1,labelsize=8)
 ax.set_xlabel('Parameter setting',labelpad=7);ax.set_zlabel('Within-metric normalized score',labelpad=9,fontsize=8);ax.set_zlim(0,1.2);ax.set_zticks([.25,.5,.75,1],['0.25×','0.50×','0.75×','1.00×']);ax.view_init(elev=37,azim=-55)
 ax.set_box_aspect((1.25,1.1,.75))
 for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:axis.pane.fill=False
 save(fig,out,6)

def ribbons3d(d,out):
 fig=plt.figure(figsize=(7.5,4.8));ax=fig.add_subplot(111,projection='3d');fig.subplots_adjust(left=.03,right=.93,bottom=.17,top=.98)
 x=np.array(d['steps']);colors=['#5cb5cc','#76b784','#cb864c']
 for j,(line,c) in enumerate(zip(d['ribbons'],colors)):
  verts=[(x[0],0),*zip(x,line),(x[-1],0)];poly=PolyCollection([verts],facecolors=[c],alpha=.20,edgecolors='none');ax.add_collection3d(poly,zs=j,zdir='y');ax.plot(x,np.full(len(x),j),line,color=c,lw=1.15)
 ax.set(xlim=(1,150),ylim=(-.15,2.15),zlim=(0,1));ax.set_xlabel('Training step',labelpad=7);ax.set_zlabel('Ratio',labelpad=5)
 ax.set_yticks([0,1,2],['Coverage','Freshness','Reweighting']);ax.tick_params(axis='y',labelsize=8,pad=9);ax.set_xticks([0,50,100,150]);ax.set_box_aspect((1.8,.9,1));ax.view_init(elev=24,azim=-57)
 for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:axis.pane.fill=False
 save(fig,out,7)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--seed',type=int,default=20260930);ap.add_argument('--data',type=Path);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 d=json.loads(args.data.read_text()) if args.data else make_data(args.seed)
 if d.get('synthetic') is not True:raise ValueError('Only synthetic example data supported by this renderer.')
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
 style();radar(d,args.out);bars(d,args.out,4,'bars1');bars3d(d,args.out);ribbons3d(d,args.out)
 print('Rendered 4 geometric figure styles to',args.out)

if __name__=='__main__':main()
