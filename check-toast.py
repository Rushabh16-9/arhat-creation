import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Find all blocks containing .toast
toast_blocks = re.findall(r'\.toast\s*\{[^}]*\}', css)
for block in toast_blocks:
    print(block)
    print("---")
