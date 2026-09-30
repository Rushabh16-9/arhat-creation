import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update the sidebar navigation
js = re.sub(
    r'<ul className="sidebar-nav">.*?<button onClick=\{\(\) => \{ setActiveTab\("products"\); setShowForm\(false\); \}\} className=\{!showForm \? "active" : ""\} id="tab-products">.*?? Add Product\s*</button>\s*</li>',
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
              ?? Billing 
            </button>
          </li>''',
    js,
    flags=re.DOTALL
)

# 2. Update the main header title
js = re.sub(
    r'\{activeTab === "products" \? "Product Management" : "Dashboard"\}',
    '{activeTab === "products" ? "Product Management" : activeTab === "bill" ? "Billing " : "Dashboard"}',
    js
)

# 3. Update the main content rendering
js = re.sub(
    r'\{/\* Products Table \*/\}.*?\{loading \? \(.*?<div className="admin-table-wrap">',
    '''{/* Main Content */}
        {loading ? (
          <div className="page-loader">
            <div className="loader-ring" />
            <p className="loader-text">Loading products...</p>
          </div>
        ) : activeTab === "bill" && !showForm ? (
          <BillingSystem 
            products={products} 
            onUpdateStock={(updatedProduct) => {
              setProducts(prev => prev.map(p => p.id === updatedProduct.id ? updatedProduct : p));
            }}
            showToast={showToast}
          />
        ) : activeTab === "products" && !showForm ? (
          <div className="admin-table-wrap">''',
    js,
    flags=re.DOTALL
)

# 4. Make sure the ternary is properly closed. The previous script might have left it weird.
# Let's just fix it by ensuring `) : null}` is at the end of the table
js = re.sub(
    r'</tbody>\s*</table>\s*</div>\s*\)\s*\}\s*</main>',
    '</tbody>\n            </table>\n          </div>\n        ) : null}\n      </main>',
    js,
    flags=re.DOTALL
)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Tabs and content updated!")
