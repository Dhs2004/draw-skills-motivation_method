#!/usr/bin/env python3
"""Nine vector axonometric bar designs. Linear normalized heights, same data.
Requires numpy, matplotlib, Pillow. Affine parallel projection avoids near/far scaling.
"""
import argparse,json,csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import to_rgb
from PIL import Image,ImageDraw,ImageFont
STYLES=[
 dict(name='balanced_isometric',title='Balanced Isometric',bx=(1,-.23),by=(.62,.68),z=1.22,gap=2.1,palette=['#a9b9a8','#78a7a3','#7998ba','#c48d89']),
 dict(name='frontal_oblique',title='Frontal Oblique',bx=(1,0),by=(.65,.75),z=1.20,gap=2.0,palette=['#99bac6','#91a4c4','#b1a0c4','#c9a7b1']),
 dict(name='elevated_grid',title='Elevated Grid',bx=(1,-.39),by=(.55,.85),z=1.00,gap=1.8,palette=['#b0c3b3','#84b0a8','#789dab','#8a91b4']),
 dict(name='architectural',title='Architectural',bx=(1,-.12),by=(.34,.90),z=1.20,gap=1.8,palette=['#c7bea9','#a9b8b3','#889faf','#aa99ab']),
 dict(name='wide_isometric',title='Wide Isometric',bx=(.93,-.40),by=(.85,.48),z=1.00,gap=2.65,palette=['#a7b7cd','#78a4bd','#8eaaa3','#c8ac8c']),
 dict(name='terraced_rows',title='Terraced Rows',bx=(1,0),by=(.20,1.0),z=.96,gap=1.65,palette=['#abc7cd','#8caaba','#a5a7c3','#bf9dae']),
 dict(name='compact_parallel',title='Compact Parallel',bx=(1,-.17),by=(.46,.76),z=1.10,gap=1.9,palette=['#b8bca4','#8fb5a5','#7c9caf','#b698aa']),
 dict(name='porcelain_perspective',title='Porcelain Axonometric',bx=(1,-.30),by=(.70,.68),z=1.10,gap=2.1,palette=['#b4ccca','#a6bfca','#b8b8d0','#d1b6c2']),
 dict(name='slate_copper',title='Slate & Copper',bx=(1,-.08),by=(.48,.82),z=1.18,gap=1.9,palette=['#829aa9','#9baeb9','#bcaea1','#c3937d']),
]

def tint(c,v):
 a=np.array(to_rgb(c));return tuple(a+(1-a)*v) if v>=0 else tuple(a*(1+v))

