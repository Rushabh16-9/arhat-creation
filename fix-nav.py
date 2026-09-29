import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make the main-nav stand out more
css = css.replace(
    'background:rgba(255,255,255,0.9); border:1px solid var(--border);',
    'background:var(--surface); border:1px solid var(--border2); box-shadow: 0 8px 32px rgba(15, 23, 42, 0.08);'
)

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Nav bar updated!")
