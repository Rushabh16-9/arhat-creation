import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re
matches = re.search(r'\{loading \? \(.*?\) : activeTab === "bill" && !showForm \? \(.*?\) : activeTab === "products" && !showForm \? \(.*?<div className="admin-table-wrap">.*?(</main>)', "".join(lines), re.DOTALL)
if matches:
    print(matches.group(0)[-200:])
else:
    print("Match failed")