def plot(d,out,cfg):
 raw=np.array(d['sensitivity'],float);norm=raw/raw.max(axis=1,keepdims=True)
 bx=np.array(cfg['bx']);by=np.array(cfg['by']);bz=np.array([0,cfg['z']]);step=1.45;gap=cfg['gap'];w=.78;depth=.62
 def project(x,y,z=0):return x*bx+y*by+z*bz
 def poly(points,**kw):ax.add_patch(Polygon([project(*p) for p in points],closed=True,**kw))
 fig=plt.figure(figsize=(8.0,6.5));ax=fig.add_axes([.06,.13,.87,.79]);ax.set_aspect('equal');ax.axis('off')
 xmax=3*step+w+.17;ymax=3*gap+depth
 corners=np.array([project(x,y,z) for x in [-.7,xmax+1.6] for y in [-.95,ymax+.3] for z in [0,1.30]])
 ax.set_xlim(corners[:,0].min(),corners[:,0].max());ax.set_ylim(corners[:,1].min(),corners[:,1].max())
 # Low-contrast floor strips preserve row membership without an enclosing cage.
 for j in reversed(range(4)):
  y=j*gap;c=cfg['palette'][j]
  poly([(-.14,y-.08,0),(xmax,y-.08,0),(xmax,y+depth+.10,0),(-.14,y+depth+.10,0)],facecolor=tint(c,.91),edgecolor=tint(c,.53),lw=.55,zorder=1)
  for k in range(4):
   p=project(k*step,y-.08);q=project(k*step,y+depth+.10);ax.plot([p[0],q[0]],[p[1],q[1]],color=tint(c,.64),lw=.4,zorder=2)
  xy=project(xmax+.22,y+depth*.40)
  ax.text(*xy,f'Metric {chr(65+j)}',fontsize=9.4,fontweight='normal',ha='left',va='center',color=tint(c,-.42),zorder=70)
  # A faint zero-plane rule makes the local base of each row legible.
  p=project(-.14,y,0);q=project(xmax,y,0);ax.plot([p[0],q[0]],[p[1],q[1]],color=tint(c,.38),lw=.65,zorder=3)
 # Draw far rows first. All bars retain identical footprint and vertical scale.
 for j in reversed(range(4)):
  for k in range(4):
   x=k*step;y=j*gap;h=norm[j,k];c=cfg['palette'][j];order=10+(3-j)*10+k*.2
   poly([(x,y,0),(x+w,y,0),(x+w,y,h),(x,y,h)],facecolor=c,edgecolor=tint(c,-.37),lw=.65,zorder=order)
   poly([(x+w,y,0),(x+w,y+depth,0),(x+w,y+depth,h),(x+w,y,h)],facecolor=tint(c,-.18),edgecolor=tint(c,-.37),lw=.65,zorder=order+.05)
   poly([(x,y,h),(x+w,y,h),(x+w,y+depth,h),(x,y+depth,h)],facecolor=tint(c,.40),edgecolor=tint(c,-.30),lw=.6,zorder=order+.1)
   xy=project(x+w*.50,y+depth*.50,h);xy[1]+=.095
   ax.text(*xy,f'{raw[j,k]:.1f}',ha='center',va='bottom',fontsize=9.0,color='#3a4854',zorder=85,bbox=dict(facecolor='white',edgecolor='none',alpha=.88,pad=1.0))
 # A common normalized vertical axis, separate from raw-score top labels.
 base=project(-.45,0,0);top=project(-.45,0,1.1)
 ax.plot([base[0],top[0]],[base[1],top[1]],color='#768695',lw=.8,zorder=90)
 for value in [0,.5,1.0]:
  xy=project(-.45,0,value);ax.plot([xy[0]-.06,xy[0]],[xy[1],xy[1]],color='#768695',lw=.7,zorder=90);ax.text(xy[0]-.10,xy[1],f'{value:g}×',ha='right',va='center',fontsize=8,color='#637584',zorder=90)
 for k,label in enumerate(['0','5','10','20']):
  xy=project(k*step+w/2,-.40);ax.text(*xy,label,ha='center',va='top',fontsize=9.4,color='#536675')
 xy=project((xmax-.14)/2,-.40);xy[1]=min(project(k*step+w/2,-.40)[1] for k in range(4))-.46;ax.text(*xy,'Parameter setting',ha='center',va='top',fontsize=10.3,color='#455a6a')
 fig.text(.08,.962,'NORMALIZED SCORE',ha='left',va='top',fontsize=10.3,fontweight='bold',color='#354c5b')
 fig.text(.08,.925,'Bar height: score / metric maximum     ·     Labels: raw score',ha='left',va='top',fontsize=8.0,color='#7b8993')
 fig.text(.95,.025,'SYNTHETIC DATA · identical values across all nine designs',ha='right',fontsize=7,color='#8b969e')
 fig.canvas.draw()
 renderer=fig.canvas.get_renderer();texts=[t for t in ax.texts if t.get_visible()];collisions=[]
 for i,t in enumerate(texts):
  for u in texts[i+1:]:
   if t.get_window_extent(renderer).overlaps(u.get_window_extent(renderer)):collisions.append([t.get_text(),u.get_text()])
 if collisions:raise ValueError(f'{cfg["name"]}: text overlaps {collisions}')
 stem='normalized_3d_bar_'+cfg['name']
 for ext in ['png','pdf','svg']:fig.savefig(out/(stem+'.'+ext),dpi=360,facecolor='white')
 fig.savefig(out/(stem+'_preview.png'),dpi=135,facecolor='white');plt.close(fig)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--data',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);d=json.loads(a.data.read_text());v=np.array(d['sensitivity'],float)
 if d.get('synthetic') is not True or v.shape!=(4,4) or not np.all(np.isfinite(v)) or np.any(v<=0):raise ValueError('Expected a positive 4×4 synthetic sensitivity array.')
 plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none'})
 (a.out/'normalized_3d_bar_data.json').write_text(json.dumps(dict(synthetic=True,seed=d.get('seed'),sensitivity=d['sensitivity'],normalization='raw / maximum over settings within each metric'),indent=2))
 with (a.out/'normalized_3d_bar_data.csv').open('w',newline='') as f:
  wr=csv.writer(f);wr.writerow(['metric','setting','raw_score','normalized_height'])
  for j in range(4):
   for k,setting in enumerate([0,5,10,20]):wr.writerow([f'Metric {chr(65+j)}',setting,v[j,k],v[j,k]/v[j].max()])
 for cfg in STYLES:plot(d,a.out,cfg)
 canvas=Image.new('RGB',(1800,1620),'#edf1f3');draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('DejaVuSans.ttf',20)
 for i,cfg in enumerate(STYLES):
  x=i%3*600;y=i//3*540;draw.rounded_rectangle((x+10,y+10,x+590,y+530),radius=13,fill='white');im=Image.open(a.out/('normalized_3d_bar_'+cfg['name']+'_preview.png')).convert('RGB');im.thumbnail((570,462));canvas.paste(im,(x+(600-im.width)//2,y+20));draw.text((x+300,y+499),cfg['title'],font=font,anchor='mm',fill='#3d5260')
 canvas.save(a.out/'normalized_3d_bar_gallery_overview.png');print('Rendered 9 axonometric bar designs.')
if __name__=='__main__':main()
