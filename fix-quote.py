with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace(\"You'll be redirected\", \"You will be redirected\")

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print(\"Replaced single quote in You'll\")
