#!/usr/bin/env python3
"""DEPPO experimental-figure styles, using reproducible synthetic data only.
Dependencies: numpy, matplotlib. --data replays this script's JSON schema.
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
NAMES={3:'annular_pastel_radar',4:'paired_grayscale_hatched_bars',5:'paired_backbone_hatched_bars',6:'perspective_normalized_3d_bars',7:'perspective_3d_ribbon_dynamics',8:'dual_line_translucent_area',9:'dual_pool_task_count_lines',10:'dual_pool_state_count_lines',11:'six_panel_shared_legend_learning',12:'paired_response_entropy_lines',13:'filtering_ablation_lines',14:'four_panel_shaping_diagnostics'}

def make_data(seed):
 r=np.random.default_rng(seed);x=np.arange(1,151)
 def noisy(y,scale=.01):
  z=r.normal(0,scale,len(x));z=np.convolve(np.pad(z,(2,2),mode='edge'),np.ones(5)/5,'valid');return np.asarray(y)+z
 def rise(low,high,rate,delay=0):return low+(high-low)*(1-np.exp(-np.maximum(x-delay,0)/rate))
 radar=np.clip(r.normal(62,18,(7,6)),15,96);radar[0]=r.uniform(82,96,6)
 bars1=r.uniform(43,87,(2,4));bars2=r.uniform(62,91,(2,4));bars2[:,0]=r.uniform(16,27,2)
 sensitivity=r.uniform(45,96,(4,4));sensitivity[:,2]+=4;sensitivity=np.minimum(sensitivity,98)
 ribbons=np.array([noisy(rise(.04,.94,58),.035),noisy(rise(.02,.64,92),.028),noisy(rise(.01,.36,100,22),.02)])
 preference=noisy(.0004*x-.013+.012*np.sin(x/13),.012)
 relative=noisy(.00037*x-.011+.010*np.sin(x/13+.3),.006)
 tasks=np.array([rise(0,750,83),rise(0,650,48),rise(0,760,68),rise(0,530,43)])
 states=np.array([rise(0,65000,123),rise(0,78000,50),rise(0,68000,118),rise(0,45000,62)])
 for a in [tasks,states]:
  for i in range(4):a[i]=np.maximum.accumulate(noisy(a[i],max(a[i])*.008))
 learning=[]
 for panel in range(6):
  learning.append([np.clip(noisy(rise(.02,.72,68,8+panel*2),.085),0,1),np.clip(noisy(rise(.03,.89,47,3+panel*3),.060),0,1),np.clip(noisy(rise(.04,.98,32,2+panel*3),.045),0,1)])
 response=[noisy(79+17*np.exp(-x/20)+2*np.sin(x/8),1.7),noisy(72+25*np.exp(-x/48)+2*np.sin(x/12),1.4),noisy(56+42*np.exp(-x/43)+1.5*np.sin(x/11),1.1)]
 entropy=[noisy(.75+.40*np.exp(-x/20)+.04*np.sin(x/14),.022),noisy(.36+.79*np.exp(-x/45),.018),noisy(.28+.86*np.exp(-x/40),.016)]
 filtering=[np.clip(noisy(rise(.05,.97,42,5),.018),0,1),np.clip(noisy(rise(.05,.86,54,12),.026),0,1)]
 shaping=[ [np.clip(noisy(rise(.01,.27,60),.022),0,1),np.clip(noisy(rise(.01,.42,12)+.04*np.sin(x/13),.032),0,1)],
 [noisy(1+.065/(1+np.exp(-(x-95)/18)),.004),noisy(1+.22/(1+np.exp(-(x-92)/16)),.016)],
 [noisy(-.012*np.exp(-((x-22)/13)**2)+.05/(1+np.exp(-(x-96)/23)),.004),noisy(-.014*np.exp(-((x-23)/15)**2)+.038/(1+np.exp(-(x-97)/22)),.005)],
 [np.clip(noisy(rise(.005,.12,62),.008),0,None),np.clip(noisy(rise(.005,.10,57),.008),0,None)]]
 return dict(synthetic=True,seed=seed,steps=x,radar=radar,bars1=bars1,bars2=bars2,sensitivity=sensitivity,ribbons=np.clip(ribbons,0,1),preference=preference,relative=relative,tasks=tasks,states=states,learning=learning,response=response,entropy=entropy,filtering=filtering,shaping=shaping)

def serial(x):
 if isinstance(x,np.ndarray):return x.tolist()
 if isinstance(x,np.generic):return x.item()
 raise TypeError(type(x))

def style():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,'axes.titlesize':10,'legend.fontsize':8,'xtick.labelsize':8,'ytick.labelsize':8,'axes.linewidth':.65,'lines.linewidth':1.4,'pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})

def clean(ax):
 ax.grid(True,color='#d9dfe3',alpha=.55,lw=.5);ax.set_axisbelow(True)
 for s in ax.spines.values():s.set_color('#777777')

def save(fig,out,num):
 fig.text(.988,.012,'SYNTHETIC DATA · style demonstration',ha='right',va='bottom',color='#777777',fontsize=6.8)
 stem=f'deppo_fig{num:02d}_{NAMES[num]}'
 for ext in ['png','pdf','svg']:fig.savefig(out/(stem+'.'+ext),dpi=300)
 fig.savefig(out/(stem+'_preview.png'),dpi=120);plt.close(fig)

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

def filled(d,out):
 fig,ax=plt.subplots(figsize=(6.5,3.5));fig.subplots_adjust(left=.13,right=.98,bottom=.20,top=.96);x=d['steps']
 for key,c,label in [('preference',RED,'Success–failure preference'),('relative',BLUE,'Relative reweighting')]:
  y=np.array(d[key]);ax.plot(x,y,color=c,lw=1.1,label=label);ax.fill_between(x,0,y,color=c,alpha=.12,lw=0)
 ax.axhline(0,color='#777777',ls=':',lw=.75);ax.set(xlabel='Training step',ylabel='Value',xlim=(1,150));clean(ax);ax.legend(loc='upper left',frameon=False,fontsize=8);save(fig,out,8)

def counts(d,out,num,key,label):
 fig,ax=plt.subplots(figsize=(6.2,3.4));fig.subplots_adjust(left=.14,right=.98,bottom=.21,top=.78)
 for line,c,ls,name in zip(d[key],[BLUE,BLUE,RED,RED],['-','--','-','--'],['Small / success','Small / failure','Large / success','Large / failure']):ax.plot(d['steps'],line,color=c,ls=ls,label=name,lw=1.3)
 ax.set(xlabel='Training step',ylabel=label,xlim=(1,150),ylim=(0,None));clean(ax);ax.legend(ncol=2,loc='lower center',bbox_to_anchor=(.5,1.035),frameon=False,fontsize=8)
 if num==10:ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x/1000:.0f}k'))
 save(fig,out,num)

def learning(d,out):
 fig,axs=plt.subplots(2,3,figsize=(10.7,5.8),sharex=True,sharey=True);fig.subplots_adjust(left=.08,right=.985,bottom=.14,top=.90,hspace=.12,wspace=.07)
 for n,ax in enumerate(axs.flat):
  for y,c,name in zip(d['learning'][n],[BLUE,ORANGE,RED],['Baseline A','Baseline B','Candidate']):ax.plot(d['steps'],y,color=c,lw=1.15,label=name)
  ax.text(.04,.94,'Task '+chr(65+n),transform=ax.transAxes,ha='left',va='top',fontsize=10);ax.set_ylim(0,1.02);ax.set_xlim(1,150);clean(ax)
  if n%3==0:ax.set_ylabel('Validation success rate')
  if n>=3:ax.set_xlabel('Training step')
 fig.legend(*axs[0,0].get_legend_handles_labels(),ncol=3,frameon=False,loc='upper center',bbox_to_anchor=(.5,.986));save(fig,out,11)

def paired(d,out):
 fig,axs=plt.subplots(1,2,figsize=(9.3,3.4));fig.subplots_adjust(left=.075,right=.985,bottom=.21,top=.82,wspace=.23)
 for ax,key,label in zip(axs,['response','entropy'],['Response length','Entropy loss']):
  for y,c,name in zip(d[key],[BLUE,ORANGE,RED],['Baseline A','Baseline B','Candidate']):ax.plot(d['steps'],y,color=c,lw=1.2,label=name)
  ax.set(xlabel='Training step',ylabel=label,xlim=(1,150));clean(ax)
 fig.legend(*axs[0].get_legend_handles_labels(),ncol=3,frameon=False,loc='upper center',bbox_to_anchor=(.5,.987));save(fig,out,12)

def ablation(d,out):
 fig,ax=plt.subplots(figsize=(6.2,3.4));fig.subplots_adjust(left=.13,right=.98,bottom=.21,top=.82)
 for y,c,name in zip(d['filtering'],[BLUE,RED],['With filtering','Without filtering']):ax.plot(d['steps'],y,color=c,label=name,lw=1.25)
 ax.set(xlabel='Training step',ylabel='Validation success rate',xlim=(1,150),ylim=(0,1));clean(ax);ax.legend(loc='lower center',bbox_to_anchor=(.5,1.04),ncol=2,frameon=False);save(fig,out,13)

def diagnostics(d,out):
 fig,axs=plt.subplots(2,2,figsize=(8,6.0));fig.subplots_adjust(left=.11,right=.98,bottom=.13,top=.90,wspace=.27,hspace=.30)
 for pair,ax,label in zip(d['shaping'],axs.flat,['Gated ratio','Mean scale','Mean preference','Mean absolute preference']):
  for y,c,name in zip(pair,[BLUE,RED],['With filtering','Without filtering']):ax.plot(d['steps'],y,color=c,label=name,lw=1.2)
  ax.set(xlabel='Training step',ylabel=label,xlim=(1,150));clean(ax)
 fig.legend(*axs[0,0].get_legend_handles_labels(),ncol=2,frameon=False,loc='upper center',bbox_to_anchor=(.5,.985));save(fig,out,14)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--seed',type=int,default=20260930);ap.add_argument('--data',type=Path);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 d=json.loads(args.data.read_text()) if args.data else make_data(args.seed)
 if d.get('synthetic') is not True:raise ValueError('Only synthetic example data supported by this renderer.')
 (args.out/'synthetic_data.json').write_text(json.dumps(d,default=serial,indent=2))
 # Long-format export includes every raw numerical array with unambiguous indices.
 rows=[]
 def flatten(v,key,indices=()):
  if isinstance(v,(list,np.ndarray)):
   for i,a in enumerate(v):flatten(a,key,indices+(i,))
  else:rows.append([key,'.'.join(map(str,indices)),v])
 for k,v in d.items():
  if k not in ['synthetic','seed']:flatten(v,k)
 with (args.out/'synthetic_values.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['array','zero_based_index','value']);w.writerows(rows)
 style();radar(d,args.out);bars(d,args.out,4,'bars1');bars(d,args.out,5,'bars2');bars3d(d,args.out);ribbons3d(d,args.out);filled(d,args.out);counts(d,args.out,9,'tasks','Task count');counts(d,args.out,10,'states','State count');learning(d,args.out);paired(d,args.out);ablation(d,args.out);diagnostics(d,args.out)
 print('Rendered 12 DEPPO experimental-style examples to',args.out)
if __name__=='__main__':main()
