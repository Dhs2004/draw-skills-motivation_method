#!/usr/bin/env python3
"""Reproducible synthetic demonstrations of three academic plot styles.
Requires numpy and matplotlib. --data replays a previously saved demo dataset.
"""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MultipleLocator, FuncFormatter

NAMES = ['triptych_cyan_orange_learning_efficiency',
         'six_panel_serif_multimetric_dual_axis',
         'grouped_bar_blue_palette_hatched_baseline']

def synthetic(seed):
    r = np.random.default_rng(seed)
    x = np.arange(10, 151, 10)
    mean_a = .13 + .56*(1-np.exp(-(x-10)/32)) - .0009*np.maximum(x-100, 0)
    mean_b = .20 + .62*(1-np.exp(-(x-10)/25))
    success = [np.clip(m+r.normal(0,.035,(8,len(x))),0,1) for m in [mean_a,mean_b]]
    tokens = np.arange(25, 501, 50)
    token_cdf = [np.clip(.56/(1+np.exp(-(tokens-205)/43)),0,1), np.clip(.60/(1+np.exp(-(tokens-135)/72)),0,1)]
    # Histogram masses are derived from generated token samples, not from CDF curves.
    bins=np.arange(0,551,50)
    samples=[np.clip(r.normal(230,75,1800),0,499),np.clip(r.exponential(108,1800),0,499)]
    hist=[np.histogram(a,bins)[0]/len(a) for a in samples]
    turns_x=np.arange(151)
    turns=[np.clip(m+r.normal(0,noise,(8,len(turns_x))),4,15) for m,noise in
           [(7+8*np.exp(-turns_x/48),1.15),(6.3+8.7*np.exp(-turns_x/11),.55)]]
    trip=dict(steps=x,success_runs=success,tokens=tokens,token_success=token_cdf,
              bin_centers=(bins[1:]+bins[:-1])/2,token_masses=hist,turn_steps=turns_x,turn_runs=turns)
    long_x=np.linspace(0,80000,17);short_x=np.linspace(0,28000,15)
    t=long_x/80000;u=short_x/28000
    share=.43+.21*t+.07*np.exp(-t*32)+r.normal(0,.006,len(t))
    concentration=.0178+.010*t+.0025*np.exp(-t*30)+r.normal(0,.00025,len(t))
    margin=.018+.22*(1-np.exp(-t*3))+r.normal(0,.008,len(t))
    acc=.50+.098*(1-np.exp(-t*24))-.028*t+r.normal(0,.003,len(t))
    shares=[.50+.34/(1+np.exp(-(u-.42)*9)),.49+.29/(1+np.exp(-(u-.45)*8)),.25+.23/(1+np.exp(-(u-.48)*8))]
    concs=[.019+.026/(1+np.exp(-(u-.47)*9)),.019+.023/(1+np.exp(-(u-.49)*9)),.017+.019/(1+np.exp(-(u-.55)*8))]
    shares=[a+r.normal(0,.007,len(u)) for a in shares];concs=[a+r.normal(0,.00035,len(u)) for a in concs]
    margin2=.02+.90/(1+np.exp(-(u-.46)*8))+r.normal(0,.011,len(u))
    acc2=.51+.145*(1-np.exp(-u*3))+r.normal(0,.003,len(u))
    multi=dict(long_steps=long_x,short_steps=short_x,share=share,concentration=concentration,
               margin=margin,accuracy=acc,shares=shares,concentrations=concs,margin2=margin2,accuracy2=acc2)
    bars=dict(categories=['Task A','Task B','Task C','Task D','Task E'],
              series=['Baseline','Variant A','Variant B','Variant C'],
              values=np.vstack([np.full(5,100),r.integers(80,96,5),r.integers(69,94,5),r.integers(52,86,5)]))
    return dict(synthetic=True,seed=seed,uncertainty='Mean ± one standard deviation over 8 simulated runs; not empirical confidence intervals.',
                triptych=trip,multi_panel=multi,grouped_bar=bars)

def serial(o):
    if isinstance(o,np.ndarray):return o.tolist()
    if isinstance(o,np.generic):return o.item()
    raise TypeError(type(o))

def setup():
    plt.rcParams.update({'font.family':'DejaVu Serif','font.size':9,'axes.titlesize':10,
      'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,
      'axes.linewidth':.8,'lines.linewidth':1.65,'pdf.fonttype':42,'ps.fonttype':42,
      'svg.fonttype':'none','savefig.facecolor':'white','axes.spines.top':True,'axes.spines.right':True})

def grid(ax):
    ax.set_axisbelow(True);ax.grid(True,ls='--',lw=.5,color='#b9b9b9',alpha=.65)

def export(fig,out,name):
    fig.text(.995,.008,'SYNTHETIC DATA · style demonstration',ha='right',va='bottom',fontsize=7,color='#666666')
    for ext in ['png','pdf','svg']:
        fig.savefig(out/(name+'_synthetic.'+ext),dpi=300)
    fig.savefig(out/(name+'_preview.png'),dpi=120)
    plt.close(fig)

