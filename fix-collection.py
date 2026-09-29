with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_header = '''        {/* PRODUCTS SECTION */}
        <section className="products-section" id="products" style={{ padding: '60px 0' }}>
          <div className="section-header" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', marginBottom: '40px' }}>
            <h2 className="section-title" style={{ fontSize: '42px', fontWeight: '800', color: 'var(--primary)', marginBottom: '12px' }}>Our Collection</h2>
            <p style={{ fontSize: '15px', color: 'var(--text-muted)', fontWeight: '500' }}>
              Explore our curated selection of {filteredProducts.length} premium product{filteredProducts.length !== 1 ? 's' : ''}
            </p>
          </div>
  
          {/* Search + Filter */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '24px', marginBottom: '48px' }}>
            
            {/* Category Pills */}
            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', justifyContent: 'center' }} id="categories" role="group" aria-label="Categories">
              {categories.map(cat => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  id={`cat-${cat.toLowerCase().replace(' ', '-')}`}
                  style={{
                    padding: '12px 24px', 
                    borderRadius: '9999px', 
                    fontSize: '14px', 
                    fontWeight: '600',
                    background: selectedCategory === cat ? 'var(--primary)' : '#fff',
                    border: `1px solid ${selectedCategory === cat ? 'var(--primary)' : 'var(--border)'}`,
                    color: selectedCategory === cat ? '#fff' : 'var(--text-muted)',
                    boxShadow: selectedCategory === cat ? '0 8px 16px rgba(15,23,42,0.15)' : '0 2px 4px rgba(0,0,0,0.02)',
                    cursor: 'pointer', 
                    transition: 'all 0.25s ease', 
                    whiteSpace: 'nowrap',
                    transform: selectedCategory === cat ? 'translateY(-2px)' : 'none'
                  }}
                  onMouseOver={e => { if (selectedCategory !== cat) { e.currentTarget.style.borderColor = 'var(--border2)'; e.currentTarget.style.color = 'var(--primary)'; } }}
                  onMouseOut={e => { if (selectedCategory !== cat) { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-muted)'; } }}
                >
                  {cat}
                </button>
              ))}
            </div>

            {/* Search Bar */}
            <div style={{ position: 'relative', width: '100%', maxWidth: '400px' }}>
              <input
                type="search"
                placeholder="Search products..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="form-input"
                style={{ width: '100%', padding: '14px 20px 14px 44px', borderRadius: '9999px', border: '1px solid var(--border)', background: '#fff', fontSize: '15px', color: 'var(--primary)', boxShadow: '0 4px 12px rgba(0,0,0,0.03)', transition: 'border-color 0.2s, box-shadow 0.2s' }}
                id="product-search"
                onFocus={e => { e.currentTarget.style.borderColor = 'var(--primary)'; e.currentTarget.style.boxShadow = '0 4px 16px rgba(15,23,42,0.1)'; }}
                onBlur={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.03)'; }}
              />
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--text-dim)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)' }}>
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </div>

          </div>'''

import re
js = re.sub(
    r'        \{\/\* PRODUCTS SECTION \*\/\}.*?<\/div>\s*<\/div>\s*\{\/\* loading \?\(\*\/\}\s*\{loading \?',
    new_header + '\n\n        {loading ?',
    js,
    flags=re.DOTALL
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated Our Collection section header!")
