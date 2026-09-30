import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'quantity' in line.lower() or 'qty' in line.lower():
        print(f'{i+1}: {line.strip()}')
