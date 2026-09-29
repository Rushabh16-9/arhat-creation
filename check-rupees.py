import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'BillingSystem' in line or 'Add Product to Bill' in line or 'removeFromCart' in line:
        pass
    if '?{' in line or '} ?' in line or ' ?' in line or '>?' in line or '(?{' in line or '>{item.product.name}</div>' in line:
        pass
    if 'option key=' in line or 'item.product.price' in line or 'total.toLocaleString' in line:
        print(f'{i+1}: {repr(line)}')
