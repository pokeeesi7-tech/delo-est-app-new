#!/usr/bin/env python3
"""Generate shared DeloЕсть brand assets for web PWA and native Android builds."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys, shutil
mode=sys.argv[1] if len(sys.argv)>1 else 'all'
root=Path(sys.argv[2] if len(sys.argv)>2 else '.');root.mkdir(parents=True,exist_ok=True)
S=1024;COBALT=(182,230,76,255);MINT=(36,79,61,255);INK=(23,37,31,255);WHITE=INK
def icon(bg,mark,accent,size=512,outline=True):
 im=Image.new('RGBA',(S,S),(0,0,0,0));d=ImageDraw.Draw(im);d.rounded_rectangle((0,0,S-1,S-1),radius=220,fill=bg)
 if outline:d.rounded_rectangle((98,98,926,926),radius=190,outline=(accent[0],accent[1],accent[2],100),width=7)
 pts=[(278,532),(430,676),(740,356)];d.line(pts,fill=mark,width=86,joint='curve')
 for x,y in pts:
  r=43;d.ellipse((x-r,y-r,x+r,y+r),fill=mark)
 d.ellipse((690,190,790,290),fill=accent);return im.resize((size,size),Image.Resampling.LANCZOS)
def foreground(size=512):
 im=Image.new('RGBA',(S,S),(0,0,0,0));d=ImageDraw.Draw(im);pts=[(278,532),(430,676),(740,356)];d.line(pts,fill=WHITE,width=94,joint='curve')
 for x,y in pts:
  r=47;d.ellipse((x-r,y-r,x+r,y+r),fill=WHITE)
 d.ellipse((690,190,790,290),fill=MINT);return im.resize((size,size),Image.Resampling.LANCZOS)
def og(path):
 W,H=1200,630;im=Image.new('RGB',(W,H),(244,247,252));d=ImageDraw.Draw(im);d.ellipse((770,-260,1450,400),fill=(225,234,255));d.ellipse((900,170,1350,620),fill=(218,247,241))
 d.rounded_rectangle((80,76,182,178),radius=26,fill=COBALT);d.line([(106,128),(127,148),(157,108)],fill='white',width=12,joint='curve');d.ellipse((144,90,163,109),fill=MINT)
 bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 try:f1=ImageFont.truetype(bold,62);f2=ImageFont.truetype(regular,30);f3=ImageFont.truetype(bold,22);f4=ImageFont.truetype(bold,54)
 except Exception:f1=f2=f3=f4=ImageFont.load_default()
 d.text((210,91),'ДелоЕсть',font=f1,fill=(23,37,31));d.text((84,250),'Подработка рядом.',font=f4,fill=(23,37,31));d.text((84,322),'Исполнители — за пару минут.',font=f4,fill=(182,230,76));d.text((88,424),'Объявления  ·  Отклики  ·  Чат',font=f2,fill=(101,115,139));d.rounded_rectangle((84,512,385,572),radius=16,fill=(182,230,76));d.text((113,529),'Найти своё дело',font=f3,fill='white');im.save(path,optimize=True)
if mode in ('site','all'):
 im=Image.new('RGBA',(192,192),COBALT);d=ImageDraw.Draw(im);pts=[(52,100),(80,128),(142,63)];d.line(pts,fill='white',width=18,joint='curve')
 for x,y in pts:
  r=9;d.ellipse((x-r,y-r,x+r,y+r),fill='white')
 d.ellipse((132,35,151,54),fill=MINT);im.save(root/'icon-192.png',optimize=True)
 im=Image.new('RGBA',(512,512),COBALT);d=ImageDraw.Draw(im);pts=[(138,266),(216,345),(382,171)];d.line(pts,fill='white',width=45,joint='curve')
 for x,y in pts:
  r=23;d.ellipse((x-r,y-r,x+r,y+r),fill='white')
 d.ellipse((347,92,397,142),fill=MINT);im.save(root/'icon-512.png',optimize=True);og(root/'og-image.png');og(root/'og-image-1.png')
 print('Wrote PWA icon set and OG image to',root)
if mode in ('android','all'):
 icon(COBALT,WHITE,MINT).save(root/'icon.png',optimize=True);foreground().save(root/'icon_fg.png',optimize=True);icon(COBALT,WHITE,MINT).save(root/'icon_orange.png',optimize=True);icon(MINT,INK,WHITE).save(root/'icon_purple.png',optimize=True)
 assets=root/'assets';assets.mkdir(parents=True,exist_ok=True)
 for name in ('icon.png','icon_fg.png','icon_orange.png','icon_purple.png'):shutil.copyfile(root/name,assets/name)
 print('Wrote native app icon set to',root)
