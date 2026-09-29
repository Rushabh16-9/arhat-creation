import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the className which was corrupted by Form Feed
# The corrupted string is "className={ilter-cat }" or something similar
# We will just replace it correctly

# We can search for 'className={\x0cilter-cat' or just 'className={'
# Since it's around line 506, let's just use regex to fix it.
content = re.sub(r'className=\{.*?ilter-cat.*?\}', r'className={`filter-cat ${selectedCategory === cat ? "active" : ""}`}', content)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("className fixed!")
