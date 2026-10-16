#!/usr/bin/env python3
from pathlib import Path
import re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else ".")
def rw(name,fn):
 p=root/name
 if not p.exists():raise SystemExit("Missing "+str(p))
 s=p.read_text(encoding="utf-8");s=fn(s);p.write_text(s,encoding="utf-8")
def theme(s):
 pairs={
 "0xFFFDF8F3":"0xFFF4F7FC","0xFFF7EFE6":"0xFFEAF0F8","0xFF1B1530":"0xFF152039","0xFF6B6480":"0xFF65738B","0xFFEADFD3":"0xFFDCE4F0","0xFFFF5A36":"0xFF405CF5","0xFFFF9F1C":"0xFF19B99A","0xFF0A0E1F":"0xFF0A1120","0xFF0E1429":"0xFF111D30","0xFF121833":"0xFF142138","0xFFEEF1FF":"0xFFF2F6FC","0xFF9AA3C7":"0xFFA1B0C6","0xFF232B52":"0xFF283850","0xFF7C5CFF":"0xFF8EA2FF","0xFF22D3EE":"0xFF4AD8BD","0xFF4ADE80":"0xFF4BE0B2","0xFFFF7B84":"0xFFFF8491"}
 for a,b in pairs.items():s=s.replace(a,b)
 if "fontFamily: 'Roboto'" not in s:s=s.replace("useMaterial3: true,","useMaterial3: true,\n    fontFamily: 'Roboto',",1)
 return s
rw("theme.dart",theme)
def home(s):
 s=s.replace("height: 64,","height: 68,",1)
 s=s.replace("duration: const Duration(milliseconds: 160),","duration: const Duration(milliseconds: 190),\n                      curve: Curves.easeOutCubic,",1)
 s=s.replace("border: Border(top: BorderSide(color: p.bd)),","border: Border(top: BorderSide(color: p.bd)),\n        boxShadow: [BoxShadow(color: p.tx.withOpacity(.035), blurRadius: 18, offset: const Offset(0, -5))],",1)
 return s
rw("home.dart",home)
def widgets(s):
 s=s.replace("borderRadius: BorderRadius.circular(20),","borderRadius: BorderRadius.circular(18),",1)
 s=s.replace("duration: const Duration(milliseconds: 140),","duration: const Duration(milliseconds: 180),",1)
 return s
rw("widgets.dart",widgets)
print("Applied Studio visual system to Flutter source")
