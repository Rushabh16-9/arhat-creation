with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove stock label from ProductCard
js = js.replace('''<div style={{ position: 'absolute', top: '16px', left: '16px', background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(4px)', color: product.stock > 10 ? '#10b981' : product.stock > 0 ? '#f59e0b' : '#ef4444', padding: '4px 10px', borderRadius: '8px', fontSize: '11px', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.05em', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>{stockLabel}</div>''', '')

# Remove stock label from Product360Modal
js = js.replace('''<div className={`modal-stock ${stockStatus}`}>{stockLabel}</div>''', '')

# Remove stock from WhatsApp message in Product360Modal
js = js.replace('''        `\uD83D\uDCC8 *Stock Available:* ${product.stock > 0 ? product.stock + ' units' : 'Check availability'}`,
        '',\n''', '')

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Stock hidden from users!")
