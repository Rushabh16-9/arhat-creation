import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'function LogoMark' in line:
        start = max(0, i)
        for j in range(start, start+25):
            print(f'{j+1}: {repr(lines[j])}')
        break
