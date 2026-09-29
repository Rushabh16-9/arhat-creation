import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix the Toast stretching issue
css = css.replace(
    '.toast {',
    '.toast {\n  height: max-content !important;\n  max-height: 60px !important;\n  display: flex !important;\n  align-items: center !important;\n'
)

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Toast height fixed!")
