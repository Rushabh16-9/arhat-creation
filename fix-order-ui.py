import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_order_header = '''            <div className="order-section" style={{ background: '#fff', borderRadius: '24px', padding: '24px', boxShadow: '0 4px 20px rgba(0,0,0,0.04)', border: '1px solid #f1f5f9', marginTop: '32px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
                <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'var(--primary)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path><path d="M3 6h18"></path><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
                </div>
                <h4 style={{ margin: 0, fontSize: '18px', fontWeight: '800', color: '#0f172a' }}>Place Your Order</h4>
              </div>
              
              <div style={{ position: 'relative', marginBottom: '24px' }}>
                <div style={{ position: 'absolute', left: '16px', top: '16px', color: '#94a3b8' }}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                </div>
                <input
                  type="text"
                  placeholder="Enter your full delivery address..."
                  value={location}
                  onChange={e => setLocation(e.target.value)}
                  style={{ width: '100%', padding: '16px 16px 16px 48px', fontSize: '15px', color: '#334155', background: '#f8fafc', border: '1px solid #cbd5e1', borderRadius: '12px', outline: 'none', transition: 'all 0.2s', boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.02)' }}
                  onFocus={e => { e.currentTarget.style.background = '#fff'; e.currentTarget.style.borderColor = 'var(--primary)'; e.currentTarget.style.boxShadow = '0 0 0 4px rgba(0, 150, 255, 0.1)'; }}
                  onBlur={e => { e.currentTarget.style.background = '#f8fafc'; e.currentTarget.style.borderColor = '#cbd5e1'; e.currentTarget.style.boxShadow = 'inset 0 2px 4px rgba(0,0,0,0.02)'; }}
                />
              </div>'''

js = re.sub(
    r'<div className="order-section">\s*<h4>Place Your Order</h4>\s*<input\s*className="location-input"\s*type="text"\s*placeholder="Enter your full delivery address..."\s*value=\{location\}\s*onChange=\{e => setLocation\(e\.target\.value\)\}\s*/>',
    lambda _: new_order_header,
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Order section UI modernized!")
