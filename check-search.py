import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'<div className="collection-header">.*?</section>', js, re.DOTALL)
if matches:
    content = matches.group(0)
    lines = content.split('\n')
    for i in range(min(50, len(lines))):
        print(f'{i+1}: {lines[i].strip()}')
