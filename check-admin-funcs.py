import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'function AdminPage\(\) \{.*?(const \[products, setProducts\] = useState\(\[\]\);)', js, re.DOTALL)
if matches:
    print(matches.group(1))

# Check for a stock update function
matches2 = re.search(r'function updateStock\(.*?\)', js, re.DOTALL)
if matches2:
    print('Found updateStock function')
else:
    print('No updateStock function')
