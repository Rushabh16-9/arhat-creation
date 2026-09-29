import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the extremely corrupted key={mq--}
js = js.replace(
    '<div key={mq--} className="marquee-card"',
    '<div key={`mq-${product.id || i}-${i}`} className="marquee-card"'
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed the key property!")
