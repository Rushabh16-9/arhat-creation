with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# Add the missing closing div for modal-gallery
js = js.replace('{/* Details Panel */}', '</div>\n\n{/* Details Panel */}')

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Missing div fixed!")
