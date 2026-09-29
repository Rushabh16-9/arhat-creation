import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'function BillingSystem\(\{ products, onUpdateStock, showToast \}\) \{.*?(// ===== ADMIN PAGE =====)', js, re.DOTALL)
if matches:
    print(matches.group(0)[:200])
    print('...')
    print(matches.group(0)[-200:])
else:
    print('Failed to find BillingSystem block!')
