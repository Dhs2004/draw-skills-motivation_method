#!/usr/bin/env python3
"""Six compact multi-metric hatched bar examples. Synthetic data only.
Requires numpy, matplotlib, Pillow. --data replays the saved JSON.
"""
import argparse,json,csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from PIL import Image,ImageDraw,ImageFont
NAMES=['paired_metrics','grouped_tasks','four_metric_facets','continuous_blocks','horizontal_metrics','normalized_metrics']
TITLES=['Paired metrics','Grouped tasks','Four-metric facets','Continuous blocks','Horizontal metrics','Baseline-normalized metrics']
COLORS=['#eee9df','#d4cecb','#b6b1b6','#88858e'];HATCH=['///','\\\\','...','---']

def data(seed):
 r=np.random.default_rng(seed)
 v=np.stack([r.uniform(55,90,(3,4)),r.uniform(50,88,(3,4)),r.uniform(80,190,(3,4)),r.uniform(25,65,(3,4))],axis=-1)
 return dict(synthetic=True,seed=seed,tasks=['Task A','Task B','Task C'],methods=['Base','Model A','Model B','Model C'],metrics=[dict(name='Success',unit='%',direction='higher'),dict(name='F1',unit='%',direction='higher'),dict(name='Latency',unit='ms',direction='lower'),dict(name='Cost',unit='units',direction='lower')],values=np.round(v,1).tolist())

def style(ax):
 ax.set_axisbelow(True);ax.grid(axis='y',color='#dce0e3',lw=.6,ls=':');ax.spines[['top','right']].set_visible(False)
 ax.spines[['left','bottom']].set_color('#6b6c70');ax.tick_params(length=3,color='#777777');ax.margins(x=.03)

def label(metric):return metric['name']+' ('+metric['unit']+') '+('↑' if metric['direction']=='higher' else '↓')

def drawbars(ax,positions,values,method_ids,width=1,horizontal=False,annotate=True):
 for p,v,i in zip(positions,values,method_ids):
  opts=dict(color=COLORS[i%4],edgecolor='#56545b',linewidth=.6,hatch=HATCH[i%4],zorder=3)
  if horizontal:
   ax.barh(p,v,height=width,**opts)
   if annotate:ax.annotate(f'{v:.1f}',(v,p),xytext=(4,0),textcoords='offset points',va='center',fontsize=8,color='#343138')
  else:
   ax.bar(p,v,width=width,**opts)
   if annotate:ax.annotate(f'{v:.1f}',(p,v),xytext=(0,4),textcoords='offset points',ha='center',va='bottom',fontsize=7.7,color='#343138')

def figure(rows,cols,methods,figsize):
 fig,axes=plt.subplots(rows,cols,figsize=figsize,squeeze=False);fig.subplots_adjust(left=.095,right=.98,bottom=.19 if rows==1 else .14,top=.81 if rows==1 else .86,wspace=.30,hspace=.43)
 handles=[Patch(facecolor=COLORS[i%4],edgecolor='#56545b',hatch=HATCH[i%4],lw=.6,label=m) for i,m in enumerate(methods)]
 fig.legend(handles=handles,ncol=min(len(methods),6),loc='upper center',bbox_to_anchor=(.5,.982),frameon=False,handlelength=2.2,columnspacing=1.8,fontsize=9)
 for ax in axes.flat:style(ax)
 return fig,axes

def save(fig,out,name):
 fig.text(.986,.015,'SYNTHETIC DATA · touching bars within groups',ha='right',fontsize=6.5,color='#85818a')
 for ext in ['png','pdf','svg']:fig.savefig(out/('hatched_bar_'+name+'.'+ext),dpi=360)
 fig.savefig(out/('hatched_bar_'+name+'_preview.png'),dpi=140);plt.close(fig)

