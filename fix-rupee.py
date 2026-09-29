with open('app/page.js', 'r', encoding='utf-8', errors='surrogatepass') as f:
    js = f.read()

# Replace \u20B9 literal with JSX expression {"\u20B9"} in ProductCard
js = js.replace('>\\u20B9{product.price', '>{"\\u20B9"}{product.price')
js = js.replace('>\\u20B9{product.original_price', '>{"\\u20B9"}{product.original_price')

# Also fix the one in MarqueeCarousel
js = js.replace('>\\u20B9{product.price', '>{"\\u20B9"}{product.price')

with open('app/page.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(js)

print("Fixed Rupee symbol rendering in ProductCard!")
