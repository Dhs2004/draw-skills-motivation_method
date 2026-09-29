#!/usr/bin/env python3
"""Six annular radar designs with identical synthetic data and 0–100 scales.
Requires matplotlib, numpy and Pillow. --data uses geometric_styles_data.json.
"""
from pathlib import Path
import argparse,json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge,Circle,Polygon
from matplotlib.lines import Line2D
from matplotlib.colors import to_rgb
from PIL import Image,ImageDraw,ImageFont

PASTEL=['#a4cad7','#b1bde2','#d9aec6','#e5b397','#e4d092','#b4ceb4']
JEWEL=['#32889e','#667abd','#ac6499','#cd8667','#bfa15b','#669985']
STYLES=[
 dict(name='pastel_bloom',title='Pastel Bloom',ring='wide',grid='circle',focus='#bc476a',serif=True,fill=.06,background='#ffffff'),
 dict(name='jewel_arc',title='Jewel Arc',ring='jewel',grid='circle',focus='#244f70',serif=False,fill=.055,background='#ffffff'),
 dict(name='porcelain_double_ring',title='Porcelain',ring='double',grid='circle',focus='#317c87',serif=True,fill=.045,background='#ffffff'),
 dict(name='aurora_gradient',title='Aurora',ring='gradient',grid='circle',focus='#7f4e90',serif=False,fill=.06,background='#ffffff'),
 dict(name='faceted_spectrum',title='Faceted Spectrum',ring='facet',grid='polygon',focus='#b86446',serif=True,fill=.045,background='#ffffff'),
 dict(name='minimal_ribbon',title='Minimal Ribbon',ring='ribbon',grid='polygon',focus='#355989',serif=False,fill=.035,background='#ffffff'),
]

def blend(c,white):
 a=np.array(to_rgb(c));return tuple(a*(1-white)+white)

