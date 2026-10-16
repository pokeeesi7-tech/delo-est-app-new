#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import shutil,sys
mode=sys.argv[1] if len(sys.argv)>1 else 'all';root=Path(sys.argv[2] if len(sys.argv)>2 else '.');root.mkdir(parents=True,exist_ok=True)
L=(182,230,76,255);I=(23,37,31,255);F=(36,79,61,255);C=(244,245,239,255)
def mark(n,bg=L,fg=I):
 im=Image.new('RGBA',(n,n),bg);d=ImageDraw.Draw(im);d.rounded_rectangle((n*.06,n*.06,n*.94,n*.94),radius=n*.22,fill=bg);pts=[(n*.25,n*.52),(n*.42,n*.68),(n*.75,n*.32)];d.line(pts,fill=fg,width=max(4,int(n*.085)),joint='curve')
 for x,y in pts:r=n*.043;d.ellipse((x-r,y-r,x+r,y+r),fill=fg)
 d.ellipse((n*.68,n*.17,n*.79,n*.28),fill=F);return im
def og(p):
 im=Image.new('RGB',(1200,630),C[:3]);d=ImageDraw.Draw(im);d.ellipse((800,-280,1500,420),fill=(232,238,219));d.rounded_rectangle((78,70,174,166),radius=24,fill=L[:3]);d.line([(101,119),(121,139),(153,99)],fill=I[:3],width=10,joint='curve')
 try:b=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',58);m=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
 except OSError:b=m=ImageFont.load_default()
 d.text((198,88),'ДелоЕсть',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',48),fill=I[:3]);d.text((80,245),'Найди своё дело.',font=b,fill=I[:3]);d.text((83,326),'Подработка и заказы рядом',font=m,fill=F[:3]);d.text((83,385),'Понятная оплата. Прямой контакт.',font=m,fill=(104,118,108));im.save(p,optimize=True)
if mode in ('site','all'):
 mark(192).save(root/'icon-192.png',optimize=True);mark(512).save(root/'icon-512.png',optimize=True);og(root/'og-image.png');og(root/'og-image-1.png')
if mode in ('android','all'):
 mark(512).save(root/'icon.png',optimize=True);fg=Image.new('RGBA',(512,512),(0,0,0,0));d=ImageDraw.Draw(fg);pts=[(128,266),(214,348),(386,166)];d.line(pts,fill=I,width=46,joint='curve')
 for x,y in pts:r=23;d.ellipse((x-r,y-r,x+r,y+r),fill=I)
 d.ellipse((347,90,403,146),fill=F);fg.save(root/'icon_fg.png',optimize=True);mark(512,L,I).save(root/'icon_orange.png',optimize=True);mark(512,I,L).save(root/'icon_purple.png',optimize=True);(root/'assets').mkdir(exist_ok=True)
 for n in ('icon.png','icon_fg.png','icon_orange.png','icon_purple.png'):shutil.copyfile(root/n,root/'assets'/n)
print('Brand assets generated')
