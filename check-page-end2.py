import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8', errors='surrogatepass') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines[-30:]):
    print(f'{len(lines) - 30 + i}: {line.rstrip()}')
