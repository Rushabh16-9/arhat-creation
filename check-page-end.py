import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8', errors='surrogatepass') as f:
    lines = f.readlines()

for i, line in enumerate(lines[-150:]):
    print(f'{len(lines) - 150 + i}: {line.rstrip()}')
