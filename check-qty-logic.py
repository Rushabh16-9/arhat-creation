import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'setQuantity(' in line or 'handleQuantityChange' in line or '<button' in line and 'setQuantity' in line:
        start = max(0, i-5)
        for j in range(start, i+5):
            try:
                print(f'{j+1}: {lines[j].rstrip()}')
            except:
                pass
        print("---")
