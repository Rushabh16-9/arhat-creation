import re

with open('app/api/gemini/route.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace gemini-1.5-flash with gemini-2.5-flash
js = js.replace('gemini-1.5-flash', 'gemini-2.5-flash')

with open('app/api/gemini/route.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Model updated to gemini-2.5-flash!")
