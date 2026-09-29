import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<h4>Place Your Order</h4>' in line:
        for j in range(max(0, i-2), i+15):
            print(f'{j+1}: {repr(lines[j])}')
        break
