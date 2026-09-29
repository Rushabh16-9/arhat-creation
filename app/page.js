"use client";
import { useState, useEffect, useRef, useCallback } from "react";

// ===== NAV LOGO SVG =====
function LogoMark() {
  return (
    <svg className="nav-logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="sw" x1="8" y1="8" x2="40" y2="40" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#8ef4ff"/>
          <stop offset="0.5" stopColor="#35d8ff"/>
          <stop offset="1" stopColor="#0a86d8"/>
        </linearGradient>
        <linearGradient id="sw2" x1="40" y1="10" x2="10" y2="40" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#a6f7ff"/>
          <stop offset="1" stopColor="#0f9ae0" stopOpacity="0.25"/>
        </linearGradient>
      </defs>
      <g transform="rotate(-32 24 24)">
        <ellipse cx="24" cy="24" rx="18.5" ry="9.6" stroke="url(#sw2)" strokeWidth="3.1" strokeLinecap="round" strokeDasharray="58 30" strokeDashoffset="14" fill="none"/>
        <circle cx="41.4" cy="20.6" r="3.1" fill="#bff6ff"/>
      </g>
      <circle cx="24" cy="24" r="6.6" fill="url(#sw)"/>
      <circle cx="24" cy="24" r="2.6" fill="#fff"/>
    </svg>
  );
}

