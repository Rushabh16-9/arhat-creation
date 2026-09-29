import re

with open('app/api/gemini/route.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace gemini-2.5-flash with gemini-3.8-flash
js = js.replace('gemini-2.5-flash', 'gemini-3.8-flash')

with open('app/api/gemini/route.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Model updated to gemini-3.8-flash!")
