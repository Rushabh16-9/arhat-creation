"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);



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

function Product360Modal({ product, onClose, onAddToCart, userProfile, onSignIn }) {
  const [location, setLocation] = useState(userProfile?.address || '');
  const [qty, setQty] = useState(1);
  const [isExpanded, setIsExpanded] = useState(false);
  const [view360Data, setView360Data] = useState(null);
  const [loadingGemini, setLoadingGemini] = useState(false);
  const [showAddressBanner, setShowAddressBanner] = useState(false);
  const WA = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '919082799791';

  // Detect if user changed their saved address
  const isAddressModified = userProfile?.address && location !== userProfile.address && location.trim() !== '';
  const locationEmpty = !location.trim();

  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = ''; };
  }, []);

  function handleBuyNow() {
    if (locationEmpty) return;
    const discount = product.original_price ? Math.round((1 - product.price / product.original_price) * 100) : 0;
    const msg = [
      `*NEW DIRECT ORDER*`,
      `---------------------------------------`,
      `*Product:* ${product.name}`,
      `*Category:* ${product.category || 'General'}`,
      `*Price:* \u20b9${product.price.toLocaleString('en-IN')}${discount ? ` (${discount}% OFF)` : ''}`,
      `*Quantity:* ${qty}`,
      `---------------------------------------`,
      `*Total:* \u20b9${(product.price * qty).toLocaleString('en-IN')}`,
      '',
      `*Delivery Location:* ${location}`,
      '',
      `*Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,
      `---------------------------------------`,
      `_Sent securely via Arhat Creation_`
    ].join('\n');
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(msg)}`, '_blank');
  }

  const handleAddToCartClick = () => {
    if (locationEmpty) return;
    onAddToCart(product, qty);
  };

  const stockStatus = product.stock > 10 ? 'good' : product.stock > 0 ? 'low' : 'none';
  const stockLabel = product.stock > 10 ? `In Stock (${product.stock} units)` : product.stock > 0 ? `Only ${product.stock} left` : 'Out of Stock';

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal-box" style={{ position: 'relative' }}>
        <button className="modal-close" onClick={onClose} aria-label="Close modal">&times;</button>
        <div className="modal-inner">
          {/* Gallery */}
          <div className="modal-gallery" style={{ padding: '20px', background: 'var(--bg3)', borderRadius: '20px', marginBottom: '20px' }}>
            <div className="main-image-wrap" style={{ position: 'relative', width: '100%', aspectRatio: '1', borderRadius: '14px', overflow: 'hidden' }}>
              {(product.enhanced_image_url || product.image_url) ? (
                <img src={product.enhanced_image_url || product.image_url} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              ) : (
                <div style={{ width: '100%', height: '100%', background: 'linear-gradient(155deg,#1a2535,#0d1520)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 60 }}>*</div>
              )}
            </div>
          </div>

          {/* Details */}
          <div className="modal-details">
            {product.category && <div className="modal-category">{product.category}</div>}
            <h2 className="modal-title">{product.name}</h2>
            {product.description && (
              <div style={{ marginBottom: '8px' }}>
                <p className="modal-desc" style={{ display: isExpanded ? 'block' : '-webkit-box', WebkitLineClamp: isExpanded ? 'unset' : 3, WebkitBoxOrient: 'vertical', overflow: 'hidden', margin: 0 }}>{product.description}</p>
                {product.description.length > 100 && (
                  <button onClick={() => setIsExpanded(!isExpanded)} style={{ background: 'transparent', border: 'none', color: 'var(--primary)', fontSize: '13px', fontWeight: '700', cursor: 'pointer', padding: 0, marginTop: '6px' }}>
                    {isExpanded ? 'Read Less' : 'Read More'}
                  </button>
                )}
              </div>
            )}

            <div className="modal-price-row" style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
              <span className="modal-price" style={{ fontSize: '28px', fontWeight: '800', color: 'var(--primary)' }}>{"\u20b9"}{product.price?.toLocaleString('en-IN')}</span>
              {product.original_price && (
                <>
                  <span style={{ textDecoration: 'line-through', color: 'var(--text-dim)', fontSize: '18px' }}>{"\u20b9"}{product.original_price.toLocaleString('en-IN')}</span>
                  <span style={{ background: '#10b981', color: '#fff', padding: '4px 10px', borderRadius: '8px', fontSize: '13px', fontWeight: '700' }}>{Math.round((1 - product.price / product.original_price) * 100)}% OFF</span>
                </>
              )}
            </div>

            <div className="modal-divider" />

            {/* Order Section */}
            <div className="order-section" style={{ background: '#fff', borderRadius: '20px', padding: '20px', boxShadow: '0 4px 20px rgba(0,0,0,0.04)', border: '1px solid #f1f5f9', marginTop: '16px' }}>
              <h4 style={{ margin: '0 0 16px 0', fontSize: '16px', fontWeight: '800', color: '#0f172a' }}>Place Your Order</h4>

              {/* Delivery Address */}
              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '6px' }}>Delivery Address *</label>
                <textarea
                  placeholder="Enter your full delivery address..."
                  value={location}
                  onChange={e => setLocation(e.target.value)}
                  rows={2}
                  style={{ width: '100%', padding: '12px 14px', fontSize: '14px', color: '#334155', background: '#f8fafc', border: `1.5px solid ${locationEmpty ? '#fca5a5' : isAddressModified ? '#fbbf24' : '#cbd5e1'}`, borderRadius: '12px', outline: 'none', resize: 'none', transition: 'border-color 0.2s', boxSizing: 'border-box' }}
                  onFocus={e => { e.currentTarget.style.borderColor = 'var(--primary)'; e.currentTarget.style.background = '#fff'; }}
                  onBlur={e => { e.currentTarget.style.background = '#f8fafc'; e.currentTarget.style.borderColor = locationEmpty ? '#fca5a5' : isAddressModified ? '#fbbf24' : '#cbd5e1'; }}
                />
                {locationEmpty && <p style={{ fontSize: '11px', color: '#ef4444', margin: '4px 0 0 2px', fontWeight: '600' }}>Address is required to place order</p>}

                {/* Address action banner */}
                {isAddressModified && (
                  <div style={{ marginTop: '8px', padding: '10px 12px', background: '#fffbeb', border: '1px solid #fbbf24', borderRadius: '10px', display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
                    <span style={{ fontSize: '12px', color: '#92400e', flex: 1, minWidth: '120px' }}>You changed your address.</span>
                    <div style={{ display: 'flex', gap: '6px' }}>
                      <button onClick={() => onSignIn('saveAddress', location)} style={{ fontSize: '11px', padding: '5px 10px', background: '#0f172a', color: '#fff', border: 'none', borderRadius: '7px', cursor: 'pointer', fontWeight: '700' }}>Save to Profile</button>
                      <button onClick={() => {}} style={{ fontSize: '11px', padding: '5px 10px', background: '#fff', color: '#0f172a', border: '1px solid #cbd5e1', borderRadius: '7px', cursor: 'pointer', fontWeight: '600' }}>Use Just This Time</button>
                    </div>
                  </div>
                )}

                {!userProfile?.name && (
                  <button onClick={() => onSignIn()} style={{ marginTop: '8px', fontSize: '12px', color: 'var(--primary)', fontWeight: '700', background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}>Sign in to auto-fill your address</button>
                )}
              </div>

              {/* Quantity */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px', background: '#f8fafc', padding: '14px 16px', borderRadius: '14px', border: '1px solid #e2e8f0' }}>
                <span style={{ fontSize: '14px', fontWeight: '700', color: '#334155' }}>Quantity</span>
                <div style={{ display: 'flex', alignItems: 'center', background: '#fff', borderRadius: '999px', border: '1px solid #cbd5e1', overflow: 'hidden' }}>
                  <button onClick={() => setQty(q => Math.max(1, q - 1))} style={{ width: '38px', height: '38px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px', color: '#475569', cursor: 'pointer', background: 'transparent', border: 'none' }}>-</button>
                  <span style={{ width: '36px', textAlign: 'center', fontSize: '15px', fontWeight: '800', color: '#0f172a' }}>{qty}</span>
                  <button onClick={() => setQty(q => q + 1)} style={{ width: '38px', height: '38px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px', color: '#475569', cursor: 'pointer', background: 'transparent', border: 'none' }}>+</button>
                </div>
              </div>

              {/* Total */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', padding: '0 2px' }}>
                <span style={{ fontSize: '14px', color: '#64748b', fontWeight: '500' }}>Total Amount</span>
                <span style={{ color: '#0f172a', fontSize: '22px', fontWeight: '800' }}>{"\u20b9"}{(product.price * qty).toLocaleString('en-IN')}</span>
              </div>

              {/* Buttons */}
              <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                <button
                  onClick={handleAddToCartClick}
                  disabled={locationEmpty}
                  title={locationEmpty ? 'Enter delivery address first' : 'Add to Cart'}
                  style={{ flex: '1 1 120px', padding: '14px', borderRadius: '14px', background: locationEmpty ? '#f1f5f9' : 'var(--bg3)', color: locationEmpty ? '#94a3b8' : 'var(--primary)', fontSize: '14px', fontWeight: '800', border: `2px solid ${locationEmpty ? '#e2e8f0' : 'var(--primary)'}`, cursor: locationEmpty ? 'not-allowed' : 'pointer', transition: 'all 0.2s', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}
                >
                  Add to Cart
                </button>
                <button
                  onClick={handleBuyNow}
                  disabled={locationEmpty}
                  title={locationEmpty ? 'Enter delivery address first' : 'Buy Now via WhatsApp'}
                  style={{ flex: '1 1 120px', padding: '14px', borderRadius: '14px', background: locationEmpty ? '#94a3b8' : 'var(--primary)', color: '#fff', fontSize: '14px', fontWeight: '800', border: 'none', cursor: locationEmpty ? 'not-allowed' : 'pointer', boxShadow: locationEmpty ? 'none' : '0 8px 24px rgba(0,150,255,0.25)', transition: 'all 0.2s', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}
                >
                  Buy Now
                </button>
              </div>
              {locationEmpty && (
                <p style={{ fontSize: '12px', color: '#ef4444', textAlign: 'center', marginTop: '10px', fontWeight: '600' }}>Please enter a delivery address above to continue</p>
              )}
              {!locationEmpty && <p style={{ fontSize: '11px', color: '#94a3b8', textAlign: 'center', marginTop: '10px' }}>Buy Now opens WhatsApp instantly</p>}
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
    <div className="product-card" onClick={onClick} role="button" tabIndex={0} onKeyDown={e => e.key === 'Enter' && onClick()} id={`product-${product.id}`}>
      <div className="product-img-wrap">
        {(product.enhanced_image_url || product.image_url) ? (
          <img src={product.enhanced_image_url || product.image_url} alt={product.name} />
        ) : (
          <div className="product-img-placeholder">
            <span className="placeholder-icon">📦</span>
          </div>
        )}
        {discount > 0 && <div className="badge-discount">-{discount}%</div>}
      </div>

      <div className="product-body">
        {product.category && (
          <div className="product-category-tag">{product.category}</div>
        )}
        <h3 className="product-name">{product.name}</h3>
        {product.description && (
          <p className="product-desc">{product.description}</p>
        )}
        <div className="product-price-block" style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', gap: '8px', marginTop: 'auto', paddingTop: '10px' }}>
          <span className="product-price">{"₹"}{product.price?.toLocaleString('en-IN')}</span>
          {product.original_price && (
            <span className="product-orig-price">{"₹"}{product.original_price.toLocaleString('en-IN')}</span>
          )}
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



// ===== USER AUTH / PROFILE MODAL =====
function UserProfileModal({ isOpen, onClose, userProfile, setUserProfile, showToast, initialMode, initialAddress }) {
  // 'login' | 'sent' | 'profile'
  const [authStep, setAuthStep] = useState('login');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ name: '', phone: '', address: '' });

  useEffect(() => {
    if (isOpen) {
      setFormData(prev => {
        const base = { ...userProfile };
        if (initialMode === 'saveAddress' && initialAddress) {
          base.address = initialAddress;
        }
        return base;
      });
      setAuthStep(userProfile.name ? 'profile' : 'login');
      setEmail('');
    }
  }, [isOpen, userProfile, initialMode, initialAddress]);

  // Listen for magic-link sign-in and auto-advance to profile step
  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      if ((event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') && session?.user) {
        setAuthStep('profile');
        showToast('Signed in! Please complete your profile.', 'success', 3000);
      }
    });
    return () => subscription.unsubscribe();
  }, []);

  const handleSendLink = async () => {
    if (!email.trim()) return;
    setLoading(true);
    try {
      const { error } = await supabase.auth.signInWithOtp({
        email: email.trim(),
        options: { shouldCreateUser: true }
      });
      if (error) throw error;
      setAuthStep('sent');
      showToast('Sign-in link sent! Check your inbox.', 'success', 4000);
    } catch (e) {
      showToast(e.message || 'Failed to send link. Try again.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = () => {
    setUserProfile(formData);
    localStorage.setItem('arhat_user_profile', JSON.stringify(formData));
    showToast('Profile saved!', 'success', 2000);
    onClose();
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    setUserProfile({ name: '', phone: '', address: '' });
    localStorage.removeItem('arhat_user_profile');
    showToast('Signed out.', 'info', 2000);
    setAuthStep('login');
    onClose();
  };

  if (!isOpen) return null;

  const inputStyle = {
    width: '100%', padding: '14px 16px', borderRadius: '12px',
    border: '1.5px solid var(--border)', outline: 'none', fontSize: '15px',
    boxSizing: 'border-box', transition: 'border-color 0.2s', fontFamily: 'inherit'
  };
  const btnPrimary = {
    width: '100%', padding: '15px', background: 'var(--primary)', color: '#fff',
    fontSize: '15px', fontWeight: '800', border: 'none', borderRadius: '12px',
    cursor: loading ? 'not-allowed' : 'pointer', marginTop: '8px', opacity: loading ? 0.7 : 1
  };

  return (
    <>
      <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.55)', zIndex: 9998, backdropFilter: 'blur(4px)' }} onClick={onClose} />
      <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: 'calc(100% - 32px)', maxWidth: '400px', background: '#fff', borderRadius: '24px', zIndex: 9999, padding: '28px', boxShadow: '0 24px 48px rgba(0,0,0,0.15)', maxHeight: '90vh', overflowY: 'auto' }}>

        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ margin: 0, fontSize: '22px', fontWeight: '800', color: 'var(--primary)' }}>
            {authStep === 'login' ? 'Sign In' : authStep === 'sent' ? 'Check Your Email' : (userProfile.name ? 'Your Profile' : 'Complete Profile')}
          </h2>
          <button onClick={onClose} style={{ background: 'var(--bg3)', border: 'none', width: '32px', height: '32px', borderRadius: '50%', cursor: 'pointer', display: 'grid', placeItems: 'center', fontSize: '18px', color: 'var(--text)' }}>&times;</button>
        </div>

        {/* Step 1: Enter Email */}
        {authStep === 'login' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <p style={{ color: 'var(--text-muted)', fontSize: '14px', margin: 0, lineHeight: 1.6 }}>
              Enter your email — we'll send you a secure sign-in link. No password needed!
            </p>
            <input
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSendLink()}
              style={inputStyle}
              autoFocus
            />
            <button onClick={handleSendLink} disabled={loading} style={btnPrimary}>
              {loading ? 'Sending...' : 'Send Sign-In Link'}
            </button>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', textAlign: 'center', margin: 0 }}>
              Already have a profile saved?{' '}
              <button onClick={() => setAuthStep('profile')} style={{ background: 'none', border: 'none', color: 'var(--primary)', fontWeight: 700, cursor: 'pointer', fontSize: '12px', padding: 0 }}>
                Skip to profile
              </button>
            </p>
          </div>
        )}

        {/* Step 2: Email Sent — waiting */}
        {authStep === 'sent' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', textAlign: 'center' }}>
            {/* Icon */}
            <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: '#eff6ff', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto' }}>
              <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
              </svg>
            </div>
            <div>
              <p style={{ fontWeight: '800', fontSize: '16px', color: '#0f172a', margin: '0 0 8px 0' }}>Link sent to</p>
              <p style={{ fontWeight: '700', fontSize: '15px', color: 'var(--primary)', margin: 0, wordBreak: 'break-all' }}>{email}</p>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '14px', margin: 0, lineHeight: 1.6 }}>
              Click the link in your email to sign in. This tab will update automatically once you click it.
            </p>
            <div style={{ background: '#f8fafc', borderRadius: '12px', padding: '12px', fontSize: '13px', color: '#64748b' }}>
              Didn't get the email? Check your spam folder.
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button onClick={handleSendLink} disabled={loading} style={{ flex: 1, padding: '12px', background: 'var(--bg3)', color: 'var(--primary)', border: '1.5px solid var(--primary)', borderRadius: '10px', fontSize: '13px', fontWeight: '700', cursor: 'pointer' }}>
                {loading ? 'Sending...' : 'Resend Link'}
              </button>
              <button onClick={() => setAuthStep('login')} style={{ flex: 1, padding: '12px', background: 'var(--bg3)', color: 'var(--text-muted)', border: '1.5px solid var(--border)', borderRadius: '10px', fontSize: '13px', fontWeight: '700', cursor: 'pointer' }}>
                Change Email
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Profile */}
        {authStep === 'profile' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: '700', marginBottom: '6px', color: 'var(--text)' }}>Full Name</label>
              <input type="text" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} placeholder="E.g. Rahul Sharma" style={inputStyle} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: '700', marginBottom: '6px', color: 'var(--text)' }}>Phone Number</label>
              <input type="tel" value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} placeholder="E.g. +91 98765 43210" style={inputStyle} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: '700', marginBottom: '6px', color: 'var(--text)' }}>Default Delivery Address</label>
              <textarea value={formData.address} onChange={e => setFormData({...formData, address: e.target.value})} placeholder="Enter your full address..." rows={3} style={{ ...inputStyle, resize: 'vertical' }} />
            </div>
            <button onClick={handleSaveProfile} style={btnPrimary}>Save Profile</button>
            <button onClick={handleSignOut} style={{ width: '100%', padding: '12px', background: 'none', border: '1.5px solid #fca5a5', color: '#ef4444', fontSize: '14px', fontWeight: '700', borderRadius: '12px', cursor: 'pointer', marginTop: '4px' }}>Sign Out</button>
          </div>
        )}
      </div>
    </>
  );
}

