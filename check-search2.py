import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="product-search"' in line:
        start = max(0, i-10)
        for j in range(start, i+5):
            try:
                print(f'{j+1}: {lines[j].strip()}')
            except:
                pass
        break
