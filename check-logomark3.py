import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<svg className="nav-logo-mark"' in line:
        for j in range(i, i+25):
            print(f'{j+1}: {lines[j].strip()}')
        break
