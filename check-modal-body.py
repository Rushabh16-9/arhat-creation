import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'\{product && \(\s*<div className="modal-backdrop".*?</Dialog\.Panel>\s*</div>\s*</div>\s*\)\}', js, re.DOTALL)
if matches:
    print(matches.group(0))
else:
    print("Not found regex 1")
    matches = re.search(r'\{product && \(\s*<div.*?modal.*?\}', js, re.DOTALL)
    if matches:
        print(matches.group(0)[:1000])

