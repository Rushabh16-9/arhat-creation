with open('app/globals.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_until = -1

for i, line in enumerate(lines):
    if i < skip_until:
        continue
        
    if line.startswith('@media(max-width:768px){ .nav-links') or \
       line.startswith('@media(max-width:640px){ .modal-inner') or \
       line.startswith('@media(max-width:640px){ .modal-viewer') or \
       line.startswith('@media(max-width:768px){ .footer-inner') or \
       line.startswith('@media(max-width:900px){ .admin-sidebar'):
        continue
        
    if line.startswith('@media(max-width:640px){') and 'products-grid' in lines[i+1]:
        skip_until = i + 4
        continue
        
    if line.startswith('@media (max-width: 900px) {') and 'upload-section' in lines[i+1]:
        skip_until = i + 5
        continue
        
    new_lines.append(line)

new_media_queries = """
/* ==========================================================================
   COMPREHENSIVE MOBILE RESPONSIVENESS (PHASES 1 & 2)
   ========================================================================== */

/* TABLET & SMALL DESKTOP (max-width: 900px) */
@media (max-width: 900px) {
  /* Admin Sidebar */
  .admin-sidebar { display: none; }
  .admin-content, .admin-topbar { padding-left: 20px; padding-right: 20px; }
  
  /* Admin Upload Form */
  .upload-section { grid-template-columns: 1fr !important; }
  
  /* Billing POS */
  .admin-table-wrap > div > div { flex: 1 1 100% !important; } /* Make POS columns stack */
}

/* MOBILE (max-width: 768px) */
@media (max-width: 768px) {
  /* Navbar */
  .nav-links { display: none; }
  
  /* Hero Section */
  .hero { min-height: 70vh; padding-top: 60px; }
  .hero-h1 { font-size: 40px; letter-spacing: -0.02em; }
  .hero-sub { font-size: 16px; padding: 0 20px; }
  .hero-cta-primary, .hero-cta-secondary { width: 100%; justify-content: center; }
  .hero-ctas { flex-direction: column; width: 100%; padding: 0 20px; box-sizing: border-box; }
  
  /* Footer */
  .footer-inner { grid-template-columns: 1fr; gap: 32px; text-align: center; }
  .footer-brand-tag { margin: 0 auto; }
}

/* SMALL MOBILE (max-width: 640px) */
@media (max-width: 640px) {
  /* Product Grid */
  .products-grid { grid-template-columns: 1fr; gap: 24px; padding: 0 16px; }
  .product-body { padding: 20px; } 
  .product-name { font-size: 18px; }
  
  /* Product Modal */
  .modal-box { 
    width: 100%; 
    height: 100dvh; 
    max-height: 100dvh; 
    border-radius: 0; 
    margin: 0; 
    display: flex; 
    flex-direction: column;
  }
  .modal-inner { 
    grid-template-columns: 1fr; 
    height: 100%; 
    overflow-y: auto; 
  }
  .modal-viewer { 
    border-radius: 0; 
    min-height: 350px; 
    border-right: none; 
    border-bottom: 1px solid var(--border); 
  }
  .modal-details { 
    padding: 24px; 
    padding-bottom: 100px; /* Space for checkout bar */
  }
  
  /* Admin Panel specific */
  .admin-header { flex-direction: column; align-items: flex-start; gap: 16px; }
  .add-product-btn { width: 100%; justify-content: center; }
  .stats-grid { grid-template-columns: 1fr; }
  
  /* Force tables to scroll */
  .admin-table-wrap { overflow-x: auto; }
  .admin-table { min-width: 600px; }
}

/* FIXED MOBILE CHECKOUT BAR (for modal) */
@media (max-width: 640px) {
  .checkout-mobile-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #fff;
    padding: 16px 24px;
    border-top: 1px solid var(--border);
    box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
}
"""

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
    f.write(new_media_queries)

print("Globals CSS updated with comprehensive responsive queries!")