def render(d,out):
 a=np.array(d['values']);methods=d['methods'];metrics=d['metrics'];tasks=d['tasks'];nm=len(methods);nt=len(tasks);means=a.mean(axis=0)
 fig,axs=figure(1,2,methods,(9.0,3.7))
 for k,ax in enumerate(axs.flat):
  drawbars(ax,np.arange(nm),means[:,k],range(nm));ax.set_xticks(range(nm),methods);ax.set_ylabel(label(metrics[k]));ax.set_ylim(0,max(means[:,k])*1.22);ax.set_title('Mean across tasks',fontsize=10,loc='left',pad=10)
 save(fig,out,NAMES[0])
 fig,axs=figure(1,2,methods,(10.4,3.8))
 for k,ax in enumerate(axs.flat):
  for t in range(nt):drawbars(ax,t*(nm+.9)+np.arange(nm),a[t,:,k],range(nm),annotate=False)
  ax.set_xticks(np.arange(nt)*(nm+.9)+(nm-1)/2,tasks);ax.set_ylabel(label(metrics[k]));ax.set_ylim(0,max(a[:,:,k].flat)*1.15)
 save(fig,out,NAMES[1])
 fig,axs=figure(2,2,methods,(9.2,6.0))
 for k,ax in enumerate(axs.flat):
  drawbars(ax,np.arange(nm),means[:,k],range(nm));ax.set_xticks(range(nm),methods);ax.set_ylabel(label(metrics[k]));ax.set_ylim(0,max(means[:,k])*1.23);ax.set_title(metrics[k]['name'],loc='left',fontsize=10,fontweight='bold')
 save(fig,out,NAMES[2])
 fig,axs=figure(1,2,methods,(10.4,3.8))
 for k,ax in enumerate(axs.flat):
  for t in range(nt):
   drawbars(ax,t*nm+np.arange(nm),a[t,:,k],range(nm),annotate=False)
   if t:ax.axvline(t*nm-.5,color='#55515b',lw=.9,ls=':',zorder=4)
  ax.set_xticks(np.arange(nt)*nm+(nm-1)/2,tasks);ax.set_xlim(-.5,nt*nm-.5);ax.set_ylabel(label(metrics[k]));ax.set_ylim(0,max(a[:,:,k].flat)*1.15)
 save(fig,out,NAMES[3])
 fig,axs=figure(1,2,methods,(9.2,3.8))
 for k,ax in zip([2,3],axs.flat):
  drawbars(ax,np.arange(nm),means[:,k],range(nm),horizontal=True);ax.set_yticks(range(nm),methods);ax.invert_yaxis();ax.set_xlabel(label(metrics[k]));ax.set_xlim(0,max(means[:,k])*1.26);ax.set_ylim(nm-.5,-.5);ax.grid(False);ax.grid(axis='x',color='#dce0e3',lw=.6,ls=':')
 save(fig,out,NAMES[4])
 fig,axs=figure(1,2,methods,(10.4,3.8))
 for indices,ax in zip([[0,1],[2,3]],axs.flat):
  for group,k in enumerate(indices):
   vals=means[:,k]/means[0,k]*100;drawbars(ax,group*(nm+1)+np.arange(nm),vals,range(nm),annotate=True)
  ax.set_xticks(np.arange(2)*(nm+1)+(nm-1)/2,[metrics[k]['name']+(' ↑' if metrics[k]['direction']=='higher' else ' ↓') for k in indices]);ax.axhline(100,color='#514b56',ls='--',lw=.9,zorder=5);ax.set_ylabel('Relative to Base (%)');ax.set_ylim(0,max((means[:,k]/means[0,k]*100).max() for k in indices)*1.22)
 save(fig,out,NAMES[5])

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--data',type=Path);ap.add_argument('--seed',type=int,default=20261001);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 d=json.loads(args.data.read_text()) if args.data else data(args.seed);a=np.array(d['values'],float)
 if d.get('synthetic') is not True or a.shape!=(len(d['tasks']),len(d['methods']),4) or len(d['metrics'])!=4 or not np.all(np.isfinite(a)) or np.any(a<=0):raise ValueError('Example schema expects positive synthetic task × method × 4-metric data.')
 if len(d['methods'])>4:raise ValueError('Add distinct palette/hatch entries before using more than four methods.')
 plt.rcParams.update({'font.family':'DejaVu Serif','font.size':9,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'pdf.fonttype':42,'svg.fonttype':'none','hatch.linewidth':.55,'savefig.facecolor':'white'})
 (args.out/'hatched_bar_data.json').write_text(json.dumps(d,indent=2))
 with (args.out/'hatched_bar_data.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['task','method','metric','unit','value'])
  for t,task in enumerate(d['tasks']):
   for m,method in enumerate(d['methods']):
    for k,metric in enumerate(d['metrics']):w.writerow([task,method,metric['name'],metric['unit'],a[t,m,k]])
 render(d,args.out)
 sheet=Image.new('RGB',(1800,1020),'#f0f1f3');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('DejaVuSans.ttf',20)
 for i,(name,title) in enumerate(zip(NAMES,TITLES)):
  x=i%3*600;y=i//3*510;draw.rounded_rectangle((x+10,y+10,x+590,y+500),radius=12,fill='white');im=Image.open(args.out/('hatched_bar_'+name+'_preview.png')).convert('RGB');im.thumbnail((566,416));sheet.paste(im,(x+(600-im.width)//2,y+25+(416-im.height)//2));draw.text((x+300,y+465),title,font=font,anchor='mm',fill='#41404a')
 sheet.save(args.out/'hatched_bar_gallery_overview.png');print('Rendered six touching-bar multi-metric examples.')
if __name__=='__main__':main()
