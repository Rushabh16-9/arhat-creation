const fs = require('fs');
const file = 'd:/real world solutions/arhat-shop/app/page.js';
let content = fs.readFileSync(file, 'utf8');

// 1. Remove Starfield
content = content.replace(/<canvas id="starfield".*?\/>/g, '');

// 2. Fix Hero Heading color
content = content.replace(/background: 'linear-gradient\\(135deg,#00d4ff,#0080ff\\)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'/g, "color: 'var(--primary)'");

// 3. Fix corrupted character in Hero
content = content.replace(/Curated collections.*?Exceptional quality/g, 'Curated collections &middot; Exceptional quality');

// 4. Update Hero CTA Button class
content = content.replace(/className="glow-btn hero-cta"/g, 'className="hero-cta-primary"');

// 5. Remove Ring Carousel
content = content.replace(/<RingCarousel products=\{products\} \/>/g, '{/* Ring Carousel Removed for Light Theme */}');

// 6. Update Category buttons to use the new CSS classes
content = content.replace(/style=\{\{\s*padding: '10px 18px', borderRadius: 10, fontSize: 13, fontWeight: 500,[\s\S]*?whiteSpace: 'nowrap'\s*\}\}/g, 'className={ilter-cat }');

// 7. Fix product placeholder in ProductCard and Modal
content = content.replace(/background: \linear-gradient\\(155deg, \\\$\\{product\\\?\\.color \\|\\| '#1a2535'\\}, #0a0f18\\)\/g, "background: 'var(--bg3)'");
content = content.replace(/color: 'rgba\\(255,255,255,\\.4\\)'/g, "color: 'var(--text-dim)'");
content = content.replace(/opacity: \\.4/g, "color: 'var(--border2)'");

fs.writeFileSync(file, content, 'utf8');
console.log('page.js updated via Node!');
