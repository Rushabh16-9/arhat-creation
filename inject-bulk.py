import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

bulk_upload_comp = """
// ===== BULK UPLOAD FORM =====
function BulkUploadForm({ onSave, showToast }) {
  const [queue, setQueue] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [saving, setSaving] = useState(false);
  
  function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    if (!files.length) return;
    const newItems = files.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      file,
      preview: URL.createObjectURL(file),
      name: "", price: "", original_price: "", stock: "", category: CATEGORIES[0], description: ""
    }));
    setQueue([...queue, ...newItems]);
  }
  
  function updateCurrent(field, value) {
    setQueue(q => q.map((item, idx) => idx === currentIndex ? { ...item, [field]: value } : item));
  }
  
  async function uploadImage(file) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("folder", "products");
    const res = await fetch("/api/upload", { method: "POST", body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Upload failed");
    return data.url;
  }
  
  async function handleSaveNext() {
    const item = queue[currentIndex];
    if (!item.name || !item.price) return showToast("Name and price required", "error");
    
    setSaving(true);
    try {
      showToast(`Saving ${item.name}...`, "info");
      const url = await uploadImage(item.file);
      
      const payload = {
        name: item.name,
        description: item.description,
        price: parseFloat(item.price),
        original_price: item.original_price ? parseFloat(item.original_price) : null,
        stock: parseInt(item.stock) || 0,
        category: item.category,
        image_url: url
      };
      
      const res = await fetch("/api/products", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Save failed");
      
      showToast(`${item.name} saved!`, "success");
      onSave(data.product);
      
      if (currentIndex < queue.length - 1) {
         setCurrentIndex(currentIndex + 1);
      } else {
         setQueue([]);
         setCurrentIndex(0);
         showToast("All items in bulk queue processed!", "success");
      }
    } catch (e) {
      showToast("Error: " + e.message, "error");
    } finally {
      setSaving(false);
    }
  }

  function handleRemoveCurrent() {
    const newQ = queue.filter((_, idx) => idx !== currentIndex);
    setQueue(newQ);
    if (currentIndex >= newQ.length && newQ.length > 0) setCurrentIndex(newQ.length - 1);
  }

  if (queue.length === 0) {
    return (
      <div className="upload-section" style={{ textAlign: 'center', padding: '60px 20px' }}>
        <h2 style={{ marginBottom: 16, color: 'var(--primary)' }}>Bulk Image Upload</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: 24 }}>Select multiple images to quickly add many products one by one.</p>
        <label className="glow-btn" style={{ cursor: 'pointer', display: 'inline-flex' }}>
          <span>Select Images</span>
          <input type="file" multiple accept="image/*" onChange={handleFileSelect} style={{ display: 'none' }} />
        </label>
      </div>
    );
  }

  const current = queue[currentIndex];

  return (
    <div className="bulk-form-container" style={{ background: '#fff', borderRadius: 24, border: '1px solid var(--border)', overflow: 'hidden' }}>
      <div style={{ padding: '16px 24px', background: 'var(--bg2)', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ fontSize: 16, fontWeight: 700 }}>Processing {currentIndex + 1} of {queue.length}</h3>
        <button onClick={() => setQueue([])} style={{ color: 'var(--red)', background: 'none', border: 'none', fontWeight: 600, cursor: 'pointer' }}>Cancel Bulk</button>
      </div>
      
      <div className="form-grid" style={{ padding: 24 }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
           <div style={{ position: 'relative', width: '100%', aspectRatio: '1', borderRadius: 16, overflow: 'hidden', background: '#f8fafc', border: '1px solid var(--border)' }}>
             <img src={current.preview} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
           </div>
           <div style={{ display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 8 }}>
             {queue.map((q, idx) => (
                <div key={q.id} onClick={() => setCurrentIndex(idx)} style={{ flexShrink: 0, width: 48, height: 48, borderRadius: 8, overflow: 'hidden', border: idx === currentIndex ? '2px solid var(--primary)' : '1px solid var(--border)', cursor: 'pointer', opacity: idx === currentIndex ? 1 : 0.5 }}>
                  <img src={q.preview} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </div>
             ))}
           </div>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
           <div>
             <label className="form-label">Product Name *</label>
             <input type="text" className="form-input" value={current.name} onChange={e => updateCurrent("name", e.target.value)} placeholder="Rose Barfi" />
           </div>
           <div style={{ display: 'flex', gap: 16 }}>
             <div style={{ flex: 1 }}>
               <label className="form-label">Price *</label>
               <input type="number" className="form-input" value={current.price} onChange={e => updateCurrent("price", e.target.value)} />
             </div>
             <div style={{ flex: 1 }}>
               <label className="form-label">Original Price</label>
               <input type="number" className="form-input" value={current.original_price} onChange={e => updateCurrent("original_price", e.target.value)} />
             </div>
           </div>
           <div style={{ display: 'flex', gap: 16 }}>
             <div style={{ flex: 1 }}>
               <label className="form-label">Category</label>
               <select className="form-input" value={current.category} onChange={e => updateCurrent("category", e.target.value)}>
                 {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
               </select>
             </div>
             <div style={{ flex: 1 }}>
               <label className="form-label">Stock</label>
               <input type="number" className="form-input" value={current.stock} onChange={e => updateCurrent("stock", e.target.value)} />
             </div>
           </div>
           
           <div style={{ display: 'flex', gap: 12, marginTop: 'auto', paddingTop: 16 }}>
             <button onClick={handleRemoveCurrent} disabled={saving} style={{ padding: '12px', borderRadius: '12px', background: '#f1f5f9', color: '#475569', fontWeight: 700, border: 'none', cursor: 'pointer', flex: 1 }}>Skip/Remove</button>
             <button onClick={handleSaveNext} disabled={saving} style={{ padding: '12px', borderRadius: '12px', background: 'var(--primary)', color: '#fff', fontWeight: 700, border: 'none', cursor: 'pointer', flex: 2 }}>{saving ? "Saving..." : currentIndex === queue.length - 1 ? "Save & Finish" : "Save & Next"}</button>
           </div>
        </div>
      </div>
    </div>
  );
}

function AdminDashboard"""

js = js.replace("function AdminDashboard", bulk_upload_comp)


sidebar_tab = """<li>
            <button onClick={() => { setActiveTab("bulk"); setShowForm(false); }} className={activeTab === "bulk" && !showForm ? "active" : ""} id="tab-bulk">
              ?? Bulk Upload
            </button>
          </li>
          <li>
            <button onClick={() => { setActiveTab("bill");"""

js = js.replace("""<li>
            <button onClick={() => { setActiveTab("bill");""", sidebar_tab)
            
mobile_tab = """<button onClick={() => { setActiveTab("bulk"); setShowForm(false); }} className={activeTab === "bulk" && !showForm ? "active" : ""}>
          <div style={{ fontSize: '20px', marginBottom: '4px' }}>??</div>
          <span>Bulk</span>
        </button>
        <button onClick={() => { setActiveTab("bill");"""
        
js = js.replace("""<button onClick={() => { setActiveTab("bill");""", mobile_tab)

render_logic = """) : activeTab === "bulk" && !showForm ? (
          <BulkUploadForm onSave={handleFormSave} showToast={showToast} />
        ) : activeTab === "bill" && !showForm ? ("""
        
js = js.replace(") : activeTab === \"bill\" && !showForm ? (", render_logic)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Bulk upload feature injected!")
