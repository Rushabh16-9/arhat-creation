import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Print all CSS class names related to store page
import re
classes = re.findall(r'\.(hero[^{,\s]*|nav[^{,\s]*|product[^{,\s]*|modal[^{,\s]*|store[^{,\s]*|admin[^{,\s]*|sidebar[^{,\s]*|checkout[^{,\s]*|qty[^{,\s]*)\s*\{', css)
for c in sorted(set(classes)):
    print(c)
