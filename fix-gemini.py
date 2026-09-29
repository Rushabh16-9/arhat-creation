import re

with open('app/api/gemini/route.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace gemini-2.0-flash-exp with gemini-1.5-flash
js = js.replace('gemini-2.0-flash-exp', 'gemini-1.5-flash')

with open('app/api/gemini/route.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Model updated to gemini-1.5-flash!")
