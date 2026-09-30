import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '.main-nav' in line:
        for j in range(max(0, i-2), i+15):
            print(f'{j+1}: {lines[j].strip()}')
        break
