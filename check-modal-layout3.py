import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(260, 310):
    print(f'{i+1}: {repr(lines[i])}')
