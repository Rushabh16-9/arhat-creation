with open('app/page.js', 'r', encoding='utf-8', errors='surrogatepass') as f:
    js = f.read()

modal_code = '''
// ===== PRODUCT 360 MODAL =====
function Product360Modal({ product, onClose }) {
  const [location, setLocation] = useState('');
  const [qty, setQty] = useState(1);
  const [view360Data, setView360Data] = useState(null);
  const [loadingGemini, setLoadingGemini] = useState(false);
  const WA = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '919082799791';

  useEffect(() => {
    document.body.style.overflow = 'hidden';
    if ((product.image_url || product.enhanced_image_url) && !view360Data) {
      load360Description();
    }
    return () => { document.body.style.overflow = ''; };
  }, []);

  async function load360Description() {
    try {
      setLoadingGemini(true);
      const imgUrl = product.enhanced_image_url || product.image_url;
      const imgResp = await fetch(imgUrl);
      const blob = await imgResp.blob();
      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64 = e.target.result.split(',')[1];
        const res = await fetch('/api/gemini', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'generate360Description', imageBase64: base64, mimeType: blob.type })
        });
        const data = await res.json();
        if (data.success) setView360Data(data.data);
      };
      reader.readAsDataURL(blob);
    } catch (err) {
      console.log('360 description failed:', err);
    } finally {
      setLoadingGemini(false);
    }
  }

  function handleBuyNow() {
    if (!location.trim()) {
      alert('Please enter your delivery location');
      return;
    }
    const discount = product.original_price ? Math.round((1 - product.price / product.original_price) * 100) : 0;
    const msg = [
        '\\uD83D\\uDED2 *New Order - Arhat Shop*',
        '',
        `\\uD83D\\uDCE6 *Product:* ${product.name}`,
        `\\uD83C\\uDFF7\\uFE0F *Category:* ${product.category || 'General'}`,
        `\\uD83D\\uDCB0 *Price:* {"\\u20B9"}${product.price.toLocaleString('en-IN')}${discount ? ` (${discount}% OFF)` : ''}`,
        `\\uD83D\\uDD22 *Quantity:* ${qty}`,
        `\\uD83D\\uDCB8 *Total:* {"\\u20B9"}${(product.price * qty).toLocaleString('en-IN')}`,
        '',
        `\\uD83D\\uDCCD *Delivery Location:* ${location}`,
        '',
        `\\uD83D\\uDCC8 *Stock Available:* ${product.stock > 0 ? product.stock + ' units' : 'Check availability'}`,
        '',
        `\\u23F2\\uFE0F *Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,
        '',
        '--- Sent via Arhat Shop ---'
      ].join('\\n');
    const url = `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank');
  }

  const stockStatus = product.stock > 10 ? 'good' : product.stock > 0 ? 'low' : 'none';
  const stockLabel = product.stock > 10 ? `\\u2713 In Stock (${product.stock} units)` : product.stock > 0 ? `\\u26A0 Only ${product.stock} left` : '\\u2715 Out of Stock';

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal-box" style={{ position: 'relative' }}>
        <button className="modal-close" onClick={onClose} aria-label="Close modal">\\u2715</button>
        <div className="modal-inner">
          
          {/* Gallery Viewer */}
          <div className="modal-gallery" style={{ padding: '24px', background: 'var(--bg3)', borderRadius: '24px', marginBottom: '24px' }}>
            <div className="main-image-wrap" style={{ position: 'relative', width: '100%', aspectRatio: '1', borderRadius: '16px', overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,0.05)' }}>
              {(product.enhanced_image_url || product.image_url) ? (
                <img src={product.enhanced_image_url || product.image_url} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              ) : (
                <div style={{ width: '100%', height: '100%', background: 'linear-gradient(155deg,#1a2535,#0d1520)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 60 }}>\\u2728</div>
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
          
          {/* AI Insights Card */}
          {view360Data && (
            <div style={{ marginTop: '24px', padding: '16px 20px', background: 'linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%)', borderRadius: '16px', border: '1px solid rgba(0, 150, 255, 0.1)', width: '100%', boxShadow: '0 4px 12px rgba(0,0,0,0.03)' }}>
              <div style={{ fontSize: '11px', letterSpacing: '0.15em', color: '#0369a1', textTransform: 'uppercase', marginBottom: '12px', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '6px' }}>
                \\u2728 Gemini AI Insights
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
          )}

          {/* Details Panel */}
          <div className="modal-details">
            {product.category && <div className="modal-category">{product.category}</div>}
            <h2 className="modal-title">{product.name}</h2>
            {product.description && (
              <p className="modal-desc">{product.description}</p>
            )}
            <div className="modal-price-row" style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
              <span className="modal-price" style={{ fontSize: '28px', fontWeight: '800', color: 'var(--primary)' }}>{"\\u20B9"}{product.price?.toLocaleString('en-IN')}</span>
              {product.original_price && (
                <>
                  <span className="modal-orig-price" style={{ textDecoration: 'line-through', color: 'var(--text-dim)', fontSize: '18px', fontWeight: '600' }}>{"\\u20B9"}{product.original_price.toLocaleString('en-IN')}</span>
                  <span className="modal-discount" style={{ background: '#10b981', color: '#fff', padding: '4px 10px', borderRadius: '8px', fontSize: '13px', fontWeight: '700' }}>
                    {Math.round((1 - product.price / product.original_price) * 100)}% OFF
                  </span>
                </>
              )}
            </div>
            <div className={`modal-stock ${stockStatus}`}>{stockLabel}</div>
            <div className="modal-divider" />
            <div className="order-section">
              <h4>Place Your Order</h4>
              <input
                className="location-input"
                type="text"
                placeholder="Enter your full delivery address..."
                value={location}
                onChange={e => setLocation(e.target.value)}
              />
              <div className="qty-row">
                <span>Quantity:</span>
                <div className="qty-controls">
                  <button onClick={() => setQty(q => Math.max(1, q - 1))}>\\u2212</button>
                  <span>{qty}</span>
                  <button onClick={() => setQty(q => Math.min(product.stock || 99, q + 1))}>+</button>
                </div>
              </div>
              <div style={{ fontSize: 12, color: 'rgba(0,0,0,0.6)', marginBottom: 16 }}>
                Total: <strong style={{ color: '#000', fontSize: 15 }}>{"\\u20B9"}{(product.price * qty).toLocaleString('en-IN')}</strong>
              </div>
              <button className="buy-btn" onClick={handleBuyNow} disabled={product.stock === 0}>
                {product.stock === 0 ? 'Out of Stock' : 'Order via WhatsApp'}
              </button>
              <p style={{ fontSize: 10, color: 'rgba(0,0,0,0.5)', textAlign: 'center', marginTop: 10 }}>
                You will be redirected to WhatsApp to confirm your order
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
'''

import re
js = re.sub(
    r'(?=\nfunction ProductCard)',
    '\n' + modal_code + '\n',
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(js)

print("Product360Modal restored successfully!")
