import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

marquee_css = '''
/* MARQUEE ANIMATION */
.hero-marquee-container {
  position: absolute;
  bottom: 0;
  width: 100%;
  overflow: hidden;
  padding-bottom: 48px;
  display: flex;
  align-items: center;
  mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
  -webkit-mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
  z-index: 5;
}
.hero-marquee {
  display: flex;
  gap: 20px;
  width: max-content;
  animation: scrollMarquee 35s linear infinite;
}
.hero-marquee:hover {
  animation-play-state: paused;
}
@keyframes scrollMarquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(-50% - 10px)); }
}
.marquee-card {
  width: 200px;
  height: 260px;
  border-radius: 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.06);
  overflow: hidden;
  flex-shrink: 0;
  position: relative;
  transition: transform .3s var(--ease-out);
  cursor: pointer;
}
.marquee-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.1);
  border-color: var(--border2);
}
.marquee-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .5s var(--ease-out);
}
.marquee-card:hover img {
  transform: scale(1.05);
}
.marquee-badge {
  position: absolute;
  bottom: 12px;
  left: 12px;
  right: 12px;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(8px);
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  color: var(--primary);
  border: 1px solid var(--border);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
'''

if 'hero-marquee-container' not in css:
    css = css + marquee_css

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

marquee_jsx = '''
        {/* Marquee Animation */}
        <div className="hero-marquee-container">
          <div className="hero-marquee">
            {[...(products && products.length > 0 ? products : Array(5).fill({ name: 'Coming Soon' })), ...(products && products.length > 0 ? products : Array(5).fill({ name: 'Coming Soon' })), ...(products && products.length > 0 ? products : Array(5).fill({ name: 'Coming Soon' }))].slice(0, 15).map((product, i) => (
              <div key={mq--} className="marquee-card" onClick={() => product.id && document.getElementById('products').scrollIntoView({ behavior: 'smooth' })}>
                {(product.enhanced_image_url || product.image_url) ? (
                  <img src={product.enhanced_image_url || product.image_url} alt={product.name} loading="lazy" />
                ) : (
                  <div className="product-img-placeholder">
                    <span className="placeholder-icon">??</span>
                  </div>
                )}
                <div className="marquee-badge">{product.name}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
'''

js = js.replace('{/* Ring Carousel Removed for Light Theme */}\n      </section>', marquee_jsx)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Added Marquee animation!")