def plot_trip(d,out):
    fig,axes=plt.subplots(1,3,figsize=(14.2,3.35));fig.subplots_adjust(left=.047,right=.954,bottom=.19,top=.87,wspace=.34)
    colors=['#08b6ed','#ff4b21'];labels=['Variant A','Variant B'];markers=['o','s']
    ax=axes[0];x=np.array(d['steps'])
    for runs,c,label,m in zip(d['success_runs'],colors,labels,markers):
        a=np.array(runs);y=a.mean(0);sd=a.std(0,ddof=1)
        ax.fill_between(x,y-sd,y+sd,color=c,alpha=.16,lw=0)
        ax.plot(x,y,color=c,marker=m,ms=3.5,label=label)
    ax.set(xlabel='Training step',ylabel='Success rate',ylim=(.08,.92),title='(a) Learning progress');ax.yaxis.set_major_formatter(PercentFormatter(1));ax.legend(loc='upper left',framealpha=.95);grid(ax)
    ax=axes[1];twin=ax.twinx();bins=np.array(d['bin_centers'])
    for probs,c,label,m in zip(d['token_success'],colors,labels,markers):ax.plot(d['tokens'],probs,color=c,marker=m,ms=3.5,label=label)
    for masses,c,offset in zip(d['token_masses'],colors,[-10,10]):
        twin.bar(bins+offset,masses,width=20,color=c,alpha=.20,edgecolor='none')
    twin.set_ylim(0,.65);twin.set_ylabel('Token-length mass',labelpad=5);twin.yaxis.set_major_formatter(PercentFormatter(1))
    twin.axvline(500,color=colors[1],ls='--',lw=1);twin.text(491,.625,'budget',color=colors[1],ha='right',va='top',fontsize=8)
    ax.set(xlabel='Generated tokens',ylabel='Successful trajectory fraction',ylim=(0,.8),xlim=(0,520),title='(b) Token-level efficiency');ax.legend(loc='upper left');grid(ax)
    ax=axes[2]
    for runs,c,label in zip(d['turn_runs'],colors,labels):
        a=np.array(runs);y=a.mean(0);sd=a.std(0,ddof=1)
        ax.fill_between(d['turn_steps'],y-sd,y+sd,color=c,alpha=.23,lw=0);ax.plot(d['turn_steps'],y,color=c,lw=1.05,label=label)
    ax.axhline(15,color='#9730a5',ls='--',lw=1,label='Turn limit = 15')
    ax.set(xlabel='Training step',ylabel='Turns to success',ylim=(4,15.6),title='(c) Turn-level efficiency');ax.legend(loc='upper right');grid(ax)
    export(fig,out,NAMES[0])

def plot_multi(d,out):
    with plt.rc_context({'font.size':10,'axes.labelweight':'bold','axes.titleweight':'bold','axes.linewidth':1.3,'xtick.labelsize':9,'ytick.labelsize':9}):
        fig,axs=plt.subplots(2,3,figsize=(13.8,6.2));fig.subplots_adjust(left=.066,right=.948,top=.94,bottom=.15,hspace=.50,wspace=.27)
        gray='#8c8683';green='#38ad12';red='#dc2930';blue='#007bb6';orange='#f48100'
        xs=[np.array(d['long_steps']),np.array(d['short_steps'])]
        for row in range(2):
            for col in range(3):
                ax=axs[row,col];ax.grid(True,color='#dedede',lw=.7);ax.set_axisbelow(True)
                ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x/1000:.0f}k' if x else '0'))
                ax.xaxis.set_major_locator(MultipleLocator(20000 if row==0 else 5000))
                ax.set_xlabel('Training step',fontsize=9,labelpad=2)
            for col,key in enumerate(['share','concentration']):
                ax=axs[row,col];series=[d[key]] if row==0 else d['shares' if col==0 else 'concentrations']
                for y,c,m,label in zip(series,[gray,green,red],['H','D','^'],['Raw','Variant A','Variant B']):ax.plot(xs[row],y,color=c,marker=m,ms=5,label=label)
                ax.legend(loc='upper left',framealpha=.94)
                if col==0:ax.yaxis.set_major_formatter(PercentFormatter(1))
                ax.set_title(('Component share' if col==0 else 'Concentration'),loc='left',fontsize=11,pad=8)
                ax.text(.5,-.30,f'({chr(97+row*3+col)}) '+('Baseline' if row==0 else 'Variants')+(' — share' if col==0 else ' — concentration'),transform=ax.transAxes,ha='center',fontweight='bold',fontsize=10)
            ax=axs[row,2];right=ax.twinx();x=xs[row]
            l1=ax.plot(x,d['margin' if row==0 else 'margin2'],color=blue,marker='s',ms=5,label='Margin')
            l2=right.plot(x,d['accuracy' if row==0 else 'accuracy2'],color=orange,marker='o',ms=5,label='Accuracy')
            ax.tick_params(axis='y',colors=blue);right.tick_params(axis='y',colors=orange)
            ax.spines['left'].set_color(blue);right.spines['right'].set_color(orange)
            ax.set_title('Margin ↑',loc='left',color=blue,fontsize=11,pad=8);right.set_title('Accuracy ↑',loc='right',color=orange,fontsize=11,pad=8)
            right.yaxis.set_major_formatter(PercentFormatter(1));right.set_ylim(.49,.61 if row==0 else .67);ax.set_ylim(0,.27 if row==0 else 1)
            if row==1:
                ax.axhline(.15,color=blue,ls='--',lw=1.4);right.axhline(.59,color=orange,ls='--',lw=1.4)
            ax.legend(l1+l2,[a.get_label() for a in l1+l2],loc='lower right' if row==0 else 'upper left')
            ax.text(.5,-.30,f'({chr(99+row*3)}) '+('Baseline' if row==0 else 'Variant')+' — performance',transform=ax.transAxes,ha='center',fontweight='bold',fontsize=10)
        export(fig,out,NAMES[1])

