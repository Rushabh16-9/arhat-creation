with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# Update the Chat button display from inline-grid to flex
old_btn = r'<a href=\{`https://wa\.me/\$\{WA\}`\} target="_blank" rel="noopener noreferrer"\s*className="glow-btn nav-cta" id="nav-whatsapp-btn">'
new_btn = '<a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer" className="glow-btn nav-cta" id="nav-whatsapp-btn" style={{ display: \'flex\', alignItems: \'center\', gap: \'6px\', height: \'38px\', padding: \'0 16px\' }}>'

js = re.sub(old_btn, new_btn, js)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Chat button flex alignment fixed!")
