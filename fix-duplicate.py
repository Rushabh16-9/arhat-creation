with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the duplicate className
js = js.replace('className="form-input"\n\nstyle={{ flex: \'1 1 200px\' }} className="form-input search-input"', 'style={{ flex: \'1 1 200px\' }} className="form-input search-input"')

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Duplicate className fixed!")
