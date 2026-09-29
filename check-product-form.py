import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<ProductForm' in line or 'ProductForm ' in line:
        start = max(0, i-2)
        for j in range(start, i+5):
            print(f'{j+1}: {repr(lines[j])}')
        break
