import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = 0
for i, line in enumerate(lines):
    if 'function RingCarousel' in line:
        start = i
        break

for i in range(start, min(start+60, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
