with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_carousel = '''// ===== MARQUEE CAROUSEL =====
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
              <div style={{ color: '#fff', fontWeight: '600', fontSize: '14px', textShadow: '0 2px 4px rgba(0,0,0,0.3)' }}>\u20B9{product.price?.toLocaleString('en-IN')}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}'''

import re
# Replace RingCarousel function
js = re.sub(
    r'// ===== 3D RING CAROUSEL =====.*?function RingCarousel\(\{ products \}\) \{.*?\}(?=\n\n// ===== PRODUCT CARD =====)',
    new_carousel,
    js,
    flags=re.DOTALL
)

# Also replace <RingCarousel products={products} /> with <MarqueeCarousel products={products} />
js = js.replace('<RingCarousel products={products} />', '<MarqueeCarousel products={products} />')

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Replaced RingCarousel with MarqueeCarousel!")
