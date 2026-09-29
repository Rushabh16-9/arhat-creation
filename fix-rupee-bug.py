with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix template literals (in the PDF generation)
js = js.replace('` + rupee + `', '\u20B9')

# Fix JSX text (in the React render blocks)
js = js.replace('\'\'\' + rupee + \'\'\'', '{"\u20B9"}')
js = js.replace('\'\'\' + close_icon + \'\'\'', '{"\u2715"}')

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Rupee bug fixed!")
