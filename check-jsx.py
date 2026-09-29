import sys

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Product360Modal' in line:
        start = i
        break

for i in range(start, min(start+100, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')

