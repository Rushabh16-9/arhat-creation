import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'function ProductForm.*?return \((.*?)\)\s*\}', js, re.DOTALL)
if matches:
    content = matches.group(1)
    lines = content.split('\n')
    for line in lines:
        if 'gridTemplateColumns' in line or 'display: "grid"' in line or 'display: \'grid\'' in line or 'flex' in line:
            print(line.strip())
