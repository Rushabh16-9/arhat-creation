import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the inner layout of BulkUploadForm to make it look premium
old_layout = """<div className="form-grid" style={{ padding: 24 }}>
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
           <div className="form-field">
             <label className="form-label">Product Name *</label>
             <input type="text" className="form-input" value={current.name} onChange={e => updateCurrent("name", e.target.value)} placeholder="Rose Barfi" />
           </div>
           <div style={{ display: 'flex', gap: 16 }}>
             <div className="form-field" style={{ flex: 1 }}>
               <label className="form-label">Price *</label>
               <input type="number" className="form-input" value={current.price} onChange={e => updateCurrent("price", e.target.value)} />
             </div>
             <div className="form-field" style={{ flex: 1 }}>
               <label className="form-label">Original Price</label>
               <input type="number" className="form-input" value={current.original_price} onChange={e => updateCurrent("original_price", e.target.value)} />
             </div>
           </div>
           <div style={{ display: 'flex', gap: 16 }}>
             <div className="form-field" style={{ flex: 1 }}>
               <label className="form-label">Category</label>
               <select className="form-input" value={current.category} onChange={e => updateCurrent("category", e.target.value)}>
                 {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
               </select>
             </div>
             <div className="form-field" style={{ flex: 1 }}>
               <label className="form-label">Stock</label>
               <input type="number" className="form-input" value={current.stock} onChange={e => updateCurrent("stock", e.target.value)} />
             </div>
           </div>
           
           <div style={{ display: 'flex', gap: 12, marginTop: 'auto', paddingTop: 16 }}>
             <button onClick={handleRemoveCurrent} disabled={saving} style={{ padding: '12px', borderRadius: '12px', background: '#f1f5f9', color: '#475569', fontWeight: 700, border: 'none', cursor: 'pointer', flex: 1 }}>Skip/Remove</button>
             <button onClick={handleSaveNext} disabled={saving} style={{ padding: '12px', borderRadius: '12px', background: 'var(--primary)', color: '#fff', fontWeight: 700, border: 'none', cursor: 'pointer', flex: 2 }}>{saving ? "Saving..." : currentIndex === queue.length - 1 ? "Save & Finish" : "Save & Next"}</button>
           </div>
        </div>
      </div>"""

