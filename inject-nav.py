import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add menuOpen state
js = js.replace(
    "const [products, setProducts] = useState([]);",
    "const [products, setProducts] = useState([]);\n  const [menuOpen, setMenuOpen] = useState(false);"
)

# 2. Add hamburger and mobile menu
old_nav = '''      <nav className="main-nav" role="navigation">

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

          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" /></svg>

          <span>Chat with us</span>

        </a>

      </nav>'''

new_nav = '''      <nav className="main-nav" role="navigation">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
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

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <a href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer"
              className="glow-btn nav-cta" id="nav-whatsapp-btn">
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
      </nav>'''

js = re.sub(
    r'<nav className="main-nav" role="navigation">.*?</nav>',
    lambda _: new_nav,
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Nav injected!")
