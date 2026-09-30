import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'const AdminDashboard.*?return', js, re.DOTALL)
if matches:
    content = matches.group(0)
    lines = content.split('\n')
    for i in range(min(50, len(lines))):
        print(f'{i+1}: {lines[i].strip()}')
