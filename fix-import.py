import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the import
js = js.replace(
    "import imglyRemoveBackground from '@imgly/background-removal';",
    "import { removeBackground as imglyRemoveBackground } from '@imgly/background-removal';"
)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed the import!")