def render(data,out,style):
 fig=plt.figure(figsize=(6.7,6.6),facecolor=style['background'])
 ax=fig.add_axes([.045,.155,.91,.82]);ax.set_aspect('equal');ax.set_xlim(-1.48,1.48);ax.set_ylim(-1.43,1.43);ax.axis('off')
 theta=np.arange(6)*np.pi/3;directions=np.c_[np.sin(theta),np.cos(theta)]
 # Every design shares the same linear radius and six task positions.
 grid='#dce3e8'
 for k in [2,4,6,8,10]:
  radius=k/10
  if style['grid']=='polygon':ax.add_patch(Polygon(directions*radius,closed=True,facecolor=('#f5f8fa' if k%4==2 else '#ffffff'),edgecolor=grid,lw=.65,zorder=1-k*.01))
  else:ax.add_patch(Circle((0,0),radius,facecolor=('#f5f8fa' if k%4==2 else '#ffffff'),edgecolor=grid,lw=.65,zorder=1-k*.01))
 for direction in directions:ax.plot([0,direction[0]],[0,direction[1]],color='#d8e0e5',lw=.65,zorder=2)
 ax.add_patch(Circle((0,0),.012,color='#ccd5dd',zorder=3))
 # Color identifies the task, never the score.
 for j in range(6):
  center=90-j*60;start=center-28.4;end=center+28.4;c=PASTEL[j];strong=JEWEL[j];kind=style['ring']
  if kind=='wide':
   ax.add_patch(Wedge((0,0),1.265,start,end,width=.17,facecolor=blend(c,.12),edgecolor='white',lw=.8))
   ax.add_patch(Wedge((0,0),1.282,start,end,width=.011,facecolor=strong,edgecolor='none',alpha=.7))
  elif kind=='jewel':
   ax.add_patch(Wedge((0,0),1.26,start,end,width=.16,facecolor=strong,edgecolor='none'))
   ax.add_patch(Wedge((0,0),1.074,start,end,width=.012,facecolor=blend(c,.22),edgecolor='none'))
  elif kind=='double':
   ax.add_patch(Wedge((0,0),1.264,start,end,width=.034,facecolor=strong,edgecolor='none'))
   ax.add_patch(Wedge((0,0),1.214,start,end,width=.113,facecolor=blend(c,.64),edgecolor='none'))
   ax.add_patch(Wedge((0,0),1.076,start,end,width=.009,facecolor=blend(c,.22),edgecolor='none'))
  elif kind=='gradient':
   for band in range(36):
    radius=1.084+(band+1)*.185/36
    ax.add_patch(Wedge((0,0),radius,start,end,width=.185/36+.0005,facecolor=blend(c,.78-.55*band/35),edgecolor='none'))
   ax.add_patch(Wedge((0,0),1.275,start,end,width=.01,facecolor=strong,edgecolor='none',alpha=.8))
  elif kind=='facet':
   ax.add_patch(Wedge((0,0),1.265,start,end,width=.15,facecolor=blend(c,.34),edgecolor='white',lw=.7))
   ax.add_patch(Wedge((0,0),1.28,start,end,width=.018,facecolor=strong,edgecolor='none'))
   ax.scatter(*(directions[j]*1.055),s=12,color=strong,zorder=5,linewidths=0)
  else:
   ax.add_patch(Wedge((0,0),1.135,start+1,end-1,width=.062,facecolor=c,edgecolor='none'))
   ax.add_patch(Wedge((0,0),1.144,start+1,end-1,width=.008,facecolor=strong,edgecolor='none'))
  if kind=='ribbon':
   xy=directions[j]*1.292;rot=0;labelcolor='#334455';bbox=dict(boxstyle='round,pad=.33,rounding_size=.3',facecolor=blend(c,.72),edgecolor='none')
  else:
   r=1.175 if kind!='double' else 1.159;xy=directions[j]*r;rot=-j*60
   if rot < -90:rot+=180
   if rot < -90:rot+=180
   labelcolor='white' if kind=='jewel' else '#334455';bbox=None
  ax.text(*xy,f'Task {chr(65+j)}',ha='center',va='center',rotation=rot,rotation_mode='anchor',fontsize=10.3,fontweight='normal',fontfamily='DejaVu Serif' if style['serif'] else 'DejaVu Sans',color=labelcolor,bbox=bbox,zorder=12)
 # Muted but individually distinguishable baselines; modest, distinct markers.
 baselines=['#6b8ea7','#aa9b78','#85a49c','#9790b3','#bc9a96','#909aa5']
 markers=['s','^','D','v','P','x'];dash=['-','--','-','--','-','-.'];values=np.array(data['radar'],dtype=float)
 legend=[]
 for i in range(6):
  pts=values[i+1,:,None]/100*directions;pts=np.vstack([pts,pts[0]])
  ax.plot(pts[:,0],pts[:,1],color=baselines[i],lw=1.0,alpha=.86,ls=dash[i],marker=markers[i],ms=3.2,mew=.65,markerfacecolor='white' if i<5 else baselines[i],zorder=4+i*.1)
  legend.append(Line2D([],[],color=baselines[i],lw=1.15,ls=dash[i],marker=markers[i],ms=3.8,markerfacecolor='white' if i<5 else baselines[i],label=f'Baseline {i+1}'))
 pts=values[0,:,None]/100*directions;pts=np.vstack([pts,pts[0]])
 ax.fill(pts[:,0],pts[:,1],color=style['focus'],alpha=style['fill'],zorder=3)
 ax.plot(pts[:,0],pts[:,1],color='white',lw=3.9,zorder=9,solid_joinstyle='round')
 ax.plot(pts[:,0],pts[:,1],color=style['focus'],lw=2.15,marker='o',ms=4.6,markerfacecolor='white',mew=1.55,zorder=10,solid_joinstyle='round')
 legend.insert(0,Line2D([],[],color=style['focus'],lw=2.0,marker='o',ms=4.6,markerfacecolor='white',label='Candidate'))
 # Put grid labels between spokes, away from the colored task labels.
 for value in [20,40,60,80,100]:
  th=np.deg2rad(28);x=value/100*np.sin(th);y=value/100*np.cos(th)
  ax.text(x,y,str(value),fontsize=7.1,ha='center',va='center',color='#7e8d99',zorder=15,bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=.7))
 fig.legend(handles=legend,loc='lower center',bbox_to_anchor=(.5,.050),ncol=4,frameon=False,fontsize=8.0,handlelength=2.2,handletextpad=.65,columnspacing=1.4,labelspacing=.9)
 fig.text(.5,.020,'SYNTHETIC DATA  ·  identical data and 0–100 scale across designs',ha='center',va='center',fontsize=6.4,color='#89949d')
 stem='annular_radar_'+style['name']
 for ext in ['png','pdf','svg']:fig.savefig(out/(stem+'.'+ext),dpi=360,facecolor='white')
 fig.savefig(out/(stem+'_preview.png'),dpi=140,facecolor='white');plt.close(fig)

def overview(out):
 canvas=Image.new('RGB',(1800,1400),'#eef1f4');draw=ImageDraw.Draw(canvas)
 font=ImageFont.truetype('DejaVuSans.ttf',21)
 for i,s in enumerate(STYLES):
  x=i%3*600;y=i//3*700
  draw.rounded_rectangle((x+12,y+10,x+588,y+688),radius=15,fill='white')
  im=Image.open(out/('annular_radar_'+s['name']+'_preview.png')).convert('RGB');im.thumbnail((560,590));canvas.paste(im,(x+(600-im.width)//2,y+28))
  draw.text((x+300,y+645),f'{i+1:02d}  {s["title"]}',anchor='mm',font=font,fill='#344151')
 canvas.save(out/'radar_gallery_overview.png')

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--data',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 data=json.loads(a.data.read_text());v=np.array(data['radar'],dtype=float)
 if data.get('synthetic') is not True or v.shape!=(7,6) or not np.all(np.isfinite(v)) or np.any((v<0)|(v>100)):raise ValueError('Expected explicitly synthetic 7 × 6 radar scores in [0, 100].')
 plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})
 (a.out/'radar_data.json').write_text(json.dumps(dict(synthetic=True,seed=data.get('seed'),radar=data['radar']),indent=2))
 with (a.out/'radar_data.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['series',*[f'Task {chr(65+i)}' for i in range(6)]]);w.writerows(zip(['Candidate',*[f'Baseline {i}' for i in range(1,7)]],*v.T))
 for style in STYLES:render(data,a.out,style)
 overview(a.out);print('Generated 6 annular radar designs with identical data.')
if __name__=='__main__':main()
