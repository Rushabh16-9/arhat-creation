# -*- coding: utf-8 -*-
with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

old_footer_regex = r'<footer className="site-footer">.*?</footer>'

new_footer = """<footer className="site-footer">
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
          <p className="footer-copy">\u00a9 {new Date().getFullYear()} Arhat Creation. All rights reserved.</p>
          <div className="footer-socials" style={{ display: 'flex', gap: '16px' }}>
            <a href="#" aria-label="Instagram" style={{ color: 'var(--text-dim)', fontSize: '13px', fontWeight: '700', letterSpacing: '.1em' }}>IG</a>
            <a href="#" aria-label="Facebook" style={{ color: 'var(--text-dim)', fontSize: '13px', fontWeight: '700', letterSpacing: '.1em' }}>FB</a>
            <a href="#" aria-label="Twitter" style={{ color: 'var(--text-dim)', fontSize: '13px', fontWeight: '700', letterSpacing: '.1em' }}>X</a>
          </div>
        </div>
      </footer>"""

js = re.sub(old_footer_regex, new_footer, js, flags=re.DOTALL)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Footer replaced in page.js!")
