# -*- coding: utf-8 -*-
import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the modal viewer (remove 360, add gallery)
new_viewer = '''            {/* Gallery Viewer */}
            <div className="modal-gallery" style={{ padding: '24px', background: 'var(--bg3)', borderRadius: '24px', marginBottom: '24px' }}>
              <div className="main-image-wrap" style={{ position: 'relative', width: '100%', aspectRatio: '1', borderRadius: '16px', overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,0.05)' }}>
                {(product.enhanced_image_url || product.image_url) ? (
                  <img
                    src={product.enhanced_image_url || product.image_url}
                    alt={product.name}
                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  />
                ) : (
                  <div style={{ width: '100%', height: '100%', background: 'linear-gradient(155deg,#1a2535,#0d1520)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 60 }}>\uD83D\uDCE6</div>
                )}
              </div>
              
              {/* Thumbnail Strip */}
              {(product.enhanced_image_url || product.image_url) && (
                <div style={{ display: 'flex', gap: '12px', marginTop: '16px', justifyContent: 'center' }}>
                  {[1, 2, 3].map(i => (
                    <div key={i} style={{ width: '64px', height: '64px', borderRadius: '10px', overflow: 'hidden', border: i === 1 ? '2px solid var(--primary)' : '1px solid var(--border)', cursor: 'pointer', opacity: i === 1 ? 1 : 0.6, transition: 'all 0.2s' }}>
                      <img src={product.enhanced_image_url || product.image_url} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                    </div>
                  ))}
                </div>
              )}
            </div>
'''

js = re.sub(
    r'\{\/\*\ 360 Viewer \*\/\}.*?(?=\{\/\*\ GEMINI INSIGHTS \*\/\})',
    new_viewer,
    js,
    flags=re.DOTALL
)

# Fix the price row in modal
new_price_row = '''              <div className="modal-price-row" style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
                <span className="modal-price" style={{ fontSize: '28px', fontWeight: '800', color: 'var(--primary)' }}>\u20B9{product.price?.toLocaleString('en-IN')}</span>
                {product.original_price && (
                  <>
                    <span className="modal-orig-price" style={{ textDecoration: 'line-through', color: 'var(--text-dim)', fontSize: '18px', fontWeight: '600' }}>\u20B9{product.original_price.toLocaleString('en-IN')}</span>
                    <span className="modal-discount" style={{ background: '#10b981', color: '#fff', padding: '4px 10px', borderRadius: '8px', fontSize: '13px', fontWeight: '700' }}>
                      {Math.round((1 - product.price / product.original_price) * 100)}% OFF
                    </span>
                  </>
                )}
              </div>'''

js = re.sub(
    r'<div className="modal-price-row">.*?</div>',
    new_price_row,
    js,
    flags=re.DOTALL
)

# Remove "View 360" button from product card and replace with View Details
js = re.sub(r'<span className="view-btn">View 360.*</span>', '<span className="view-btn">View Details</span>', js)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Modal 360 removed, gallery added, and price discount fixed!")
