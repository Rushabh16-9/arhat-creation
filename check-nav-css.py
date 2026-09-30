import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.search(r'\.nav-inner.*?\}', css, re.DOTALL)
if matches: print(matches.group(0))

matches = re.search(r'\.site-header.*?\}', css, re.DOTALL)
if matches: print(matches.group(0))

matches = re.search(r'\.nav-cta.*?\}', css, re.DOTALL)
if matches: print(matches.group(0))

matches = re.search(r'\.glow-btn.*?\}', css, re.DOTALL)
if matches: print(matches.group(0))
