"use client";

import { useState, useEffect, useRef, useCallback } from "react";



// ===== NAV LOGO SVG =====

function LogoMark() {
  return (
    <svg className="nav-logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="logo-grad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#1e293b"/>
          <stop offset="100%" stopColor="#0f172a"/>
        </linearGradient>
        <linearGradient id="logo-gold" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#f59e0b"/>
          <stop offset="100%" stopColor="#b45309"/>
        </linearGradient>
      </defs>
      <rect width="48" height="48" rx="14" fill="url(#logo-grad)" stroke="rgba(245, 158, 11, 0.2)" strokeWidth="1"/>
      <path d="M24 10L10 38H16.5L20 29H28L31.5 38H38L24 10ZM24 17.5L26.5 24H21.5L24 17.5Z" fill="url(#logo-gold)"/>
      <circle cx="24" cy="24" r="18" stroke="url(#logo-gold)" strokeWidth="1.5" strokeDasharray="3 4" opacity="0.4"/>
    </svg>
  );
}



// ===== MARQUEE CAROUSEL =====

function MarqueeCarousel({ products }) {

  const CARDS = products && products.length > 0 ? products : [];

  

  if (CARDS.length === 0) return null;



  // Duplicate cards to ensure smooth infinite scrolling

  const displayCards = [...CARDS, ...CARDS, ...CARDS, ...CARDS, ...CARDS, ...CARDS].slice(0, 20);



  return (

    <div className="hero-marquee-container" style={{ position: 'relative', padding: '40px 0', marginTop: '40px', width: '100vw', left: '50%', right: '50%', marginLeft: '-50vw', marginRight: '-50vw', overflow: 'hidden', maskImage: 'linear-gradient(to right, transparent, black 10%, black 90%, transparent)', WebkitMaskImage: 'linear-gradient(to right, transparent, black 10%, black 90%, transparent)' }}>

      <div className="hero-marquee" style={{ display: 'flex', gap: '24px', width: 'max-content', animation: 'scrollMarquee 40s linear infinite' }}>

        {displayCards.map((product, i) => (

          <div key={`${product.id}-${i}`} className="marquee-card" style={{ width: '240px', height: '320px', borderRadius: '16px', overflow: 'hidden', background: '#fff', boxShadow: '0 10px 30px rgba(0,0,0,0.08)', flexShrink: 0, border: '1px solid var(--border)', transition: 'transform 0.3s ease', cursor: 'pointer' }} onClick={() => {

            const el = document.getElementById(`product-${product.id}`);

            if (el) el.click();

          }}>

            <img src={product.enhanced_image_url || product.image_url} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />

            <div style={{ position: 'absolute', bottom: '0', left: '0', right: '0', padding: '24px 16px 16px', background: 'linear-gradient(to top, rgba(0,0,0,0.8), transparent)' }}>

              <div style={{ color: '#fff', fontWeight: '700', fontSize: '16px', marginBottom: '4px', textShadow: '0 2px 4px rgba(0,0,0,0.3)' }}>{product.name}</div>

              <div style={{ color: '#fff', fontWeight: '600', fontSize: '14px', textShadow: '0 2px 4px rgba(0,0,0,0.3)' }}>₹{product.price?.toLocaleString('en-IN')}</div>

            </div>

          </div>

        ))}

      </div>

    </div>

  );

}



// ===== PRODUCT CARD =====



// ===== PRODUCT 360 MODAL =====

