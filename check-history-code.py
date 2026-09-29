import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

if 'setShowHistory' in js:
    print('History code IS present in file!')
else:
    print('History code is MISSING!')
    
if 'Create New Bill (POS)' in js:
    import re
    matches = re.findall(r'Create New Bill \(POS\).*', js)
    for m in matches:
        print('Found:', repr(m))
