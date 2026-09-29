import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove the duplicate
js = js.replace(
    "{view360Data && (              {view360Data && (",
    "{view360Data && ("
)
# Just in case the whitespace varies slightly
js = re.sub(
    r'\{view360Data \&\& \(\s*\{view360Data \&\& \(',
    '{view360Data && (',
    js
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed the duplicate curly brace!")
