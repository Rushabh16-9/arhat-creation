with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Use unicode escapes to avoid powershell mangling
products_emoji = '\U0001F4E6'
add_emoji = '\u2795'
bill_emoji = '\U0001F9FE'

js = js.replace('?? Products', products_emoji + ' Products')
js = js.replace('? Add Product', add_emoji + ' Add Product')
js = js.replace('?? Billing ', bill_emoji + ' Billing ')

# Wait, there's another "? Add Product" on line 657, which was unaffected because it wasn't replaced by the bad script.
# Let's also check if "?? Add Product" was there? The log says `? Add Product`
js = js.replace('? Add Product', add_emoji + ' Add Product')

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Icons fixed!")
