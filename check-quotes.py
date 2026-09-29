import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
lines = js.split('\n')
for i, line in enumerate(lines):
    if 'You\'ll' in line or 'Youll' in line or 'doesn\'t' in line:
        print(f'{i+1}: {repr(line)}')
