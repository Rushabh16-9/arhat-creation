import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(290, 325):
    try:
        print(f'{j+1}: {lines[j].strip()}')
    except:
        pass