// ===== 3D RING CAROUSEL =====
function RingCarousel({ products }) {
  const ringRef = useRef(null);
  const phaseRef = useRef(-2);
  const lastRef = useRef(null);
  const rafRef = useRef(null);
  const reduced = useRef(false);

  const CARDS = products && products.length > 0 ? products : Array(10).fill(null).map((_,i) => ({
    id: i, name: `Product ${i+1}`,
    image_url: null,
    color: ['#1a2535','#2b1535','#1a3520','#352515','#153035','#301530','#153525','#302515','#152535','#251535'][i]
  }));

  const n = Math.max(CARDS.length, 10);
  const R = 891;
  const step = 360 / n;
  const CULL = 42;

  useEffect(() => {
    reduced.current = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function tick(t) {
      if (!lastRef.current) lastRef.current = t;
      const dt = Math.min((t - lastRef.current) / 1000, 0.1);
      lastRef.current = t;
      if (!reduced.current) phaseRef.current -= 1.9 * dt;
      placeCards();
      rafRef.current = requestAnimationFrame(tick);
    }

    function placeCards() {
      if (!ringRef.current) return;
      const cards = ringRef.current.querySelectorAll('.ring-card');
      cards.forEach((card, i) => {
        let a = ((i * step + phaseRef.current) % 360 + 540) % 360 - 180;
        if (Math.abs(a) > CULL) {
          card.style.visibility = 'hidden';
          return;
        }
        card.style.visibility = 'visible';
        const r = a * Math.PI / 180;
        const c = Math.cos(r);
        card.style.transform = `translate3d(${R * Math.sin(r)}px, 0, ${R * (1 - c)}px) rotateY(${-a}deg)`;
        card.style.filter = `brightness(${0.84 + 0.5 * (1 / c - 1)})`;
      });
    }

    document.addEventListener('visibilitychange', () => { lastRef.current = null; });
    rafRef.current = requestAnimationFrame(tick);
    return () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); };
  }, [products]);

  return (
    <div className="ring-section" aria-hidden="true">
      <div className="ring-container" ref={ringRef} style={{ transformStyle: 'preserve-3d' }}>
        {CARDS.map((product, i) => (
          <div key={product?.id ?? i} className="ring-card">
            {product?.image_url || product?.enhanced_image_url ? (
              <img
                src={product.enhanced_image_url || product.image_url}
                alt=""
                onError={e => e.currentTarget.parentElement.classList.add('broken')}
              />
            ) : (
              <div style={{
                width: '100%', height: '100%',
                background: `linear-gradient(155deg, ${product?.color || '#1a2535'}, #0a0f18)`,
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                <div style={{ textAlign: 'center', padding: '0 12px' }}>
                  <div style={{ fontSize: '28px', marginBottom: '8px', opacity: .4 }}>🛍</div>
                  <div style={{ fontSize: '9px', color: 'rgba(255,255,255,.4)', fontWeight: 600, letterSpacing: '.08em' }}>
                    {product?.name || 'PRODUCT'}
                  </div>
                </div>
              </div>
            )}
            <div className="card-edge" />
          </div>
        ))}
      </div>
    </div>
  );
}

// ===== PRODUCT 360 MODAL =====
function Product360Modal({ product, onClose }) {
  const [location, setLocation] = useState('');
  const [qty, setQty] = useState(1);
  const [view360Data, setView360Data] = useState(null);
  const [loadingGemini, setLoadingGemini] = useState(false);
  const WA = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '919082799791';

  useEffect(() => {
    document.body.style.overflow = 'hidden';
    // Load 360 description from Gemini if image is available
    if ((product.image_url || product.enhanced_image_url) && !view360Data) {
      load360Description();
    }
    return () => { document.body.style.overflow = ''; };
  }, []);

  async function load360Description() {
    try {
      setLoadingGemini(true);
      const imgUrl = product.enhanced_image_url || product.image_url;
      // Fetch image and convert to base64
      const imgResp = await fetch(imgUrl);
      const blob = await imgResp.blob();
      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64 = e.target.result.split(',')[1];
        const mimeType = blob.type;
        const res = await fetch('/api/gemini', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'generate360Description', imageBase64: base64, mimeType })
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
      '🛍️ *New Order — Arhat Shop*',
      '',
      `📦 *Product:* ${product.name}`,
      `📁 *Category:* ${product.category || 'General'}`,
      `💰 *Price:* ₹${product.price.toLocaleString('en-IN')}${discount ? ` (${discount}% OFF)` : ''}`,
      `🔢 *Quantity:* ${qty}`,
      `💳 *Total:* ₹${(product.price * qty).toLocaleString('en-IN')}`,
      '',
      `📍 *Delivery Location:* ${location}`,
      '',
      `📊 *Stock Available:* ${product.stock > 0 ? product.stock + ' units' : 'Check availability'}`,
      '',
      `🕐 *Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,
      '',
      '—— Sent via Arhat Shop ——'
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
          {/* 360 Viewer */}
          <div className="modal-viewer">
            <div className="spin-container">
              {(product.enhanced_image_url || product.image_url) ? (
                <img
                  className="spin-image"
                  src={product.enhanced_image_url || product.image_url}
                  alt={product.name}
                />
              ) : (
                <div style={{
                  width: 200, height: 260, borderRadius: 16,
                  background: 'linear-gradient(155deg,#1a2535,#0d1520)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 60, animation: 'spin360 8s linear infinite'
                }}>🛍</div>
              )}
              <div className="spin-reflection" />
            </div>
            <div className="viewer-label">
              <span>360°</span> Interactive View
            </div>
            {loadingGemini && (
              <div style={{ marginTop: 12, fontSize: 11, color: 'rgba(255,255,255,.4)', display: 'flex', alignItems: 'center', gap: 6 }}>
                <span className="gemini-spinner" style={{ width: 10, height: 10 }} />
                AI analyzing...
              </div>
            )}
            {view360Data && (
              <div style={{ marginTop: 16, padding: '12px 16px', background: 'rgba(0,212,255,.05)', borderRadius: 10, border: '1px solid rgba(0,212,255,.1)', maxWidth: 220, width: '100%' }}>
                <div style={{ fontSize: 9, letterSpacing: '.1em', color: 'var(--accent2)', textTransform: 'uppercase', marginBottom: 8, fontWeight: 600 }}>✨ Gemini AI Insights</div>
                {view360Data.overallImpression && (
                  <p style={{ fontSize: 11, color: 'rgba(255,255,255,.7)', lineHeight: 1.5 }}>{view360Data.overallImpression}</p>
                )}
                {view360Data.uniqueFeature && (
                  <p style={{ fontSize: 10, color: 'rgba(0,212,255,.8)', marginTop: 6, fontStyle: 'italic' }}>✦ {view360Data.uniqueFeature}</p>
                )}
              </div>
            )}
          </div>

          {/* Details Panel */}
          <div className="modal-details">
            {product.category && <div className="modal-category">{product.category}</div>}
            <h2 className="modal-title">{product.name}</h2>
            {product.description && (
              <p className="modal-desc">{product.description}</p>
            )}
            <div className="modal-price-row">
              <span className="modal-price">₹{product.price?.toLocaleString('en-IN')}</span>
              {product.original_price && (
                <span className="modal-orig-price">₹{product.original_price.toLocaleString('en-IN')}</span>
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
                id="delivery-location"
              />
              <div className="qty-row">
                <span className="qty-label">Quantity:</span>
                <div className="qty-controls">
                  <button className="qty-btn" onClick={() => setQty(q => Math.max(1, q - 1))} id="qty-minus">−</button>
                  <span className="qty-num">{qty}</span>
                  <button className="qty-btn" onClick={() => setQty(q => Math.min(product.stock || 99, q + 1))} id="qty-plus">+</button>
                </div>
                <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>× ₹{product.price?.toLocaleString('en-IN')}</span>
              </div>
              <div style={{ fontSize: 12, color: 'rgba(255,255,255,.4)', marginBottom: 16 }}>
                Total: <strong style={{ color: '#fff', fontSize: 15 }}>₹{(product.price * qty).toLocaleString('en-IN')}</strong>
              </div>
              <button
                className="glow-btn buy-btn"
                onClick={handleBuyNow}
                disabled={product.stock === 0}
                id="buy-now-btn"
                style={{ opacity: product.stock === 0 ? 0.5 : 1, cursor: product.stock === 0 ? 'not-allowed' : 'pointer' }}
              >
                <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91C2.13 13.66 2.59 15.36 3.45 16.86L2.05 22L7.3 20.62C8.75 21.41 10.38 21.83 12.04 21.83C17.5 21.83 21.95 17.38 21.95 11.92C21.95 9.27 20.92 6.78 19.05 4.91C17.18 3.03 14.69 2 12.04 2Z"/>
                  </svg>
                  {product.stock === 0 ? 'Out of Stock' : 'Buy via WhatsApp'}
                </span>
              </button>
              <p style={{ fontSize: 10, color: 'rgba(255,255,255,.3)', textAlign: 'center', marginTop: 10 }}>
                You'll be redirected to WhatsApp to complete your order
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ===== PRODUCT CARD =====
function ProductCard({ product, onClick }) {
  const discount = product.original_price ? Math.round((1 - product.price / product.original_price) * 100) : 0;
  const stockStatus = product.stock > 10 ? 'in-stock' : product.stock > 0 ? 'low-stock' : 'out-stock';
  const stockLabel = product.stock > 10 ? 'In Stock' : product.stock > 0 ? `Only ${product.stock} left` : 'Out of Stock';

  return (
    <div className="product-card" onClick={onClick} role="button" tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && onClick()} id={`product-${product.id}`}>
      <div className="product-img-wrap">
        {(product.enhanced_image_url || product.image_url) ? (
          <img src={product.enhanced_image_url || product.image_url} alt={product.name} />
        ) : (
          <div style={{
            width: '100%', height: '100%', minHeight: 220,
            background: 'linear-gradient(155deg,#1a2535,#0d1520)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 48, opacity: .4
          }}>🛍</div>
        )}
        {discount > 0 && <div className="product-badge sale">-{discount}%</div>}
        <div className={`product-stock-badge ${stockStatus}`}>{stockLabel}</div>
      </div>
      <div className="product-info">
        {product.category && (
          <div style={{ fontSize: 10, letterSpacing: '.1em', textTransform: 'uppercase', color: 'var(--accent2)', marginBottom: 4, fontWeight: 600 }}>
            {product.category}
          </div>
        )}
        <h3 className="product-name">{product.name}</h3>
        {product.description && <p className="product-desc">{product.description}</p>}
        <div className="product-price-row">
          <div>
            <span className="product-price">₹{product.price?.toLocaleString('en-IN')}</span>
            {product.original_price && (
              <span className="product-original-price">₹{product.original_price.toLocaleString('en-IN')}</span>
            )}
          </div>
          <span className="view-btn">View 360°</span>
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
        <a href="/" className="nav-logo" aria-label="Arhat Shop Home">
          <LogoMark />
          <div className="nav-wordmark">
            <span className="kick">ARHAT</span>
            <span className="name">SHOP</span>
          </div>
        </a>
        <ul className="nav-links" role="list">
          <li><a href="#products">Products</a></li>
          <li><a href="#categories">Categories</a></li>
          <li><a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer">Contact</a></li>
        </ul>
        <a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer"
          className="glow-btn nav-cta" id="nav-whatsapp-btn">
          <span>Order Now</span>
        </a>
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

          <a href="#products" className="glow-btn hero-cta" id="hero-shop-now-btn">
            <span>Shop Now</span>
          </a>
        </div>

        {/* 3D Ring Carousel */}
        <RingCarousel products={products} />
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
          <span className="section-sub">Tap to View 360°</span>
        </div>

        {/* Search + Filter */}
        <div style={{ display: 'flex', gap: 12, marginBottom: 32, flexWrap: 'wrap' }}>
          <input
            type="search"
            placeholder="Search products..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            className="form-input"
            style={{ flex: 1, minWidth: 200 }}
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
          <div className="footer-brand">Arhat Shop</div>
          <ul className="footer-links">
            <li><a href="#products">Products</a></li>
            <li><a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer">WhatsApp</a></li>
            <li><a href="/admin">Admin</a></li>
          </ul>
          <p className="footer-copy">© {new Date().getFullYear()} Arhat Shop. All rights reserved.</p>
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
