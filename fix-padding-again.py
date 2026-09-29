with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_pos = '<div className="admin-table-wrap" style={{ padding: \'24px\' }}>'
new_pos = '<div style={{ background: \'var(--surface)\', borderRadius: \'16px\', padding: \'32px\', border: \'1px solid var(--border)\', boxShadow: \'0 4px 12px rgba(0,0,0,0.02)\', boxSizing: \'border-box\', width: \'100%\' }}>'

js = js.replace(old_pos, new_pos)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Padding wrappers fixed again!")
