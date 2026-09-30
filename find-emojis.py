import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
lines = js.split('\n')
for i, line in enumerate(lines):
    if 'Products' in line or 'Add Product' in line or 'Billing ' in line:
        if 'id="tab-' not in line and 'tab-products' not in line:
            print(f'{i+1}: {repr(line)}')
