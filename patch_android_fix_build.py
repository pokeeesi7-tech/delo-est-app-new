#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
p=root/'landing.dart';s=p.read_text(encoding='utf-8')
old='side:BorderSide(color:p.bd))]\n    ]));'
new='side:BorderSide(color:p.bd)))]\n    ]));'
if old not in s:
    old='side:BorderSide(color:p.bd))]\n    ]));'
    if old not in s: raise SystemExit('Expected top bar IconButton ending not found')
s=s.replace(old,new,1);p.write_text(s,encoding='utf-8')
p=root/'widgets.dart';s=p.read_text(encoding='utf-8')
s=s.replace('? const SizedBox(\n                  width: 22, height: 22, child: CircularProgressIndicator(strokeWidth: 2.4, color: p.tx))','? SizedBox(\n                  width: 22, height: 22, child: CircularProgressIndicator(strokeWidth: 2.4, color: p.tx))')
p.write_text(s,encoding='utf-8')
print('Fixed the top bar bracket and dynamic spinner color')
