import re

with open('app/page.js', 'r', encoding='utf-8', errors='surrogatepass') as f:
    js = f.read()

# Let's print out all function declarations in the file
matches = re.findall(r'function \w+\(', js)
for m in matches:
    print(m)
