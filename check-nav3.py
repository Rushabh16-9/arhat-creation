import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'<header className="site-header">.*?<div className="nav-actions">', js, re.DOTALL)
if matches:
    content = matches.group(0)
    lines = content.split('\n')
    for line in lines:
        print(line.strip())