def plot_bars(d,out):
    fig,ax=plt.subplots(figsize=(8.5,3.25));fig.subplots_adjust(left=.095,right=.986,top=.74,bottom=.22)
    x=np.arange(len(d['categories']));width=.19;colors=['#315da4','#c7d4e6','#7c94b1','#214da5']
    for i,(name,vals,c) in enumerate(zip(d['series'],d['values'],colors)):
        bars=ax.bar(x+(i-1.5)*width,vals,width,label=name,color=c,edgecolor='white',linewidth=.5,hatch='////' if i==0 else None,zorder=3)
        ax.bar_label(bars,labels=[f'{v:.0f}' for v in vals],fontsize=8,padding=2)
    ax.set_xticks(x,d['categories']);ax.set_ylabel('Relative interactions (%)',fontweight='bold')
    ax.set_ylim(0,118);ax.set_yticks(np.arange(0,101,20));ax.yaxis.set_major_formatter(PercentFormatter(100))
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',ls=':',lw=.7,color='#bfc6d0',zorder=0)
    ax.legend(ncol=4,loc='lower center',bbox_to_anchor=(.5,1.015),frameon=False,handlelength=1.7,columnspacing=1.5)
    fig.suptitle('Interaction cost across synthetic tasks',fontweight='bold',fontsize=12,y=.965)
    fig.text(.50,.065,'Baseline normalized to 100% in each task',ha='center',fontsize=9)
    export(fig,out,NAMES[2])

def csv_exports(d,out):
    p=out/'data';p.mkdir(exist_ok=True)
    def write(name,header,rows):
        with (p/name).open('w',newline='') as f:w=csv.writer(f);w.writerow(header);w.writerows(rows)
    t=d['triptych']
    for key,xkey in [('success_runs','steps'),('turn_runs','turn_steps')]:
        write(key+'.csv',['series','run','step','value'],((s,i,x,v) for s,runs in zip(['Variant A','Variant B'],t[key]) for i,run in enumerate(runs) for x,v in zip(t[xkey],run)))
    write('token_efficiency.csv',['tokens','variant_a_success','variant_b_success'],zip(t['tokens'],*t['token_success']))
    write('token_mass.csv',['bin_center','variant_a_mass','variant_b_mass'],zip(t['bin_centers'],*t['token_masses']))
    m=d['multi_panel'];write('baseline_metrics.csv',['step','share','concentration','margin','accuracy'],zip(m['long_steps'],m['share'],m['concentration'],m['margin'],m['accuracy']))
    write('variant_metrics.csv',['step','raw_share','a_share','b_share','raw_concentration','a_concentration','b_concentration','margin','accuracy'],zip(m['short_steps'],*m['shares'],*m['concentrations'],m['margin2'],m['accuracy2']))
    b=d['grouped_bar'];write('grouped_bar.csv',['task']+b['series'],zip(b['categories'],*b['values']))

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seed',type=int,default=20260929);ap.add_argument('--data',type=Path,help='Replay this script’s synthetic_data.json; not an arbitrary real-data loader');args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    d=json.loads(args.data.read_text()) if args.data else synthetic(args.seed)
    if d.get('synthetic') is not True:raise ValueError('This example renderer only accepts explicitly synthetic data; adapt labels and provenance for real data.')
    (args.out/'synthetic_data.json').write_text(json.dumps(d,default=serial,indent=2))
    setup();plot_trip(d['triptych'],args.out);plot_multi(d['multi_panel'],args.out);plot_bars(d['grouped_bar'],args.out);csv_exports(d,args.out)
    print('Rendered 3 synthetic examples (PNG, PDF, SVG, preview) to',args.out)
if __name__=='__main__':main()
