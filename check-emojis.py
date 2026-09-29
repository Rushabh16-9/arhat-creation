import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Products' in line and 'tab-products' in line:
        for j in range(i-2, i+15):
            print(f'{j+1}: {repr(lines[j])}')
        break
