import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'export default function AdminPage' in line:
        for j in range(i, i+50):
            print(f'{j+1}: {repr(lines[j])}')
        break
