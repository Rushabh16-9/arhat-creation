import os
import re

files_to_check = ['app/page.js', 'app/admin/page.js', 'app/layout.js']

for filepath in files_to_check:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace general text
        content = content.replace("Arhat Shop", "Arhat Creation")
        content = content.replace("arhat shop", "arhat creation")
        content = content.replace("ARHAT SHOP", "ARHAT CREATION")
        
        # Replace the wordmark specifically in page.js
        if filepath == 'app/page.js':
            content = content.replace('<span className="name">SHOP</span>', '<span className="name">CREATION</span>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Text replaced globally!")
