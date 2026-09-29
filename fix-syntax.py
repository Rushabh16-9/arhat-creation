with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
js = re.sub(r'    </svg>\n  \);\n\};\n\n\}\n', '    </svg>\n  );\n}\n', js)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Syntax error fixed!")
