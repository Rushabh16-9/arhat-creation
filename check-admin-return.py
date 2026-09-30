import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'function AdminDashboard.*?return \(\s*<div className="admin-layout">(.*?)</div>\s*\);\s*\}', js, re.DOTALL)
if matches:
    content = matches.group(1)
    lines = content.split('\n')
    for i in range(min(150, len(lines))):
        print(f'{lines[i].strip()}')
