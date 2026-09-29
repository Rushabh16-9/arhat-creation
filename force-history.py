import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

rupee = '\u20B9'
close_icon = '\u2715'

new_billing_system = '''
function BillingSystem({ products, onUpdateStock, showToast }) {
  const [cart, setCart] = useState([]);
  const [selectedProductId, setSelectedProductId] = useState("");
  const [qty, setQty] = useState(1);
  const [processing, setProcessing] = useState(false);
  
  // Bill History State
  const [pastBills, setPastBills] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('arhat_pos_bills');
    if (saved) {
      try { setPastBills(JSON.parse(saved)); } catch (e) {}
    }
  }, []);

  const selectedProduct = products.find(p => p.id === selectedProductId);

  const addToCart = () => {
    if (!selectedProduct) return;
    if (qty === '' || qty <= 0) return;
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
      
      // Save Bill to History
      const newBill = {
        id: 'BILL-' + Date.now(),
        date: new Date().toISOString(),
        items: cart,
        total: total
      };
      const updatedHistory = [newBill, ...pastBills];
      setPastBills(updatedHistory);
      localStorage.setItem('arhat_pos_bills', JSON.stringify(updatedHistory));
      
      showToast("Bill generated successfully! Saved to history.", "success");
      setCart([]);
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setProcessing(false);
    }
  };

  const handlePrint = (bill) => {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <html>
        <head>
          <title>Receipt ${bill.id}</title>
          <style>
            body { font-family: 'Inter', sans-serif; padding: 40px; color: #111; max-width: 600px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .header h1 { margin: 0; font-size: 24px; }
            .header p { color: #666; margin: 4px 0; }
            .bill-details { margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px dashed #ccc; }
            .items { width: 100%; border-collapse: collapse; }
            .items th { text-align: left; padding-bottom: 10px; border-bottom: 1px solid #eee; }
            .items td { padding: 12px 0; border-bottom: 1px solid #eee; }
            .total-row { font-size: 20px; font-weight: 800; }
            .total-row td { border: none; padding-top: 20px; }
          </style>
        </head>
        <body>
          <div class="header">
            <h1>Arhat Shop</h1>
            <p>Official Tax Invoice / Bill of Supply</p>
          </div>
          <div class="bill-details">
            <p><strong>Bill No:</strong> ${bill.id}</p>
            <p><strong>Date:</strong> ${new Date(bill.date).toLocaleString('en-IN')}</p>
          </div>
          <table class="items">
            <thead>
              <tr>
                <th>Item</th>
                <th>Qty</th>
                <th style="text-align:right">Price</th>
                <th style="text-align:right">Total</th>
              </tr>
            </thead>
            <tbody>
              ${bill.items.map(item => `
                <tr>
                  <td>${item.product.name}</td>
                  <td>${item.qty}</td>
                  <td style="text-align:right">` + rupee + `${item.product.price}</td>
                  <td style="text-align:right">` + rupee + `${item.product.price * item.qty}</td>
                </tr>
              `).join('')}
              <tr class="total-row">
                <td colspan="3" style="text-align:right; padding-right:20px;">Grand Total:</td>
                <td style="text-align:right; color:#10b981;">` + rupee + `${bill.total.toLocaleString('en-IN')}</td>
              </tr>
            </tbody>
          </table>
          <p style="text-align:center; margin-top:50px; color:#888; font-size:14px;">Thank you for your purchase!</p>
          <script>window.print(); setTimeout(() => window.close(), 500);</script>
        </body>
      </html>
    `);
    printWindow.document.close();
  };

  if (showHistory) {
    return (
      <div className="admin-table-wrap" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: '700', color: 'var(--primary)' }}>Past Bills History</h2>
          <button onClick={() => setShowHistory(false)} style={{ padding: '8px 16px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
            Back to POS
          </button>
        </div>
        
        {pastBills.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>No bills generated yet.</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {pastBills.map(bill => (
              <div key={bill.id} style={{ border: '1px solid var(--border)', borderRadius: '12px', padding: '20px', background: '#fff' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px', borderBottom: '1px dashed var(--border)', paddingBottom: '16px' }}>
                  <div>
                    <div style={{ fontWeight: '700', fontSize: '15px' }}>{bill.id}</div>
                    <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>{new Date(bill.date).toLocaleString('en-IN')}</div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <div style={{ fontSize: '18px', fontWeight: '800', color: 'var(--primary)' }}>''' + rupee + '''{bill.total.toLocaleString('en-IN')}</div>
                    <button onClick={() => handlePrint(bill)} style={{ padding: '6px 12px', background: '#10b981', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', fontSize: '13px' }}>Print PDF</button>
                  </div>
                </div>
                <div>
                  {bill.items.map((item, i) => (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '8px' }}>
                      <span style={{ color: 'var(--text-muted)' }}>{item.qty}x {item.product.name}</span>
                      <span style={{ fontWeight: '600' }}>''' + rupee + '''{(item.product.price * item.qty).toLocaleString('en-IN')}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="admin-table-wrap" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: '700', color: 'var(--primary)' }}>Create New Bill (POS)</h2>
        <button onClick={() => setShowHistory(true)} style={{ padding: '10px 20px', background: 'var(--primary)', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
          View Bill History
        </button>
      </div>
      
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
                    <option key={p.id} value={p.id}>{p.name} (''' + rupee + '''{p.price}) - {p.stock} in stock</option>
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
                  onChange={e => {
                    const rawVal = e.target.value;
                    if (rawVal === '') {
                      setQty('');
                      return;
                    }
                    const numVal = parseInt(rawVal);
                    if (selectedProduct && numVal > selectedProduct.stock) {
                      showToast("Cannot add more than available stock!", "error");
                      setQty(selectedProduct.stock);
                    } else {
                      setQty(numVal);
                    }
                  }}
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
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>''' + rupee + '''{item.product.price} x {item.qty}</div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                        <div style={{ fontWeight: '700' }}>''' + rupee + '''{(item.product.price * item.qty).toLocaleString('en-IN')}</div>
                        <button onClick={() => removeFromCart(item.product.id)} style={{ background: 'none', border: 'none', color: 'var(--red)', cursor: 'pointer', fontSize: '18px' }}>''' + close_icon + '''</button>
                      </div>
                    </div>
                  ))}
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '12px', marginTop: '12px' }}>
                    <div style={{ fontSize: '18px', fontWeight: '600' }}>Total</div>
                    <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--primary)' }}>''' + rupee + '''{total.toLocaleString('en-IN')}</div>
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

start_idx = js.find('function BillingSystem({ products, onUpdateStock, showToast }) {')
end_idx = js.find('// ===== ADMIN PAGE =====')

if start_idx != -1 and end_idx != -1:
    js = js[:start_idx] + new_billing_system + '\n\n' + js[end_idx:]
    with open('app/admin/page.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Injected successfully via indexing!")
else:
    print("Could not find start or end index.")
