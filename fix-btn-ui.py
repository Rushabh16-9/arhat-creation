import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_label = '<label className="glow-btn" style={{ cursor: \'pointer\', display: \'inline-flex\' }}>'
new_label = '<label className="glow-btn" style={{ cursor: \'pointer\', display: \'inline-flex\', alignItems: \'center\', justifyContent: \'center\', height: \'48px\', padding: \'0 32px\', borderRadius: \'14px\', fontSize: \'15px\' }}>'

js = js.replace(old_label, new_label)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Button UI fixed!")
