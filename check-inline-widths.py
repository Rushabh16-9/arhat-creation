import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
widths = re.findall(r'width[^\}]*[4-9]\d{2}', js)
for w in widths:
    print(w)

min_widths = re.findall(r'minWidth[^\}]*[3-9]\d{2}', js)
for w in min_widths:
    print(w)
