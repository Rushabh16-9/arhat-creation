import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

count = js.count('function ProductCard')
print(f"ProductCard found {count} times")
