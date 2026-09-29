# -*- coding: utf-8 -*-
with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Fix WhatsApp Message Template
old_msg_array = """const msg = [
        '\ud83d\uded2 *New Order - Arhat Shop*',
        '',
        `\ud83d\udce6 *Product:* ${product.name}`,
        `\ud83c\udff7\ufe0f *Category:* ${product.category || 'General'}`,
        `\ud83d\udcb0 *Price:* \u20b9${product.price.toLocaleString('en-IN')}${discount ? ` (${discount}% OFF)` : ''}`,
        `\ud83d\udd22 *Quantity:* ${qty}`,
        `\ud83d\udcb8 *Total:* \u20b9${(product.price * qty).toLocaleString('en-IN')}`,
        '',
        `\ud83d\udccd *Delivery Location:* ${location}`,
        '',
        `\ud83d\udcc8 *Stock Available:* ${product.stock > 0 ? product.stock + ' units' : 'Check availability'}`,
        '',
        `\u23f2\ufe0f *Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,
        '',
        '--- Sent via Arhat Shop ---'
      ].join('\\n');"""

import re
# Wait, let's just regex the msg block safely without escaping issues:
def repl_wa(m):
    return r"""const msg = [
        '\uD83D\uDED2 *New Order - Arhat Shop*',
        '',
        `\uD83D\uDCE6 *Product:* ${product.name}`,
        `\uD83C\uDFF7\uFE0F *Category:* ${product.category || 'General'}`,
        `\uD83D\uDCB0 *Price:* \u20B9${product.price.toLocaleString('en-IN')}${discount ? ` (${discount}% OFF)` : ''}`,
        `\uD83D\uDD22 *Quantity:* ${qty}`,
        `\uD83D\uDCB8 *Total:* \u20B9${(product.price * qty).toLocaleString('en-IN')}`,
        '',
        `\uD83D\uDCCD *Delivery Location:* ${location}`,
        '',
        `\uD83D\uDCC8 *Stock Available:* ${product.stock > 0 ? product.stock + ' units' : 'Check availability'}`,
        '',
        `\u23F2\uFE0F *Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,
        '',
        '--- Sent via Arhat Shop ---'
      ].join('\n');"""

js = re.sub(r'const msg = \[\s*(?:\'.*?\'|`.*?`)[^\]]*\].join\(\'\\n\'\);', repl_wa, js)


# 2. Fix Modal Viewer (Replace 360 with Gallery)
new_viewer = """            {/* Gallery Viewer */}
            <div className="modal-gallery" style={{ padding: '24px', background: 'var(--bg3)', borderRadius: '24px', marginBottom: '24px' }}>
              <div className="main-image-wrap" style={{ position: 'relative', width: '100%', aspectRatio: '1', borderRadius: '16px', overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,0.05)' }}>
                {(product.enhanced_image_url || product.image_url) ? (
                  <img
                    src={product.enhanced_image_url || product.image_url}
                    alt={product.name}
                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  />
                ) : (
                  <div style={{ width: '100%', height: '100%', background: 'linear-gradient(155deg,#1a2535,#0d1520)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 60 }}>\u2728</div>
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
            </div>"""

def repl_viewer(m):
    return new_viewer + "\n              {view360Data && ("

# The viewer starts at <div className="modal-viewer"> and ends right before {view360Data && (
js = re.sub(r'<div className="modal-viewer">.*?(?=\{view360Data \&\& \()', repl_viewer, js, flags=re.DOTALL)


# 3. Fix Price Row
new_price_row = """              <div className="modal-price-row" style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
                <span className="modal-price" style={{ fontSize: '28px', fontWeight: '800', color: 'var(--primary)' }}>\u20B9{product.price?.toLocaleString('en-IN')}</span>
                {product.original_price && (
                  <>
                    <span className="modal-orig-price" style={{ textDecoration: 'line-through', color: 'var(--text-dim)', fontSize: '18px', fontWeight: '600' }}>\u20B9{product.original_price.toLocaleString('en-IN')}</span>
                    <span className="modal-discount" style={{ background: '#10b981', color: '#fff', padding: '4px 10px', borderRadius: '8px', fontSize: '13px', fontWeight: '700' }}>
                      {Math.round((1 - product.price / product.original_price) * 100)}% OFF
                    </span>
                  </>
                )}
              </div>"""
def repl_price(m): return new_price_row
js = re.sub(r'<div className="modal-price-row">.*?</div>', repl_price, js, flags=re.DOTALL)


# 4. Fix Gemini Insights Styling
new_insights = """              {view360Data && (
                <div style={{ marginTop: '24px', padding: '16px 20px', background: 'linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%)', borderRadius: '16px', border: '1px solid rgba(0, 150, 255, 0.1)', width: '100%', boxShadow: '0 4px 12px rgba(0,0,0,0.03)' }}>
                  <div style={{ fontSize: '11px', letterSpacing: '0.15em', color: '#0369a1', textTransform: 'uppercase', marginBottom: '12px', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    \u2728 Gemini AI Insights
                  </div>
                  {view360Data.overallImpression && (
                    <p style={{ fontSize: '14px', color: '#334155', lineHeight: '1.6', fontWeight: '500', marginBottom: '12px' }}>
                      {view360Data.overallImpression}
                    </p>
                  )}
                  {view360Data.uniqueFeature && (
                    <p style={{ fontSize: '13px', color: '#0ea5e9', fontStyle: 'italic', fontWeight: '600', paddingLeft: '8px', borderLeft: '3px solid #38bdf8' }}>
                      {view360Data.uniqueFeature}
                    </p>
                  )}
                </div>
              )}"""

def repl_insights(m): return new_insights
js = re.sub(r'\{view360Data \&\& \(\s*<div.*?</p>\s*\)\}\s*</div>\s*\)\}', repl_insights, js, flags=re.DOTALL)


# 5. Remove 360 text from the product card buttons
js = re.sub(r'<span className="view-btn">View 360.*?</span>', '<span className="view-btn">View Details</span>', js)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("All fixes applied safely!")
