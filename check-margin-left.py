import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.findall(r'.*?margin-left.*?', js)
for m in matches:
    print(m.strip())
    
matches = re.findall(r'.*?transform.*?', js)
for m in matches:
    print(m.strip())
