import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = 0
for i, line in enumerate(lines):
    if 'function Product360Modal' in line:
        start = i
        break

for i in range(start, min(start+150, len(lines))):
    print(f'{i+1:3d}: {lines[i].rstrip()}')
