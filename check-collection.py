import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Our Collection' in line:
        start = max(0, i-5)
        for j in range(start, start+40):
            try:
                print(f'{j+1}: {lines[j].strip()}')
            except:
                pass
        break
