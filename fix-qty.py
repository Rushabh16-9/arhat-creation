import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_code = '''              <div className="qty-row">
                <span>Quantity:</span>
                <div className="qty-controls">
                  <button onClick={() => setQty(q => Math.max(1, q - 1))}>\u2212</button>
                  <span>{qty}</span>
                  <button onClick={() => setQty(q => Math.min(product.stock || 99, q + 1))}>+</button>
                </div>
              </div>
              <div style={{ fontSize: 12, color: 'rgba(0,0,0,0.6)', marginBottom: 16 }}>
                Total: <strong style={{ color: '#000', fontSize: 15 }}>{"\u20B9"}{(product.price * qty).toLocaleString('en-IN')}</strong>
              </div>'''

new_code = '''              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', background: '#f8fafc', padding: '16px', borderRadius: '16px', border: '1px solid #e2e8f0' }}>
                <span style={{ fontSize: '15px', fontWeight: '700', color: '#334155' }}>Quantity</span>
                <div style={{ display: 'flex', alignItems: 'center', background: '#ffffff', borderRadius: '999px', border: '1px solid #cbd5e1', overflow: 'hidden', boxShadow: '0 2px 8px rgba(0,0,0,0.03)' }}>
                  <button onClick={() => setQty(q => Math.max(1, q - 1))} style={{ width: '40px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px', fontWeight: '500', color: '#475569', cursor: 'pointer', background: 'transparent', border: 'none', transition: 'background 0.2s' }} onMouseOver={e => e.currentTarget.style.background = '#f1f5f9'} onMouseOut={e => e.currentTarget.style.background = 'transparent'}>\u2212</button>
                  <span style={{ width: '40px', textAlign: 'center', fontSize: '16px', fontWeight: '800', color: '#0f172a' }}>{qty}</span>
                  <button onClick={() => setQty(q => Math.min(product.stock || 99, q + 1))} style={{ width: '40px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px', fontWeight: '500', color: '#475569', cursor: 'pointer', background: 'transparent', border: 'none', transition: 'background 0.2s' }} onMouseOver={e => e.currentTarget.style.background = '#f1f5f9'} onMouseOut={e => e.currentTarget.style.background = 'transparent'}>+</button>
                </div>
              </div>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', padding: '0 4px' }}>
                <span style={{ fontSize: '15px', color: '#64748b', fontWeight: '500' }}>Total Amount</span>
                <span style={{ color: '#0f172a', fontSize: '24px', fontWeight: '800' }}>{"\u20B9"}{(product.price * qty).toLocaleString('en-IN')}</span>
              </div>'''

# Wait, the file has double newlines in some places because of how lines were written. Let's just use re.sub with whitespace matching
js = re.sub(
    r'<div className="qty-row">.*?Total:.*?</div>\s*</div>',
    new_code,
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Quantity UI modernized!")
