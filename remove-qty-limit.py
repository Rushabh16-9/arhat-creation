with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the Math.min check with just q + 1
old_str = "setQty(q => Math.min(product.stock || 99, q + 1))"
new_str = "setQty(q => q + 1)"
js = js.replace(old_str, new_str)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Quantity limit removed!")