new_layout = """<div style={{ padding: 24, display: 'grid', gridTemplateColumns: 'minmax(250px, 1fr) minmax(300px, 2fr)', gap: 32 }}>
        {/* Left Side: Image Viewer */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
           <div style={{ position: 'relative', width: '100%', aspectRatio: '1', borderRadius: 20, overflow: 'hidden', background: 'var(--bg2)', border: '1px solid var(--border)', boxShadow: '0 8px 30px rgba(0,0,0,0.06)' }}>
             <img src={current.preview} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
           </div>
           <div style={{ display: 'flex', gap: 10, overflowX: 'auto', paddingBottom: 8 }}>
             {queue.map((q, idx) => (
                <div key={q.id} onClick={() => setCurrentIndex(idx)} style={{ flexShrink: 0, width: 56, height: 56, borderRadius: 12, overflow: 'hidden', border: idx === currentIndex ? '3px solid var(--primary)' : '1px solid var(--border)', cursor: 'pointer', opacity: idx === currentIndex ? 1 : 0.4, transition: 'all 0.2s', transform: idx === currentIndex ? 'scale(1.05)' : 'scale(1)' }}>
                  <img src={q.preview} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </div>
             ))}
           </div>
        </div>
        
        {/* Right Side: Inputs */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20, background: 'var(--bg2)', padding: 24, borderRadius: 20, border: '1px solid var(--border)' }}>
           <div className="form-field">
             <label className="form-label" style={{ fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Product Name <span style={{color: 'var(--red)'}}>*</span></label>
             <input type="text" className="form-input" style={{ fontSize: 16, padding: '14px 18px', background: '#fff', border: '2px solid transparent', boxShadow: '0 2px 10px rgba(0,0,0,0.02)' }} value={current.name} onChange={e => updateCurrent("name", e.target.value)} placeholder="e.g. Premium Rose Barfi" onFocus={e => e.target.style.borderColor = 'var(--primary)'} onBlur={e => e.target.style.borderColor = 'transparent'} />
           </div>
           
           <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
             <div className="form-field">
               <label className="form-label" style={{ fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Price <span style={{color: 'var(--red)'}}>*</span></label>
               <div style={{ position: 'relative' }}>
                 <span style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', fontWeight: 600, color: 'var(--text-muted)' }}>?</span>
                 <input type="number" className="form-input" style={{ fontSize: 16, padding: '14px 18px 14px 32px', background: '#fff', border: '2px solid transparent', boxShadow: '0 2px 10px rgba(0,0,0,0.02)', width: '100%', boxSizing: 'border-box' }} value={current.price} onChange={e => updateCurrent("price", e.target.value)} onFocus={e => e.target.style.borderColor = 'var(--primary)'} onBlur={e => e.target.style.borderColor = 'transparent'} />
               </div>
             </div>
             <div className="form-field">
               <label className="form-label" style={{ fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Original Price</label>
               <div style={{ position: 'relative' }}>
                 <span style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', fontWeight: 600, color: 'var(--text-muted)' }}>?</span>
                 <input type="number" className="form-input" style={{ fontSize: 16, padding: '14px 18px 14px 32px', background: '#fff', border: '2px solid transparent', boxShadow: '0 2px 10px rgba(0,0,0,0.02)', width: '100%', boxSizing: 'border-box' }} value={current.original_price} onChange={e => updateCurrent("original_price", e.target.value)} onFocus={e => e.target.style.borderColor = 'var(--primary)'} onBlur={e => e.target.style.borderColor = 'transparent'} />
               </div>
             </div>
           </div>
           
           <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
             <div className="form-field">
               <label className="form-label" style={{ fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Category</label>
               <select className="form-input" style={{ fontSize: 16, padding: '14px 18px', background: '#fff', border: '2px solid transparent', boxShadow: '0 2px 10px rgba(0,0,0,0.02)', cursor: 'pointer' }} value={current.category} onChange={e => updateCurrent("category", e.target.value)} onFocus={e => e.target.style.borderColor = 'var(--primary)'} onBlur={e => e.target.style.borderColor = 'transparent'}>
                 {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
               </select>
             </div>
             <div className="form-field">
               <label className="form-label" style={{ fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Stock</label>
               <input type="number" className="form-input" style={{ fontSize: 16, padding: '14px 18px', background: '#fff', border: '2px solid transparent', boxShadow: '0 2px 10px rgba(0,0,0,0.02)' }} value={current.stock} onChange={e => updateCurrent("stock", e.target.value)} onFocus={e => e.target.style.borderColor = 'var(--primary)'} onBlur={e => e.target.style.borderColor = 'transparent'} />
             </div>
           </div>
           
           <div style={{ display: 'flex', gap: 16, marginTop: 'auto', paddingTop: 16 }}>
             <button onClick={handleRemoveCurrent} disabled={saving} style={{ padding: '16px', borderRadius: '16px', background: '#e2e8f0', color: '#475569', fontSize: 15, fontWeight: 700, border: 'none', cursor: 'pointer', flex: 1, transition: 'all 0.2s' }} onMouseOver={e => e.currentTarget.style.background = '#cbd5e1'} onMouseOut={e => e.currentTarget.style.background = '#e2e8f0'}>Skip / Remove</button>
             <button onClick={handleSaveNext} disabled={saving} style={{ padding: '16px', borderRadius: '16px', background: 'var(--primary)', color: '#fff', fontSize: 15, fontWeight: 800, border: 'none', cursor: 'pointer', flex: 2, boxShadow: '0 8px 24px rgba(0, 150, 255, 0.3)', transition: 'all 0.2s' }} onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = '0 12px 32px rgba(0, 150, 255, 0.4)'; }} onMouseOut={e => { e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 150, 255, 0.3)'; }}>
                {saving ? "Saving..." : currentIndex === queue.length - 1 ? "? Save & Finish" : "Next Image ?"}
             </button>
           </div>
        </div>
      </div>"""

if old_layout in js:
    js = js.replace(old_layout, new_layout)
    with open('app/admin/page.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("New premium layout successfully applied!")
else:
    print("Could not find the old layout string to replace.")

