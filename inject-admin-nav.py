with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

mobile_nav = '''
      {/* Mobile Bottom Navigation */}
      <nav className="admin-mobile-nav">
        <button onClick={() => { setActiveTab("products"); setShowForm(false); }} className={activeTab === "products" && !showForm ? "active" : ""}>
          <div style={{ fontSize: '20px', marginBottom: '4px' }}>??</div>
          <span>Products</span>
        </button>
        <button onClick={() => { setShowForm(true); setEditProduct(null); setActiveTab("products"); }} className={showForm && !editProduct ? "active" : ""}>
          <div style={{ fontSize: '20px', marginBottom: '4px' }}>?</div>
          <span>Add</span>
        </button>
        <button onClick={() => { setActiveTab("bill"); setShowForm(false); }} className={activeTab === "bill" && !showForm ? "active" : ""}>
          <div style={{ fontSize: '20px', marginBottom: '4px' }}>??</div>
          <span>POS</span>
        </button>
        <button onClick={handleLogout} style={{ color: "var(--red)" }}>
          <div style={{ fontSize: '20px', marginBottom: '4px' }}>??</div>
          <span>Logout</span>
        </button>
      </nav>
      
      {/* Main Content Area */}
'''

# Inject mobile_nav right before the <main className="admin-main">
js = js.replace(
    '      {/* Main */}\n      <main className="admin-main">',
    mobile_nav + '      <main className="admin-main">'
)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Admin mobile nav injected!")
