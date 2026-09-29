import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

replace_str = '''              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', padding: '0 4px' }}>
                <span style={{ fontSize: '15px', color: '#64748b', fontWeight: '500' }}>Total Amount</span>
                <span style={{ color: '#0f172a', fontSize: '24px', fontWeight: '800' }}>{"\u20B9"}{(product.price * qty).toLocaleString('en-IN')}</span>
              </div>
              
              <button className="buy-btn" onClick={handleBuyNow} disabled={product.stock === 0} style={{ width: '100%', padding: '16px', borderRadius: '16px', background: 'var(--primary)', color: '#fff', fontSize: '16px', fontWeight: '800', border: 'none', cursor: 'pointer', boxShadow: '0 8px 24px rgba(0, 150, 255, 0.3)', transition: 'all 0.2s', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }} onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = '0 12px 32px rgba(0, 150, 255, 0.4)'; }} onMouseOut={e => { e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 150, 255, 0.3)'; }}>
                {product.stock === 0 ? 'Out of Stock' : 'Order via WhatsApp'}
                {product.stock !== 0 && <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>}
              </button>
              <p style={{ fontSize: '12px', color: '#94a3b8', textAlign: 'center', marginTop: '16px', fontWeight: '500' }}>
                You will be redirected to WhatsApp to confirm your order
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );'''

js = re.sub(
    r'<div style=\{\{ display: \'flex\', justifyContent: \'space-between\', alignItems: \'center\', marginBottom: \'24px\', padding: \'0 4px\' \}\}>.*?\);\s*\}\s*function ProductCard',
    lambda _: replace_str + '\n}\n\nfunction ProductCard',
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed missing closing tags and restored Order button!")
