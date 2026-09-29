with open('app/globals.css', 'a', encoding='utf-8') as f:
    f.write("""
/* ADMIN MOBILE NAV (Bottom Bar) */
.admin-mobile-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: var(--surface);
  border-top: 1px solid var(--border);
  z-index: 1000;
  box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
}

@media (max-width: 900px) {
  .admin-mobile-nav {
    display: flex;
    justify-content: space-around;
    padding: 10px 0 16px 0;
  }
  
  .admin-mobile-nav button {
    background: none;
    border: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: var(--text-muted);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    cursor: pointer;
  }
  
  .admin-mobile-nav button.active {
    color: var(--primary);
  }
  
  .admin-mobile-nav button.active div {
    filter: drop-shadow(0 2px 4px rgba(15,23,42,0.2));
  }
}
""")

print("Admin mobile nav CSS injected!")
