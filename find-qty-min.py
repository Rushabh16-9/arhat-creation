import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Math.min' in line and 'quantity' in line.lower():
        print(f'{i+1}: {line.strip()}')
    elif 'setQuantity(Math.min' in line:
        print(f'{i+1}: {line.strip()}')
