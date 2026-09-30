with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Replace the entire sidebar block up to the View Store link
old_sidebar = """        <ul className="sidebar-nav">
          <li>
            <button onClick={() => { setActiveTab("products"); setShowForm(false); }} className={!showForm ? "active" : ""} id="tab-products">
              ?? Products
            </button>
          </li>
          <li>
            <button onClick={() => { setShowForm(true); setEditProduct(null); }}
className={showForm && !editProduct ? "active" : ""}
id="tab-add-product">
              ? Add Product
            </button>
          </li>
          <li>
            <a href="/" target="_blank" rel="noopener noreferrer" id="view-store-link">"""

new_sidebar = """        <ul className="sidebar-nav">
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
            <button onClick={() => { setActiveTab("bill"); setShowForm(false); }} className={activeTab === "bill" && !showForm ? "active" : ""} id="tab-billing">
              ?? Billing 
            </button>
          </li>
          <li>
            <a href="/" target="_blank" rel="noopener noreferrer" id="view-store-link">"""

if old_sidebar in js:
    js = js.replace(old_sidebar, new_sidebar)
    print("Sidebar replaced successfully.")
else:
    print("Old sidebar exact string not found.")
    
# Let's write it back so I can check if it worked
with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)
