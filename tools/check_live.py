#!/usr/bin/env python3
"""Byte-check the public Pages deployment; commit or Actions success alone is not proof."""
from pathlib import Path
from urllib.request import urlopen,Request
import hashlib,time,sys
root=Path(__file__).resolve().parents[1]
base='https://aipmandy.github.io/HowToBeAnAICreator/'
for name in ['index.html','topic-lab.html','sitemap.xml','robots.txt']:
    expected=(root/'docs'/name).read_bytes()
    actual=b''
    for attempt in range(12):
        try:
            with urlopen(Request(base+name,headers={'User-Agent':'creator-live-check/1.0','Cache-Control':'no-cache'}),timeout=15) as resp:
                if resp.status!=200:raise RuntimeError(str(resp.status))
                actual=resp.read()
            if actual==expected:break
        except Exception as exc:print('retry:',name,str(exc))
        if attempt<11:time.sleep(10)
    if actual!=expected:
        print('MISMATCH:',name,'expected',hashlib.sha256(expected).hexdigest(),'got',hashlib.sha256(actual).hexdigest())
        sys.exit(1)
    print('PASS',base+name,hashlib.sha256(expected).hexdigest())
print('All 4 Pages resources byte-identical')
