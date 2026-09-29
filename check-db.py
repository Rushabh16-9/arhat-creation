import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/api/products/route.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    print(f'{i+1}: {repr(line)}')
