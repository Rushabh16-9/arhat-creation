import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_modal = '''function Product360Modal({ product, onClose }) {
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
      console.log('Insights failed:', err);
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
        `\\uD83D\\uDCB0 *Price:* \\u20B9${product.price.toLocaleString('en-IN')}${discount ? ` (${discount}% OFF)` : ''}`,
        `\\uD83D\\uDD22 *Quantity:* ${qty}`,
        `\\uD83D\\uDCB8 *Total:* \\u20B9${(product.price * qty).toLocaleString('en-IN')}`,
        '',
        `\\uD83D\\uDCCD *Delivery Location:* ${location}`,
        '',
        `\\u23F2\\uFE0F *Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,
        '',
        '--- Sent via Arhat Shop ---'
      ].join('\\n');
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(msg)}`, '_blank');
  }

  const stockStatus = product.stock > 10 ? 'good' : product.stock > 0 ? 'low' : 'none';
  const stockLabel = product.stock > 10 ? `\\u2713 In Stock (${product.stock} units)` : product.stock > 0 ? `\\u26A0 Only ${product.stock} left` : '\\u2715 Out of Stock';

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal-box" style={{ position: 'relative' }}>
        <button className="modal-close" onClick={onClose} aria-label="Close modal">\\u2715</button>
        <div className="modal-inner">
          
          {/* LEFT COLUMN: Gallery & AI Insights */}
          <div className="modal-left-col" style={{ padding: '32px', background: 'var(--bg2)', borderRight: '1px solid var(--border)', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {/* Gallery Viewer */}
            <div className="modal-gallery">
              <div className="main-image-wrap" style={{ position: 'relative', width: '100%', aspectRatio: '1', borderRadius: '16px', overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,0.05)', background: '#fff' }}>
                {(product.enhanced_image_url || product.image_url) ? (
                  <img src={product.enhanced_image_url || product.image_url} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                ) : (
                  <div style={{ width: '100%', height: '100%', background: 'linear-gradient(155deg,#f1f5f9,#e2e8f0)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 40 }}>\\uD83D\\uDCE6</div>
                )}
              </div>
              
              {/* Thumbnail Strip */}
              {(product.enhanced_image_url || product.image_url) && (
                <div style={{ display: 'flex', gap: '12px', marginTop: '16px', justifyContent: 'center' }}>
                  {[1, 2, 3].map(i => (
                    <div key={i} style={{ width: '64px', height: '64px', borderRadius: '10px', overflow: 'hidden', border: i === 1 ? '2px solid var(--primary)' : '1px solid var(--border)', cursor: 'pointer', opacity: i === 1 ? 1 : 0.6, transition: 'all 0.2s', background: '#fff' }}>
                      <img src={product.enhanced_image_url || product.image_url} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* AI Insights Card */}
            {view360Data && (
              <div style={{ padding: '20px', background: 'linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%)', borderRadius: '16px', border: '1px solid rgba(14, 165, 233, 0.15)', boxShadow: '0 4px 12px rgba(0,0,0,0.03)' }}>
                <div style={{ fontSize: '11px', letterSpacing: '0.15em', color: '#0369a1', textTransform: 'uppercase', marginBottom: '12px', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  \\u2728 Gemini AI Insights
                </div>
                {view360Data.overallImpression && (
                  <p style={{ fontSize: '14px', color: '#334155', lineHeight: '1.6', fontWeight: '500', marginBottom: '12px' }}>
                    {view360Data.overallImpression}
                  </p>
                )}
                {view360Data.uniqueFeature && (
                  <p style={{ fontSize: '13px', color: '#0ea5e9', fontStyle: 'italic', fontWeight: '600', paddingLeft: '10px', borderLeft: '3px solid #38bdf8' }}>
                    {view360Data.uniqueFeature}
                  </p>
                )}
              </div>
            )}
            
            {loadingGemini && (
              <div style={{ fontSize: 13, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center', padding: '20px' }}>
                <span className="gemini-spinner" style={{ width: 14, height: 14 }} />
                AI is analyzing product details...
              </div>
            )}
          </div>
          
          {/* RIGHT COLUMN: Details Panel */}
          <div className="modal-details" style={{ padding: '40px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              {product.category && <div className="modal-category" style={{ fontSize: '12px', fontWeight: '700', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '8px' }}>{product.category}</div>}
              <h2 className="modal-title" style={{ fontSize: '32px', fontWeight: '800', color: 'var(--primary)', marginBottom: '12px', lineHeight: '1.1' }}>{product.name}</h2>
              {product.description && (
                <p className="modal-desc" style={{ fontSize: '15px', color: 'var(--text-muted)', lineHeight: '1.6' }}>{product.description}</p>
              )}
            </div>
            
            <div className="modal-price-row" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span className="modal-price" style={{ fontSize: '32px', fontWeight: '800', color: 'var(--primary)' }}>\\u20B9{product.price?.toLocaleString('en-IN')}</span>
              {product.original_price && (
                <>
                  <span className="modal-orig-price" style={{ textDecoration: 'line-through', color: 'var(--text-dim)', fontSize: '20px', fontWeight: '600' }}>\\u20B9{product.original_price.toLocaleString('en-IN')}</span>
                  <span className="modal-discount" style={{ background: '#10b981', color: '#fff', padding: '4px 10px', borderRadius: '8px', fontSize: '13px', fontWeight: '700' }}>
                    {Math.round((1 - product.price / product.original_price) * 100)}% OFF
                  </span>
                </>
              )}
            </div>
            
            <div className={`modal-stock \${stockStatus}`} style={{ display: 'inline-block', padding: '6px 12px', borderRadius: '6px', fontSize: '12px', fontWeight: '600', width: 'fit-content', background: product.stock > 10 ? '#f0fdf4' : product.stock > 0 ? '#fffbeb' : '#fef2f2', color: product.stock > 10 ? '#166534' : product.stock > 0 ? '#b45309' : '#991b1b' }}>{stockLabel}</div>
            
            <div className="modal-divider" style={{ height: '1px', background: 'var(--border)', margin: '8px 0' }} />
            
            <div className="order-section" style={{ background: 'var(--bg2)', padding: '24px', borderRadius: '16px', border: '1px solid var(--border)' }}>
              <h4 style={{ margin: '0 0 16px 0', fontSize: '16px', color: 'var(--primary)', fontWeight: '700' }}>Place Your Order</h4>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <input
                  className="location-input"
                  type="text"
                  placeholder="Enter your full delivery address..."
                  value={location}
                  onChange={e => setLocation(e.target.value)}
                  style={{ width: '100%', padding: '14px 16px', borderRadius: '10px', border: '1px solid var(--border)', background: 'var(--surface)', color: 'var(--primary)', fontSize: '15px' }}
                />
                
                <div className="qty-row" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <span style={{ fontSize: '14px', fontWeight: '600', color: 'var(--text-muted)' }}>Quantity:</span>
                    <div className="qty-controls" style={{ display: 'flex', alignItems: 'center', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '8px', overflow: 'hidden' }}>
                      <button onClick={() => setQty(q => Math.max(1, q - 1))} style={{ padding: '8px 14px', border: 'none', background: 'transparent', cursor: 'pointer', fontSize: '16px', color: 'var(--primary)' }}>\\u2212</button>
                      <span style={{ padding: '0 12px', fontSize: '15px', fontWeight: '600', color: 'var(--primary)', borderLeft: '1px solid var(--border)', borderRight: '1px solid var(--border)' }}>{qty}</span>
                      <button onClick={() => setQty(q => Math.min(product.stock || 99, q + 1))} style={{ padding: '8px 14px', border: 'none', background: 'transparent', cursor: 'pointer', fontSize: '16px', color: 'var(--primary)' }}>+</button>
                    </div>
                  </div>
                </div>
                
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px', background: 'var(--surface)', borderRadius: '10px', border: '1px dashed var(--border)' }}>
                  <span style={{ fontSize: '14px', color: 'var(--text-muted)', fontWeight: '500' }}>Total Amount</span>
                  <strong style={{ color: 'var(--primary)', fontSize: '20px', fontWeight: '800' }}>\\u20B9{(product.price * qty).toLocaleString('en-IN')}</strong>
                </div>
                
                <button
                  onClick={handleBuyNow}
                  disabled={product.stock === 0}
                  style={{ width: '100%', padding: '16px', borderRadius: '12px', background: '#25D366', color: '#fff', border: 'none', fontSize: '16px', fontWeight: '700', cursor: product.stock === 0 ? 'not-allowed' : 'pointer', opacity: product.stock === 0 ? 0.5 : 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', boxShadow: '0 8px 24px rgba(37, 211, 102, 0.25)', transition: 'transform 0.2s' }}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91C2.13 13.66 2.59 15.36 3.45 16.86L2.05 22L7.3 20.62C8.75 21.41 10.38 21.83 12.04 21.83C17.5 21.83 21.95 17.38 21.95 11.92C21.95 9.27 20.92 6.78 19.05 4.91C17.18 3.03 14.69 2 12.04 2Z"/>
                  </svg>
                  {product.stock === 0 ? 'Out of Stock' : 'Order via WhatsApp'}
                </button>
                <p style={{ fontSize: '12px', color: 'var(--text-dim)', textAlign: 'center', margin: 0, fontWeight: '500' }}>
                  You will be redirected to WhatsApp to confirm your order
                </p>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}'''

start_idx = js.find('function Product360Modal({ product, onClose }) {')
end_idx = js.find('// ===== PRODUCT CARD =====', start_idx)

if start_idx != -1 and end_idx != -1:
    js = js[:start_idx] + new_modal + '\n\n' + js[end_idx:]
    with open('app/page.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("UI completely overhauled!")
else:
    print("Could not find boundaries")
