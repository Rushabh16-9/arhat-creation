import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'<nav className="nav">.*?</nav>', js, re.DOTALL)
if matches:
    print(matches.group(0))
