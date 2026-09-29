import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the key property which lost its backticks
js = re.sub(r'key=\{mq-\$\{(.*?)\}-\$\{(.*?)\}\}', r'key={`mq-${\1}-${\2}`}', js)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed the missing backticks in the key property!")
