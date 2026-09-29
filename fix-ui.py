import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Starfield
content = re.sub(r'<canvas id="starfield".*?/>', '', content)

# 2. Fix Hero Heading color
content = content.replace("background: 'linear-gradient(135deg,#00d4ff,#0080ff)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'", "color: 'var(--primary)'")

# 3. Fix corrupted character in Hero
content = re.sub(r'Curated collections.*?Exceptional quality', 'Curated collections &middot; Exceptional quality', content)

# 4. Update Hero CTA Button class
content = content.replace('className="glow-btn hero-cta"', 'className="hero-cta-primary"')

# 5. Remove Ring Carousel
content = content.replace('<RingCarousel products={products} />', '{/* Ring Carousel Removed for Light Theme */}')

# 6. Update Category buttons to use the new CSS classes
content = re.sub(r"style=\{\{\s*padding: '10px 18px', borderRadius: 10, fontSize: 13, fontWeight: 500,[\s\S]*?whiteSpace: 'nowrap'\s*\}\}", "className={ilter-cat }", content)

# 7. Fix product placeholder in ProductCard and Modal
content = content.replace("background: linear-gradient(155deg, , #0a0f18)", "background: 'var(--bg3)'")
content = content.replace("color: 'rgba(255,255,255,.4)'", "color: 'var(--text-dim)'")
content = content.replace("opacity: .4", "color: 'var(--border2)'")

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("page.js updated via Python!")
