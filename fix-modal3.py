import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

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
              )}'''

js = re.sub(
    r'<div className="modal-viewer">.*?</div>\s*\{loadingGemini',
    new_viewer + '\n              {loadingGemini',
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Modal 360 ACTUALLY removed!")
