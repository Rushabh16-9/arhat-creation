with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("name: Product , unique_key:", "name: `Product ${i+1}`, unique_key:")

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed syntax error in page.js!")
