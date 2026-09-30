import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

billing_component = '''
function BillingSystem({ products, onUpdateStock, showToast }) {
  const [cart, setCart] = useState([]);
  const [selectedProductId, setSelectedProductId] = useState("");
  const [qty, setQty] = useState(1);
  const [processing, setProcessing] = useState(false);

  const selectedProduct = products.find(p => p.id === selectedProductId);

  const addToCart = () => {
    if (!selectedProduct) return;
    if (qty <= 0) return;
    if (qty > selectedProduct.stock) {
      showToast("Cannot add more than available stock!", "error");
      return;
    }
    
    setCart(prev => {
      const existing = prev.find(item => item.product.id === selectedProduct.id);
      if (existing) {
        if (existing.qty + qty > selectedProduct.stock) {
          showToast("Cannot add more than available stock!", "error");
          return prev;
        }
        return prev.map(item => item.product.id === selectedProduct.id ? { ...item, qty: item.qty + qty } : item);
      }
      return [...prev, { product: selectedProduct, qty }];
    });
    setQty(1);
    setSelectedProductId("");
  };

  const removeFromCart = (id) => {
    setCart(prev => prev.filter(item => item.product.id !== id));
  };

  const total = cart.reduce((sum, item) => sum + (item.product.price * item.qty), 0);

  const handleCheckout = async () => {
    if (cart.length === 0) return;
    setProcessing(true);
    try {
      for (const item of cart) {
        const updatedProduct = { ...item.product, stock: item.product.stock - item.qty };
        const res = await fetch("/api/products", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(updatedProduct)
        });
        if (!res.ok) throw new Error("Failed to update stock for " + item.product.name);
        
        onUpdateStock(updatedProduct);
      }
      showToast("Bill generated successfully! Stock has been deducted.", "success");
      setCart([]);
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="admin-table-wrap" style={{ padding: '24px' }}>
      <h2 style={{ fontSize: '20px', fontWeight: '700', marginBottom: '24px', color: 'var(--primary)' }}>Create New Bill (POS)</h2>
      
      <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
        <div style={{ flex: '1 1 300px' }}>
          <div style={{ background: 'var(--bg3)', padding: '20px', borderRadius: '16px', border: '1px solid var(--border)' }}>
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Add Product to Bill</h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', marginBottom: '8px', color: 'var(--text-muted)' }}>Select Product</label>
                <select 
                  value={selectedProductId} 
                  onChange={e => setSelectedProductId(e.target.value)}
                  style={{ width: '100%', padding: '12px', borderRadius: '10px', border: '1px solid var(--border)', outline: 'none' }}
                >
                  <option value="">-- Choose Product --</option>
                  {products.filter(p => p.stock > 0).map(p => (
                    <option key={p.id} value={p.id}>{p.name} (?{p.price}) - {p.stock} in stock</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', marginBottom: '8px', color: 'var(--text-muted)' }}>Quantity</label>
                <input 
                  type="number" 
                  min="1" 
                  max={selectedProduct?.stock || 1}
                  value={qty} 
                  onChange={e => setQty(parseInt(e.target.value) || 1)}
                  style={{ width: '100%', padding: '12px', borderRadius: '10px', border: '1px solid var(--border)', outline: 'none' }}
                />
              </div>
              
              <button 
                onClick={addToCart}
                disabled={!selectedProduct}
                style={{ width: '100%', padding: '12px', borderRadius: '10px', background: selectedProduct ? 'var(--primary)' : 'var(--border)', color: '#fff', fontWeight: '600', border: 'none', cursor: selectedProduct ? 'pointer' : 'not-allowed', transition: 'all 0.2s' }}
              >
                Add to Bill
              </button>
            </div>
          </div>
        </div>
        
        <div style={{ flex: '2 1 400px' }}>
          <div style={{ border: '1px solid var(--border)', borderRadius: '16px', overflow: 'hidden' }}>
            <div style={{ background: 'var(--surface)', padding: '16px 20px', borderBottom: '1px solid var(--border)', fontWeight: '600' }}>Current Bill</div>
            <div style={{ padding: '20px', background: 'var(--surface)' }}>
              {cart.length === 0 ? (
                <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '40px 0' }}>No items added yet</div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {cart.map((item, idx) => (
                    <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '12px', borderBottom: '1px dashed var(--border)' }}>
                      <div>
                        <div style={{ fontWeight: '600', fontSize: '15px' }}>{item.product.name}</div>
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>?{item.product.price} x {item.qty}</div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                        <div style={{ fontWeight: '700' }}>?{(item.product.price * item.qty).toLocaleString('en-IN')}</div>
                        <button onClick={() => removeFromCart(item.product.id)} style={{ background: 'none', border: 'none', color: 'var(--red)', cursor: 'pointer', fontSize: '18px' }}>?</button>
                      </div>
                    </div>
                  ))}
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '12px', marginTop: '12px' }}>
                    <div style={{ fontSize: '18px', fontWeight: '600' }}>Total</div>
                    <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--primary)' }}>?{total.toLocaleString('en-IN')}</div>
                  </div>
                  
                  <button 
                    onClick={handleCheckout}
                    disabled={processing}
                    style={{ width: '100%', padding: '16px', marginTop: '24px', borderRadius: '12px', background: '#10b981', color: '#fff', fontWeight: '700', fontSize: '16px', border: 'none', cursor: processing ? 'wait' : 'pointer', transition: 'all 0.2s', boxShadow: '0 4px 12px rgba(16, 185, 129, 0.2)' }}
                  >
                    {processing ? 'Processing...' : 'Confirm Bill & Reduce Stock'}
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
'''

# 1. Inject BillingSystem before AdminPanel
js = js.replace('// ===== ADMIN PAGE =====', billing_component + '\n\n// ===== ADMIN PAGE =====')

# 2. Add the sidebar tab
old_tab = '''          <li>
            <button onClick={() => { setShowForm(true); setEditProduct(null); }}
className={showForm && !editProduct ? "active" : ""}
id="tab-add-product">
              ? Add Product
            </button>
          </li>'''

new_tab = '''          <li>
            <button onClick={() => { setShowForm(true); setEditProduct(null); setActiveTab("products"); }}
className={showForm && !editProduct && activeTab === "products" ? "active" : ""}
id="tab-add-product">
              ? Add Product
            </button>
          </li>
          <li>
            <button onClick={() => { setActiveTab("bill"); setShowForm(false); }}
className={activeTab === "bill" ? "active" : ""}
id="tab-billing">
              ?? Billing 
            </button>
          </li>'''

js = js.replace(old_tab, new_tab)

# 3. Update the header title
js = js.replace(
    '{activeTab === "products" ? "Product Management" : "Dashboard"}',
    '{activeTab === "products" ? "Product Management" : activeTab === "bill" ? "Billing " : "Dashboard"}'
)

# 4. Conditionally render the table and the billing system
old_table = '''        {/* Products Table */}
        {loading ? (
          <div className="page-loader">
            <div className="loader-ring" />
            <p className="loader-text">Loading products...</p>
          </div>
        ) : (
          <div className="admin-table-wrap">'''

new_table = '''        {/* Main Content */}
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
          <div className="admin-table-wrap">'''

js = js.replace(old_table, new_table)

# 5. Fix the end of the products table conditional rendering
# Right now, there is a `)}` closing the `!loading` ternary. Since we added a nested ternary, we need an extra `) : null}` for when neither tab matches (like showForm).
# Actually, the original was `{loading ? (...) : ( <div className="admin-table-wrap"> ... </div> )}`
# The `showForm` is rendered completely separate earlier!
# Let's check how the file ends.

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Billing System partially injected!")
