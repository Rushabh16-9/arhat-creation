import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update the sidebar navigation
js = re.sub(
    r'<ul className="sidebar-nav">.*?id="tab-add-product">.*?</button>\s*</li>',
    '''<ul className="sidebar-nav">
          <li>
            <button onClick={() => { setActiveTab("products"); setShowForm(false); }} className={activeTab === "products" && !showForm ? "active" : ""} id="tab-products">
              ?? Products
            </button>
          </li>
          <li>
            <button onClick={() => { setShowForm(true); setEditProduct(null); setActiveTab("products"); }} className={showForm && !editProduct ? "active" : ""} id="tab-add-product">
              ? Add Product
            </button>
          </li>
          <li>
            <button onClick={() => { setActiveTab("bill"); setShowForm(false); }} className={activeTab === "bill" ? "active" : ""} id="tab-billing">
              ?? Billing (POS)
            </button>
          </li>''',
    js,
    flags=re.DOTALL
)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Sidebar replaced successfully with regex.")
