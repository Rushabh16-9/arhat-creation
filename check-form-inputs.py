import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Product Name *' in line:
        start = max(0, i-5)
        for j in range(start, i+20):
            print(f'{j+1}: {lines[j].strip()}')
        break
