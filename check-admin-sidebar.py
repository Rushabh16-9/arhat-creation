import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'className="admin-sidebar"' in line or 'onClick={() => setActiveTab' in line:
        for j in range(max(0, i-2), min(i+15, len(lines))):
            print(f'{j+1}: {repr(lines[j])}')
        break
