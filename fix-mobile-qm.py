import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('<div style={{ fontSize: \'20px\', marginBottom: \'4px\' }}>??</div>', '<div style={{ fontSize: \'20px\', marginBottom: \'4px\' }}>{"\\uD83D\\uDCF8"}</div>')

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Mobile icons fixed!")
