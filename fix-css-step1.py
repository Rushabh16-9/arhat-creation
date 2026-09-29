import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# First, let's remove existing media queries that are causing conflicts or are incomplete
css = re.sub(r'@media\s*\(\s*max-width\s*:\s*\d+px\s*\)\s*\{[^}]*\}', '', css, flags=re.DOTALL)
# The above regex doesn't handle nested braces well (like media queries). Let's be very careful.
# Actually, the media queries in this file are mostly at the end or have simple structures. Let's just find them and remove them manually.
