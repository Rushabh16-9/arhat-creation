import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Find any existing media queries
import re
queries = re.findall(r'@media[^{]+\{', css)
for q in queries:
    print(repr(q))
