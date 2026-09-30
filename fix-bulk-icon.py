import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# The corrupted emoji might be '??' or literally something else.
if '?? Bulk' in js:
    js = js.replace('?? Bulk Upload', '{"\\uD83D\\uDCF8"} Bulk Upload')
    js = js.replace('?? Bulk', '{"\\uD83D\\uDCF8"} Bulk')
    
with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Icons fixed!")
