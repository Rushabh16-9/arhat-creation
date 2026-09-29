import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '.admin-content {' in line or '.admin-content{' in line:
        for j in range(i, i+5):
            print(f'{j+1}: {repr(lines[j])}')
        break
