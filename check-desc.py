import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<p className="modal-desc"' in line:
        for j in range(max(0, i-2), i+5):
            print(f'{j+1}: {repr(lines[j])}')
        break
