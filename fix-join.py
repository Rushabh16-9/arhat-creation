with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the broken join string
js = js.replace("].join('\n\n');", "].join('\\n');")

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed broken newline in join!")
