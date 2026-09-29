import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '.admin-layout' in line or '.admin-sidebar' in line:
        print(f'{i+1}: {repr(line)}')