function Product360Modal({ product, onClose }) {

  const [location, setLocation] = useState('');

  const [qty, setQty] = useState(1);
  const [isExpanded, setIsExpanded] = useState(false);

  const [view360Data, setView360Data] = useState(null);

  const [loadingGemini, setLoadingGemini] = useState(false);

  const WA = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '919082799791';



  useEffect(() => {

    document.body.style.overflow = 'hidden';

    

    return () => { document.body.style.overflow = ''; };

  }, []);



  



  function handleBuyNow() {

    if (!location.trim()) {

      alert('Please enter your delivery location');

      return;

    }

    const discount = product.original_price ? Math.round((1 - product.price / product.original_price) * 100) : 0;

    const msg = [

        ' *New Order - Arhat Creation*',

        '',

        ` *Product:* ${product.name}`,

        `️ *Category:* ${product.category || 'General'}`,

        ` *Price:* {"₹"}${product.price.toLocaleString('en-IN')}${discount ? ` (${discount}% OFF)` : ''}`,

        ` *Quantity:* ${qty}`,

        ` *Total:* {"₹"}${(product.price * qty).toLocaleString('en-IN')}`,

        '',

        ` *Delivery Location:* ${location}`,

        '',

        ` *Stock Available:* ${product.stock > 0 ? product.stock + ' units' : 'Check availability'}`,

        '',

        `⏲️ *Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,

        '',

        '--- Sent via Arhat Creation ---'

      ].join('\n');

    const url = `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;

    window.open(url, '_blank');

  }



  const stockStatus = product.stock > 10 ? 'good' : product.stock > 0 ? 'low' : 'none';

  const stockLabel = product.stock > 10 ? `✓ In Stock (${product.stock} units)` : product.stock > 0 ? `⚠ Only ${product.stock} left` : '✕ Out of Stock';



  return (

    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>

      <div className="modal-box" style={{ position: 'relative' }}>

        <button className="modal-close" onClick={onClose} aria-label="Close modal">✕</button>

        <div className="modal-inner">

          

          {/* Gallery Viewer */}

          <div className="modal-gallery" style={{ padding: '24px', background: 'var(--bg3)', borderRadius: '24px', marginBottom: '24px' }}>

            <div className="main-image-wrap" style={{ position: 'relative', width: '100%', aspectRatio: '1', borderRadius: '16px', overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,0.05)' }}>

              {(product.enhanced_image_url || product.image_url) ? (

                <img src={product.enhanced_image_url || product.image_url} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />

              ) : (

                <div style={{ width: '100%', height: '100%', background: 'linear-gradient(155deg,#1a2535,#0d1520)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 60 }}>✨</div>

              )}

            </div>



          </div>

{/* Details Panel */}

          <div className="modal-details">

            {product.category && <div className="modal-category">{product.category}</div>}

            <h2 className="modal-title">{product.name}</h2>

                        {product.description && (
              <div style={{ marginBottom: '8px' }}>
                <p className="modal-desc" style={{ display: isExpanded ? 'block' : '-webkit-box', WebkitLineClamp: isExpanded ? 'unset' : 3, WebkitBoxOrient: 'vertical', overflow: 'hidden', textOverflow: 'ellipsis', margin: 0, transition: 'all 0.3s ease' }}>{product.description}</p>
                {product.description.length > 100 && (
                  <button onClick={() => setIsExpanded(!isExpanded)} style={{ background: 'transparent', border: 'none', color: 'var(--primary)', fontSize: '13px', fontWeight: '700', cursor: 'pointer', padding: 0, marginTop: '8px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    {isExpanded ? 'Read Less' : 'Read More'}
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ transform: isExpanded ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}><path d="m6 9 6 6 6-6"></path></svg>
                  </button>
                )}
              </div>
            )}

            <div className="modal-price-row" style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>

              <span className="modal-price" style={{ fontSize: '28px', fontWeight: '800', color: 'var(--primary)' }}>{"₹"}{product.price?.toLocaleString('en-IN')}</span>

              {product.original_price && (

                <>

                  <span className="modal-orig-price" style={{ textDecoration: 'line-through', color: 'var(--text-dim)', fontSize: '18px', fontWeight: '600' }}>{"₹"}{product.original_price.toLocaleString('en-IN')}</span>

                  <span className="modal-discount" style={{ background: '#10b981', color: '#fff', padding: '4px 10px', borderRadius: '8px', fontSize: '13px', fontWeight: '700' }}>

                    {Math.round((1 - product.price / product.original_price) * 100)}% OFF

                  </span>

                </>

              )}

            </div>

            

            <div className="modal-divider" />

                        <div className="order-section" style={{ background: '#fff', borderRadius: '20px', padding: '20px', boxShadow: '0 4px 20px rgba(0,0,0,0.04)', border: '1px solid #f1f5f9', marginTop: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'var(--primary)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path><path d="M3 6h18"></path><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
                </div>
                <h4 style={{ margin: 0, fontSize: '18px', fontWeight: '800', color: '#0f172a' }}>Place Your Order</h4>
              </div>
              
              <div style={{ position: 'relative', marginBottom: '16px' }}>
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
              </div>

                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px', background: '#f8fafc', padding: '16px', borderRadius: '16px', border: '1px solid #e2e8f0' }}>
                <span style={{ fontSize: '15px', fontWeight: '700', color: '#334155' }}>Quantity</span>
                <div style={{ display: 'flex', alignItems: 'center', background: '#ffffff', borderRadius: '999px', border: '1px solid #cbd5e1', overflow: 'hidden', boxShadow: '0 2px 8px rgba(0,0,0,0.03)' }}>
                  <button onClick={() => setQty(q => Math.max(1, q - 1))} style={{ width: '40px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px', fontWeight: '500', color: '#475569', cursor: 'pointer', background: 'transparent', border: 'none', transition: 'background 0.2s' }} onMouseOver={e => e.currentTarget.style.background = '#f1f5f9'} onMouseOut={e => e.currentTarget.style.background = 'transparent'}>−</button>
                  <span style={{ width: '40px', textAlign: 'center', fontSize: '16px', fontWeight: '800', color: '#0f172a' }}>{qty}</span>
                  <button onClick={() => setQty(q => q + 1)} style={{ width: '40px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px', fontWeight: '500', color: '#475569', cursor: 'pointer', background: 'transparent', border: 'none', transition: 'background 0.2s' }} onMouseOver={e => e.currentTarget.style.background = '#f1f5f9'} onMouseOut={e => e.currentTarget.style.background = 'transparent'}>+</button>
                </div>
              </div>
              
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', padding: '0 4px' }}>
                <span style={{ fontSize: '15px', color: '#64748b', fontWeight: '500' }}>Total Amount</span>
                <span style={{ color: '#0f172a', fontSize: '24px', fontWeight: '800' }}>{"₹"}{(product.price * qty).toLocaleString('en-IN')}</span>
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
  );
}

function ProductCard({ product, onClick }) {

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

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>

            <span style={{ fontSize: '24px', fontWeight: '800', color: 'var(--primary)' }}>{"\u20B9"}{product.price?.toLocaleString('en-IN')}</span>

            {product.original_price && (

              <span style={{ fontSize: '15px', fontWeight: '600', color: '#94a3b8', textDecoration: 'line-through' }}>{"\u20B9"}{product.original_price.toLocaleString('en-IN')}</span>

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

}



// ===== TOAST =====

function Toast({ message, type, show }) {

  return (

    <div className={`toast ${type} ${show ? 'show' : ''}`} role="alert">

      {message}

    </div>

  );

}



// ===== MAIN PAGE =====

export default function StorePage() {

  const [products, setProducts] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);

  const [loading, setLoading] = useState(true);

  const [selectedProduct, setSelectedProduct] = useState(null);

  const [toast, setToast] = useState({ show: false, message: '', type: 'info' });

  const [searchQuery, setSearchQuery] = useState('');

  const [selectedCategory, setSelectedCategory] = useState('All');

  const WA = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '919082799791';



  useEffect(() => {

    loadProducts();

  }, []);



  useEffect(() => {

    const canvas = document.getElementById('starfield');

    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; draw(); }

    function draw() {

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < 150; i++) {

        const x = Math.random() * canvas.width;

        const y = Math.random() * canvas.height;

        const a = 0.05 + Math.random() * 0.25;

        ctx.beginPath();

        ctx.arc(x, y, 0.6, 0, Math.PI*2);

        ctx.fillStyle = 'rgba(255,255,255,' + a + ')';

        ctx.fill();

      }

    }

    window.addEventListener('resize', resize);

    resize();

    return () => window.removeEventListener('resize', resize);

  }, []);







  async function loadProducts() {

    setLoading(true);

    try {

      const res = await fetch('/api/products');

      const data = await res.json();

      setProducts(data.products || []);

      if (data.isMock) {

        showToast('Demo mode — Configure Supabase to manage real products', 'info');

      }

    } catch (err) {

      console.error(err);

      showToast('Failed to load products', 'error');

    } finally {

      setLoading(false);

    }

  }



  function showToast(message, type = 'info', duration = 4000) {

    setToast({ show: true, message, type });

    setTimeout(() => setToast(t => ({ ...t, show: false })), duration);

  }



  const categories = ['All', ...new Set(products.map(p => p.category).filter(Boolean))];

  const filteredProducts = products.filter(p => {

    const matchesSearch = !searchQuery || p.name?.toLowerCase().includes(searchQuery.toLowerCase()) || p.description?.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesCategory = selectedCategory === 'All' || p.category === selectedCategory;

    return matchesSearch && matchesCategory;

  });



  return (

    <>

      {/* NAV */}

            <nav className="main-nav" role="navigation">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
          <a href="/" className="nav-logo" aria-label="Arhat Creation Home">
            <LogoMark />
            <div className="nav-wordmark">
              <span className="kick">ARHAT</span>
              <span className="name">CREATION</span>
            </div>
          </a>

          <ul className="nav-links" role="list">
            <li><a href="#products">Products</a></li>
            <li><a href="#categories">Categories</a></li>
            <li><a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer">Contact</a></li>
          </ul>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer" className="glow-btn nav-cta" id="nav-whatsapp-btn" style={{ display: 'flex', alignItems: 'center', gap: '6px', height: '38px', padding: '0 16px' }}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" /></svg>
              <span>Chat</span>
            </a>
            
            <button className="mobile-menu-btn" onClick={() => setMenuOpen(!menuOpen)} style={{ background: 'none', border: 'none', padding: '8px', cursor: 'pointer', display: 'none' }}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                {menuOpen ? (
                  <>
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </>
                ) : (
                  <>
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                  </>
                )}
              </svg>
            </button>
          </div>
        </div>
        
        {menuOpen && (
          <div className="mobile-menu-dropdown" style={{ width: '100%', padding: '16px 0', display: 'flex', flexDirection: 'column', gap: '16px', borderTop: '1px solid var(--border)' }}>
            <a href="#products" onClick={() => setMenuOpen(false)} style={{ padding: '12px', fontWeight: '600', color: 'var(--text)' }}>Products</a>
            <a href="#categories" onClick={() => setMenuOpen(false)} style={{ padding: '12px', fontWeight: '600', color: 'var(--text)' }}>Categories</a>
            <a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer" style={{ padding: '12px', fontWeight: '600', color: 'var(--primary)' }}>Contact Support</a>
            <a href="/admin" style={{ padding: '12px', fontWeight: '600', color: 'var(--text-muted)' }}>Admin Panel</a>
          </div>
        )}
      </nav>



      {/* HERO */}

      <section className="hero">

        <div className="hero-bg" />



        {/* Starfield */}

        <canvas id="starfield" style={{ position: "absolute", inset: 0, pointerEvents: "none" }} />



        <div className="hero-content">

          <div className="hero-badge">

            <div className="hero-badge-icon">

              <svg viewBox="5 1 14 22" width="14" height="16" preserveAspectRatio="none"

                fill="rgba(16,112,152,.72)" stroke="rgba(190,236,255,.6)" strokeWidth="1.6" strokeLinejoin="round">

                <path d="M13.9 1.6 5.5 13.6a.7.7 0 0 0 .6 1.1h4.2l-1 7.7a.7.7 0 0 0 1.25.55l8.3-12.1a.7.7 0 0 0-.6-1.1h-4.2l1-7.7a.7.7 0 0 0-1.25-.55Z"/>

              </svg>

            </div>

            <span className="hero-badge-text">Premium quality at your doorstep</span>

          </div>



          <h1 className="hero-h1">

            <span>Discover Premium</span>

            <span style={{ background: 'linear-gradient(135deg,#00d4ff,#0080ff)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>

              Products

            </span>

          </h1>

          <p className="hero-sub">

            <b>Curated collections · <span>Exceptional quality</span></b>{' '}

            delivered fast with care

          </p>



                      <a href="#products" className="hero-cta-primary" id="hero-shop-now-btn">

              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>

                Shop Now

                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ transition: 'transform 0.3s ease' }}>

                  <line x1="5" y1="12" x2="19" y2="12"></line>

                  <polyline points="12 5 19 12 12 19"></polyline>

                </svg>

              </span>

            </a>

        </div>



        {/* 3D Ring Carousel */}

        <MarqueeCarousel products={products} />

      </section>



      {/* PRODUCTS SECTION */}

      <section className="products-section" id="products">

        <div className="section-header">

          <div>

            <h2 className="section-title">Our Collection</h2>

            <p style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 4 }}>

              {filteredProducts.length} product{filteredProducts.length !== 1 ? 's' : ''} found

            </p>

          </div>

        </div>



        {/* Search + Filter */}

        <div className="filter-row" style={{ display: 'flex', gap: 12, marginBottom: 32, flexWrap: 'wrap', alignItems: 'center' }}>

          <input

            type="search"

            placeholder="Search products..."

            value={searchQuery}

            onChange={e => setSearchQuery(e.target.value)}

            style={{ flex: '1 1 200px' }} className="form-input search-input"

            id="product-search"

          />

          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }} id="categories" role="group" aria-label="Categories">

            {categories.map(cat => (

              <button

                key={cat}

                onClick={() => setSelectedCategory(cat)}

                id={`cat-${cat.toLowerCase()}`}

                style={{

                  padding: '10px 18px', borderRadius: 10, fontSize: 13, fontWeight: 500,

                  background: selectedCategory === cat ? 'rgba(0,212,255,.15)' : 'rgba(255,255,255,.04)',

                  border: `1px solid ${selectedCategory === cat ? 'rgba(0,212,255,.4)' : 'rgba(255,255,255,.08)'}`,

                  color: selectedCategory === cat ? 'var(--accent2)' : 'rgba(255,255,255,.7)',

                  cursor: 'pointer', transition: 'all .2s', whiteSpace: 'nowrap'

                }}

              >

                {cat}

              </button>

            ))}

          </div>

        </div>



        {loading ? (

          <div className="page-loader">

            <div className="loader-ring" />

            <p className="loader-text">Loading products...</p>

          </div>

        ) : (

          <div className="products-grid">

            {filteredProducts.length === 0 ? (

              <div className="empty-state">

                <h3>No products found</h3>

                <p>{searchQuery ? 'Try a different search term' : 'Products will appear here once added by admin'}</p>

              </div>

            ) : (

              filteredProducts.map(product => (

                <ProductCard

                  key={product.id}

                  product={product}

                  onClick={() => setSelectedProduct(product)}

                />

              ))

            )}

          </div>

        )}

      </section>



      {/* FOOTER */}

      <footer className="site-footer">
        <div className="footer-inner">
          <div className="footer-col-brand" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div className="nav-logo" style={{ marginBottom: '8px' }}>
              <LogoMark />
              <span className="name" style={{ fontSize: '20px' }}>ARHAT<span className="kick">CREATION</span></span>
            </div>
            <p className="footer-brand-tag" style={{ color: 'var(--text-muted)', lineHeight: '1.6', fontSize: '14px', maxWidth: '300px' }}>
              Curating premium products and delivering unparalleled luxury directly to you. Experience the extraordinary.
            </p>
          </div>

          <div className="footer-col">
            <h4 className="footer-heading">Shop</h4>
            <ul className="footer-links">
              <li><a href="#products">All Products</a></li>
              <li><a href="#products">New Arrivals</a></li>
              <li><a href="#products">Best Sellers</a></li>
            </ul>
          </div>

          <div className="footer-col">
            <h4 className="footer-heading">Support</h4>
            <ul className="footer-links">
              <li><a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer">Contact via WhatsApp</a></li>
              <li><a href="#">Shipping & Returns</a></li>
              <li><a href="#">Privacy Policy</a></li>
            </ul>
          </div>

          <div className="footer-col">
            <h4 className="footer-heading">Admin</h4>
            <ul className="footer-links">
              <li><a href="/admin">Dashboard Access</a></li>
            </ul>
          </div>
        </div>
        
        <div className="footer-bottom" style={{ marginTop: '48px', paddingTop: '24px', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', alignItems: 'center' }}>
          <p className="footer-copy">© {new Date().getFullYear()} Arhat Creation. All rights reserved.</p>
          <div className="footer-socials" style={{ display: 'flex', gap: '16px' }}>
            <a href="#" aria-label="Instagram" style={{ color: 'var(--text-dim)', fontSize: '13px', fontWeight: '700', letterSpacing: '.1em' }}>IG</a>
            <a href="#" aria-label="Facebook" style={{ color: 'var(--text-dim)', fontSize: '13px', fontWeight: '700', letterSpacing: '.1em' }}>FB</a>
            <a href="#" aria-label="Twitter" style={{ color: 'var(--text-dim)', fontSize: '13px', fontWeight: '700', letterSpacing: '.1em' }}>X</a>
          </div>
        </div>
      </footer>



      {/* WHATSAPP FLOAT */}

      <a

        href={`https://wa.me/${WA}`}

        target="_blank"

        rel="noopener noreferrer"

        className="wa-float"

        aria-label="Chat on WhatsApp"

        id="whatsapp-float-btn"

      >

        <svg width="31" height="31" viewBox="0 0 32 32" fill="white">

          <path d="M16 2C8.28 2 2 8.28 2 16c0 2.48.68 4.8 1.86 6.8L2.07 30l7.4-1.77C11.32 29.38 13.62 30 16 30c7.72 0 14-6.28 14-14S23.72 2 16 2zm6.93 19.36c-.3.83-1.74 1.63-2.4 1.7-.62.07-1.2.3-4.07-.86-3.43-1.38-5.6-4.9-5.77-5.13-.16-.23-1.37-1.82-1.37-3.47 0-1.65.86-2.46 1.17-2.8.3-.33.65-.42.87-.42.22 0 .43 0 .62.01.2.01.47-.08.73.56.27.65.9 2.2.98 2.36.08.16.14.35.03.56-.1.2-.16.33-.32.51-.16.18-.34.4-.48.54-.16.16-.33.33-.14.65.19.32.84 1.38 1.8 2.24 1.24 1.1 2.28 1.45 2.6 1.61.32.16.5.14.69-.08.19-.22.8-.93 1.01-1.25.21-.32.43-.27.72-.16.29.1 1.84.87 2.16 1.03.32.16.53.24.61.37.08.13.08.77-.22 1.6z"/>

        </svg>

      </a>



      {/* 360 MODAL */}

      {selectedProduct && (

        <Product360Modal

          product={selectedProduct}

          onClose={() => setSelectedProduct(null)}

        />

      )}



      {/* TOAST */}

      <Toast {...toast} />



      

    </>

  );

}

