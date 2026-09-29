import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<div className="order-section">' in line:
        for j in range(i, i+30):
            print(f'{j+1}: {repr(lines[j])}')
        break
