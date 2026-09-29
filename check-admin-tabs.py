import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'<div className="admin-tabs".*?</nav>', js, re.DOTALL)
if matches:
    print(matches.group(0))

matches2 = re.search(r'\{activeTab === "products" && \(.*?\)\}', js, re.DOTALL)
if matches2:
    print("Found activeTab products block")
