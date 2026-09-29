import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
lines = js.split('\n')
for i, line in enumerate(lines):
    if 'admin-mobile-nav' in line:
        for j in range(i, i+20):
            print(f'{j+1}: {repr(lines[j])}')
        break
