#!/usr/bin/env python3
"""Rebuild the icon contact sheet using Pillow and the bundled manifest."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'assets/manifest.json').read_text())
w,h,cols=170,142,6
sheet=Image.new('RGB',(w*cols,math.ceil(len(items)/cols)*h),'white');draw=ImageDraw.Draw(sheet)
font=ImageFont.load_default(size=16)
for i,r in enumerate(items):
 x=i%cols*w;y=i//cols*h
 icon=Image.open(root/'assets'/r['file']).convert('RGBA');icon=icon.crop(icon.getbbox());icon.thumbnail((72,80))
 sheet.paste(icon,(x+(w-icon.width)//2,y+14+(80-icon.height)//2),icon)
 draw.text((x+w/2,y+109),r['name'],font=font,fill='#303030',anchor='mm')
 draw.rectangle((x,y,x+w-1,y+h-1),outline='#e7e7e7')
sheet.save(root/'assets/catalog.png')
print(root/'assets/catalog.png')
