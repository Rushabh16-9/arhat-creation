import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.search(r'function BulkUploadForm', js)
if matches:
    print("BulkUploadForm exists in the file!")
else:
    print("BulkUploadForm DOES NOT exist in the file!")
    
matches = re.search(r'export default function (\w+)', js)
if matches:
    print(f"Default export component is: {matches.group(1)}")
