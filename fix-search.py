with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

old_row_regex = r'<div style=\{\{\s*display:\s*\'flex\',\s*gap:\s*12,\s*marginBottom:\s*32,\s*flexWrap:\s*\'wrap\'\s*\}\}>(.*?)</div>\s*<div className="products-grid">'

new_row = """<div className="filter-row" style={{ display: 'flex', gap: 12, marginBottom: 32, flexWrap: 'wrap', alignItems: 'center' }}>
\\1
</div>
"""

# Let's just do a string replace on the wrapper and the input style
js = js.replace(
    "<div style={{ display: 'flex', gap: 12, marginBottom: 32, flexWrap: 'wrap' }}>",
    "<div className=\"filter-row\" style={{ display: 'flex', gap: 12, marginBottom: 32, flexWrap: 'wrap', alignItems: 'center' }}>"
)

js = js.replace(
    "style={{ flex: 1, minWidth: 200 }}",
    "style={{ flex: '1 1 200px' }} className=\"form-input search-input\""
)

# And remove the old className="form-input" which is now duplicated
js = js.replace('className="form-input"\n\nstyle={{ flex: \'1 1 200px\' }} className="form-input search-input"', 'style={{ flex: \'1 1 200px\' }} className="form-input search-input"')

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Page.js updated!")
