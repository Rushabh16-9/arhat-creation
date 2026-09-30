import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '?' in line and '??' not in line:
        start = max(0, i-1)
        for j in range(start, min(len(lines), start+3)):
            try:
                print(f'{j+1}: {lines[j].strip()}')
            except:
                pass
        print('---')
