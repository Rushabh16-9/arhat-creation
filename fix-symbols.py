import sys

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

rupee = '\u20B9'
close_icon = '\u2715'

js = js.replace(
    '<option key={p.id} value={p.id}>{p.name} (?{p.price}) - {p.stock} in stock</option>',
    '<option key={p.id} value={p.id}>{p.name} (' + rupee + '{p.price}) - {p.stock} in stock</option>'
)

js = js.replace(
    '<div style={{ fontSize: \'13px\', color: \'var(--text-muted)\' }}>?{item.product.price} x {item.qty}</div>',
    '<div style={{ fontSize: \'13px\', color: \'var(--text-muted)\' }}>' + rupee + '{item.product.price} x {item.qty}</div>'
)

js = js.replace(
    '<div style={{ fontWeight: \'700\' }}>?{(item.product.price * item.qty).toLocaleString(\'en-IN\')}</div>',
    '<div style={{ fontWeight: \'700\' }}>' + rupee + '{(item.product.price * item.qty).toLocaleString(\'en-IN\')}</div>'
)

js = js.replace(
    '<button onClick={() => removeFromCart(item.product.id)} style={{ background: \'none\', border: \'none\', color: \'var(--red)\', cursor: \'pointer\', fontSize: \'18px\' }}>?</button>',
    '<button onClick={() => removeFromCart(item.product.id)} style={{ background: \'none\', border: \'none\', color: \'var(--red)\', cursor: \'pointer\', fontSize: \'18px\' }}>' + close_icon + '</button>'
)

js = js.replace(
    '<div style={{ fontSize: \'24px\', fontWeight: \'800\', color: \'var(--primary)\' }}>?{total.toLocaleString(\'en-IN\')}</div>',
    '<div style={{ fontSize: \'24px\', fontWeight: \'800\', color: \'var(--primary)\' }}>' + rupee + '{total.toLocaleString(\'en-IN\')}</div>'
)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Symbols fixed!")
