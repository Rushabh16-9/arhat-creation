import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
# Find any min-width or fixed width > 400px
widths = re.findall(r'[^}]*(?:width|min-width)\s*:\s*[4-9]\d{2}px[^}]*}', css)
for w in widths:
    print(w.strip())
