import re

with open('app/page.js', 'r', encoding='utf-8', errors='surrogatepass') as f:
    js = f.read()

new_card = '''function ProductCard({ product, onClick }) {
  const discount = product.original_price ? Math.round((1 - product.price / product.original_price) * 100) : 0;
  const stockLabel = product.stock > 10 ? 'In Stock' : product.stock > 0 ? `Only ${product.stock} left` : 'Out of Stock';

  return (
    <div className="product-card" onClick={onClick} role="button" tabIndex={0} onKeyDown={e => e.key === 'Enter' && onClick()} id={`product-${product.id}`} style={{ background: '#ffffff', borderRadius: '24px', overflow: 'hidden', border: '1px solid var(--border)', boxShadow: '0 4px 16px rgba(0,0,0,0.03)', cursor: 'pointer', display: 'flex', flexDirection: 'column', height: '100%', transition: 'all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1)' }} onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-6px)'; e.currentTarget.style.boxShadow = '0 20px 40px rgba(15,23,42,0.1)'; e.currentTarget.style.borderColor = 'rgba(0,150,255,0.2)'; }} onMouseOut={e => { e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.03)'; e.currentTarget.style.borderColor = 'var(--border)'; }}>
      <div style={{ position: 'relative', width: '100%', aspectRatio: '1', overflow: 'hidden', background: 'var(--bg2)' }}>
        {(product.enhanced_image_url || product.image_url) ? (
          <img src={product.enhanced_image_url || product.image_url} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'cover', transition: 'transform 0.5s' }} onMouseOver={e => e.currentTarget.style.transform = 'scale(1.05)'} onMouseOut={e => e.currentTarget.style.transform = 'none'} />
        ) : (
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 48 }}>\uD83D\uDCE6</div>
        )}
        {discount > 0 && <div style={{ position: 'absolute', top: '16px', right: '16px', background: '#ef4444', color: '#fff', padding: '4px 10px', borderRadius: '8px', fontSize: '13px', fontWeight: '800', boxShadow: '0 4px 12px rgba(239,68,68,0.25)' }}>-{discount}%</div>}
        <div style={{ position: 'absolute', top: '16px', left: '16px', background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(4px)', color: product.stock > 10 ? '#10b981' : product.stock > 0 ? '#f59e0b' : '#ef4444', padding: '4px 10px', borderRadius: '8px', fontSize: '11px', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.05em', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>{stockLabel}</div>
      </div>
      <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', flex: 1 }}>
        {product.category && (
          <div style={{ fontSize: '12px', letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--primary)', marginBottom: '8px', fontWeight: '800', opacity: 0.8 }}>
            {product.category}
          </div>
        )}
        <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#0f172a', marginBottom: '8px', lineHeight: '1.3' }}>{product.name}</h3>
        {product.description && (
          <p style={{ fontSize: '14px', color: '#64748b', lineHeight: '1.6', marginBottom: '16px', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>{product.description}</p>
        )}
        <div style={{ marginTop: 'auto', paddingTop: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
            <span style={{ fontSize: '24px', fontWeight: '800', color: 'var(--primary)' }}>\u20B9{product.price?.toLocaleString('en-IN')}</span>
            {product.original_price && (
              <span style={{ fontSize: '15px', fontWeight: '600', color: '#94a3b8', textDecoration: 'line-through' }}>\u20B9{product.original_price.toLocaleString('en-IN')}</span>
            )}
          </div>
          <button style={{ width: '100%', padding: '14px', borderRadius: '12px', background: '#f8fafc', border: '1px solid #e2e8f0', color: 'var(--primary)', fontSize: '15px', fontWeight: '700', cursor: 'pointer', transition: 'all 0.2s', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }} onMouseOver={e => { e.currentTarget.style.background = 'var(--primary)'; e.currentTarget.style.color = '#fff'; e.currentTarget.style.borderColor = 'var(--primary)'; }} onMouseOut={e => { e.currentTarget.style.background = '#f8fafc'; e.currentTarget.style.color = 'var(--primary)'; e.currentTarget.style.borderColor = '#e2e8f0'; }}>
            View Details
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
          </button>
        </div>
      </div>
    </div>
  );
}'''

js = re.sub(
    r'function ProductCard\(\{ product, onClick \}\) \{.*?\}(?=\n\n// ===== TOAST =====)',
    lambda _: new_card,
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(js)

print("ProductCard UI successfully updated!")
