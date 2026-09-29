with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Current button:
# <a href="#products" className="glow-btn hero-cta" id="hero-shop-now-btn">
#   <span>Shop Now</span>
# </a>

new_button = '''            <a href="#products" className="hero-cta-primary" id="hero-shop-now-btn">
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                Shop Now
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ transition: 'transform 0.3s ease' }}>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </span>
            </a>'''

import re
js = re.sub(
    r'<a href="#products" className="glow-btn hero-cta".*?</a>',
    new_button,
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Shop Now button improved!")
