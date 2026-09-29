import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in [505, 506, 507, 508, 592, 593, 594, 595]:
    try:
        print(f'{i+1}: {lines[i].strip()}')
    except:
        pass
