import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'const [activeTab, setActiveTab] = useState' in line:
        for j in range(max(0, i-20), i+30):
            print(f'{j+1}: {repr(lines[j])}')
        break
