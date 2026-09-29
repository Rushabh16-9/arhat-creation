import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

if 'function BillingSystem' in js:
    print('BillingSystem IS present in file!')
else:
    print('BillingSystem is MISSING!')
