with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# Remove the first className="form-input"
js = re.sub(r'className="form-input"\s*style=\{\{\s*flex:\s*\'1 1 200px\'\s*\}\}\s*className="form-input search-input"', 'style={{ flex: \'1 1 200px\' }} className="form-input search-input"', js)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Duplicate className fixed with regex!")
