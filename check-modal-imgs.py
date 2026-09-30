import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'modal-inner' in line or 'modal-viewer' in line or 'thumbnail' in line.lower() or 'gallery' in line.lower():
        start = max(0, i-5)
        for j in range(start, i+5):
            try:
                pass
            except:
                pass
