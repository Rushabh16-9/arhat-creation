import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<div className="modal-inner">' in line:
        for j in range(max(0, i-5), min(i+50, len(lines))):
            print(f'{j+1}: {repr(lines[j])}')
        break
