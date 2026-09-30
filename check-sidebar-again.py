import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(910, 940):
    try:
        print(f'{j+1}: {lines[j].strip()}')
    except:
        pass
