import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'function ProductForm.*?return \(.*?</form>\s*</div>\s*\)', js, re.DOTALL)
if matches:
    content = matches.group(0)
    widths = re.findall(r'width\s*:\s*[4-9]\d{2}', content)
    for w in widths:
        print("Found width:", w)
    
    min_widths = re.findall(r'minWidth\s*:\s*[4-9]\d{2}', content)
    for w in min_widths:
        print("Found minWidth:", w)
