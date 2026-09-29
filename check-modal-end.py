import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(250, len(lines)):
    if 'function handleBuyNow' in lines[i]:
        for j in range(i+30, min(i+70, len(lines))):
            print(f'{j+1}: {repr(lines[j])}')
        break
