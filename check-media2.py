import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Get all media query blocks
import re
queries = [(m.start(), m.group(0)) for m in re.finditer(r'@media[^{]+\{', css)]
for start, q in queries:
    block = css[start:start+300]
    print(repr(block))
    print('---')
