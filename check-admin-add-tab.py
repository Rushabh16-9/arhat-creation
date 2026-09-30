import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'activeTab === "add"' in line or 'onClick={() => setActiveTab("add")}' in line:
        start = max(0, i-5)
        for j in range(start, min(len(lines), i+15)):
            try:
                print(f'{j+1}: {lines[j].strip()}')
            except:
                pass
        print('---')
