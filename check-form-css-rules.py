import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.search(r'\.form-field.*?\}', css, re.DOTALL)
if matches:
    print(matches.group(0))

matches = re.search(r'\.form-label.*?\}', css, re.DOTALL)
if matches:
    print(matches.group(0))
