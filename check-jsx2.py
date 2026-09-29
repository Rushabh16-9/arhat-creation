import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Product360Modal' in line:
        start = i
        break

for i in range(180, min(start+200, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')