// ===== CART SIDEBAR =====
function CartSidebar({ cart, setCart, isOpen, onClose, WA, userProfile }) {
  const cartTotal = cart.reduce((sum, item) => sum + (item.product.price * item.qty), 0);

  const handleCheckout = () => {
    if (cart.length === 0) return;
    const msg = [
      `*NEW BULK CART ORDER*`,
      `---------------------------------------`,
      ...cart.map(item => `*${item.qty}x* ${item.product.name} -> ₹${(item.product.price * item.qty).toLocaleString('en-IN')}`),
      `---------------------------------------`,
      `*Grand Total:* ₹${cartTotal.toLocaleString('en-IN')}`,
      '',
      ...(userProfile?.address ? [`*Delivery Location:* ${userProfile.address}`, ''] : []),
      `*Order Time:* ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}`,
      '',
      `*Next Step:* ${userProfile?.address ? 'Please confirm if you want delivery to your saved address above.' : 'Please reply to this message with your full delivery address to confirm your order!'}`,
      `---------------------------------------`,
      `_Sent securely via Arhat Creation_`
    ].join('\n');
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(msg)}`, '_blank');
  };

  const updateQty = (id, delta) => {
    setCart(prev => {
      return prev.map(item => {
        if (item.product.id === id) {
          const newQty = Math.max(1, item.qty + delta);
          return { ...item, qty: newQty };
        }
        return item;
      });
    });
  };

  const removeItem = (id) => setCart(prev => prev.filter(item => item.product.id !== id));

  return (
    <>
      {isOpen && <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', zIndex: 9998, backdropFilter: 'blur(4px)' }} onClick={onClose} />}
      <div style={{ position: 'fixed', top: 0, right: isOpen ? 0 : '-400px', width: '100%', maxWidth: '400px', height: '100vh', background: '#fff', zIndex: 9999, transition: 'right 0.3s cubic-bezier(0.2, 0.8, 0.2, 1)', display: 'flex', flexDirection: 'column', boxShadow: '-10px 0 30px rgba(0,0,0,0.1)' }}>
        <div style={{ padding: '24px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ fontSize: '20px', fontWeight: '800', color: 'var(--primary)', margin: 0 }}>Your Cart</h2>
          <button onClick={onClose} style={{ background: 'var(--bg3)', border: 'none', width: '32px', height: '32px', borderRadius: '50%', cursor: 'pointer', display: 'grid', placeItems: 'center' }}>✕</button>
        </div>
        
        <div style={{ flex: 1, overflowY: 'auto', padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {cart.length === 0 ? (
            <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '40px' }}>Your cart is empty.</div>
          ) : (
            cart.map(item => (
              <div key={item.product.id} style={{ display: 'flex', gap: '16px', borderBottom: '1px solid var(--border)', paddingBottom: '16px' }}>
                <div style={{ width: '72px', height: '72px', borderRadius: '12px', background: 'var(--bg3)', overflow: 'hidden', flexShrink: 0 }}>
                  <img src={item.product.enhanced_image_url || item.product.image_url} alt={item.product.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <h4 style={{ margin: '0 0 4px 0', fontSize: '14px', fontWeight: '700', color: 'var(--primary)' }}>{item.product.name}</h4>
                    <button onClick={() => removeItem(item.product.id)} style={{ background: 'none', border: 'none', color: 'var(--red)', cursor: 'pointer', fontSize: '12px', fontWeight: '600' }}>Remove</button>
                  </div>
                  <div style={{ fontSize: '15px', fontWeight: '800', color: 'var(--primary)', marginBottom: '8px' }}>{"₹"}{item.product.price.toLocaleString('en-IN')}</div>
                  <div style={{ display: 'flex', alignItems: 'center', background: '#f8fafc', borderRadius: '8px', border: '1px solid var(--border)', width: 'fit-content' }}>
                    <button onClick={() => updateQty(item.product.id, -1)} style={{ padding: '4px 12px', background: 'none', border: 'none', cursor: 'pointer' }}>-</button>
                    <span style={{ fontSize: '13px', fontWeight: '700', width: '20px', textAlign: 'center' }}>{item.qty}</span>
                    <button onClick={() => updateQty(item.product.id, 1)} style={{ padding: '4px 12px', background: 'none', border: 'none', cursor: 'pointer' }}>+</button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {cart.length > 0 && (
          <div style={{ padding: '24px', borderTop: '1px solid var(--border)', background: '#f8fafc' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', fontSize: '18px', fontWeight: '800', color: 'var(--primary)' }}>
              <span>Total</span>
              <span>{"₹"}{cartTotal.toLocaleString('en-IN')}</span>
            </div>
            <button onClick={handleCheckout} style={{ width: '100%', padding: '16px', background: 'var(--primary)', color: '#fff', fontSize: '16px', fontWeight: '700', borderRadius: '12px', border: 'none', cursor: 'pointer', display: 'flex', justifyContent: 'center', gap: '8px', alignItems: 'center' }}>
              Checkout via WhatsApp
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
            </button>
          </div>
        )}
      </div>
    </>
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
  const [sortOrder, setSortOrder] = useState('featured');
  
  const [cart, setCart] = useState([]);
  const [cartOpen, setCartOpen] = useState(false);

  const [userProfile, setUserProfile] = useState({ name: '', phone: '', address: '' });
  const [profileOpen, setProfileOpen] = useState(false);
  const [profileMode, setProfileMode] = useState(null);
  const [profileInitAddr, setProfileInitAddr] = useState('');

  useEffect(() => {
    const savedCart = localStorage.getItem('arhat_cart');
    if (savedCart) { try { setCart(JSON.parse(savedCart)); } catch(e) {} }

    const saved = localStorage.getItem('arhat_user_profile');
    if (saved) { try { setUserProfile(JSON.parse(saved)); } catch (e) {} }
    // Restore Supabase session
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session?.user && !saved) {
        const meta = session.user.user_metadata || {};
        setUserProfile({ name: meta.name || '', phone: session.user.phone || '', address: meta.address || '' });
      }
    });
  }, []);

  // Persist cart to localStorage on every change (except first render)
  const isFirstRender = useRef(true);
  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    localStorage.setItem('arhat_cart', JSON.stringify(cart));
  }, [cart]);

  const openSignIn = (mode, addr) => {
    setProfileMode(mode || null);
    setProfileInitAddr(addr || '');
    setProfileOpen(true);
  };

  const WA = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '919082799791';

  const handleAddToCart = (product, qty) => {
    setCart(prev => {
      const existing = prev.find(item => item.product.id === product.id);
      if (existing) {
        return prev.map(item => item.product.id === product.id 
          ? { ...item, qty: item.qty + qty } 
          : item);
      }
      return [...prev, { product, qty }];
    });
    showToast(`${product.name} added to cart!`, 'success', 2000);
    setSelectedProduct(null);
  };



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



  const categories = ["All", "Pooja & Samayik Upkaran", "Mens Wear & Accessories", "Gift & Tapasvi Hampers", "Attar", "Dry Fruits", "Other"];

  const filteredProducts = products.filter(p => {
    const matchesSearch = !searchQuery || p.name?.toLowerCase().includes(searchQuery.toLowerCase()) || p.description?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || p.category === selectedCategory;
    return matchesSearch && matchesCategory;
  }).sort((a, b) => {
    if (sortOrder === 'price-asc') return a.price - b.price;
    if (sortOrder === 'price-desc') return b.price - a.price;
    return 0;
  });



  return (

    <>

      {/* NAV */}

            <nav className="main-nav" role="navigation" style={{ 
              height: 'auto',
              minHeight: '64px',
              flexDirection: 'column',
              alignItems: 'stretch',
              padding: '0 24px',
              borderRadius: menuOpen ? '24px' : '32px',
              transition: 'all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)',
              overflow: 'hidden'
            }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%', minHeight: '64px' }}>
          <a href="/" className="nav-logo" aria-label="Arhat Creation Home">
            <LogoMark />
            <div className="nav-wordmark">
              <span className="kick">ARHAT</span>
              <span className="name">CREATION</span>
            </div>
          </a>

          <ul className="nav-links" role="list">
            <li><a href="#products">Products</a></li>

          </ul>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <button onClick={() => openSignIn()} style={{ display: 'flex', alignItems: 'center', gap: '6px', height: '38px', padding: '0 14px', background: 'var(--surface)', color: 'var(--primary)', border: '1.5px solid var(--border)', borderRadius: 10, cursor: 'pointer', fontWeight: 700, fontSize: 14, whiteSpace: 'nowrap' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              <span>{userProfile.name || 'Sign In'}</span>
            </button>
            <button onClick={() => setCartOpen(true)} style={{ display: 'flex', alignItems: 'center', gap: '6px', height: '38px', padding: '0 14px', background: 'var(--primary)', color: '#fff', border: 'none', borderRadius: 10, cursor: 'pointer', fontWeight: 700, fontSize: 14, position: 'relative', whiteSpace: 'nowrap' }}>
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
              <span>Cart{cart.length > 0 ? ` (${cart.length})` : ''}</span>
            </button>
            
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
        
        <div style={{
          display: 'grid',
          gridTemplateRows: menuOpen ? '1fr' : '0fr',
          transition: 'grid-template-rows 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)',
          width: '100%'
        }}>
          <div style={{ overflow: 'hidden' }}>
            <div className="mobile-menu-dropdown" style={{ 
              width: '100%', 
              padding: menuOpen ? '16px 0 24px 0' : '0', 
              display: 'flex', 
              flexDirection: 'column', 
              gap: '16px', 
              borderTop: menuOpen ? '1px solid var(--border)' : '1px solid transparent',
              opacity: menuOpen ? 1 : 0,
              transition: 'all 0.3s ease',
              pointerEvents: menuOpen ? 'auto' : 'none'
            }}>
              <a href="#products" onClick={() => setMenuOpen(false)} style={{ padding: '4px 12px', fontWeight: '600', color: 'var(--text)' }}>Products</a>
              <a href="#categories" onClick={() => setMenuOpen(false)} style={{ padding: '4px 12px', fontWeight: '600', color: 'var(--text)' }}>Categories</a>
              <a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer" style={{ padding: '4px 12px', fontWeight: '600', color: 'var(--primary)' }}>Contact Support</a>
              <a href="/admin" style={{ padding: '4px 12px', fontWeight: '600', color: 'var(--text-muted)' }}>Admin Panel</a>
            </div>
          </div>
        </div>
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
          <select 
            value={sortOrder} 
            onChange={e => setSortOrder(e.target.value)} 
            className="form-input" 
            style={{ flex: '0 0 auto', padding: '12px 16px', background: '#fff', cursor: 'pointer', borderRadius: 10, fontSize: 14 }}
          >
            <option value="featured">Sort: Featured</option>
            <option value="price-asc">Price: Low to High</option>
            <option value="price-desc">Price: High to Low</option>
          </select>

          <div className="filter-chips-wrapper" style={{ display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 8, width: '100%', scrollbarWidth: 'none', WebkitOverflowScrolling: 'touch' }} id="categories" role="group" aria-label="Categories">
            <style>{`.filter-chips-wrapper::-webkit-scrollbar { display: none; }`}</style>


            {categories.map(cat => (

              <button

                key={cat}

                onClick={() => setSelectedCategory(cat)}

                id={`cat-${cat.toLowerCase()}`}

                style={{
                  padding: '10px 20px', borderRadius: '30px', fontSize: 14, fontWeight: 600,
                  background: selectedCategory === cat ? 'var(--primary)' : 'var(--surface)',
                  border: `1px solid ${selectedCategory === cat ? 'var(--primary)' : 'var(--border)'}`,
                  color: selectedCategory === cat ? '#fff' : 'var(--text-muted)',
                  cursor: 'pointer', transition: 'all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1)', 
                  whiteSpace: 'nowrap',
                  boxShadow: selectedCategory === cat ? '0 8px 16px rgba(15,23,42,0.15)' : '0 2px 8px rgba(0,0,0,0.04)'
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
          onAddToCart={handleAddToCart}
          userProfile={userProfile}
          onSignIn={openSignIn}
        />
      )}

      <CartSidebar 
        cart={cart} 
        setCart={setCart} 
        isOpen={cartOpen} 
        onClose={() => setCartOpen(false)} 
        WA={WA} 
        userProfile={userProfile}
      />
      
      <UserProfileModal 
        isOpen={profileOpen}
        onClose={() => setProfileOpen(false)}
        userProfile={userProfile}
        setUserProfile={setUserProfile}
        showToast={showToast}
        initialMode={profileMode}
        initialAddress={profileInitAddr}
      />



      {/* TOAST */}

      <Toast {...toast} />



      

    </>

  );

}

