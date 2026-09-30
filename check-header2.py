import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '.site-header' in line or '.nav-inner' in line:
        print(f'{i+1}: {line.strip()}')
