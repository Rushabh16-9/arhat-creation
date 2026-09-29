import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    js = f.read()

import re
if 'box-sizing' in js:
    print('Found box-sizing!')
    matches = re.findall(r'.*?box-sizing.*?', js)
    for m in matches:
        print(m.strip())
else:
    print('NO box-sizing globally!')
