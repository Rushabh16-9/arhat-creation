"use client";
import { removeBackground as imglyRemoveBackground } from '@imgly/background-removal';

import { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";

const CATEGORIES = ["Skincare", "Haircare", "Makeup", "Fragrance", "Wellness", "Accessories", "Clothing", "Electronics", "Food", "Other"];

function Toast({ message, type, show }) {
  return <div className={`toast ${type} ${show ? "show" : ""}`} role="alert">{message}</div>;
}

function StatsBar({ products }) {
  const total = products.length;
  const inStock = products.filter(p => p.stock > 0).length;
  const outOfStock = products.filter(p => p.stock === 0).length;
  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-label">Total Products</div>
        <div className="stat-value cyan">{total}</div>
      </div>
      <div className="stat-card">
        <div className="stat-label">In Stock</div>
        <div className="stat-value green">{inStock}</div>
      </div>
      <div className="stat-card">
        <div className="stat-label">Out of Stock</div>
        <div className="stat-value" style={{ color: "#e5202f" }}>{outOfStock}</div>
      </div>
    </div>
  );
}

// ===== AI ANALYSER =====
function AIAnalyser({ products }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function runAnalysis() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const saved = localStorage.getItem('arhat_pos_bills');
      const bills = saved ? JSON.parse(saved) : [];
      const res = await fetch('/api/gemini', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'analyzeInventory',
          products: products.map(p => ({ id: p.id, name: p.name, price: p.price, stock: p.stock, category: p.category })),
          bills
        })
      });
      const data = await res.json();
      if (!data.success) throw new Error(data.error || 'Analysis failed');
      setResult(data.data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const urgencyColor = (u) => u === 'high' ? '#e5202f' : u === 'medium' ? '#f59e0b' : '#10b981';
  const urgencyBg = (u) => u === 'high' ? '#fef2f2' : u === 'medium' ? '#fffbeb' : '#f0fdf4';

  return (
    <div style={{ padding: '0 0 40px 0' }}>
      {/* Header */}
      <div style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', borderRadius: 20, padding: '28px 32px', marginBottom: 28, color: '#fff', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', top: -30, right: -30, width: 120, height: 120, background: 'rgba(255,255,255,0.08)', borderRadius: '50%' }} />
        <div style={{ position: 'absolute', bottom: -20, right: 60, width: 80, height: 80, background: 'rgba(255,255,255,0.05)', borderRadius: '50%' }} />
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 12 }}>
          <span style={{ fontSize: 32 }}>🤖</span>
          <div>
            <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, letterSpacing: '-0.02em' }}>AI Inventory Analyser</h2>
            <p style={{ margin: 0, fontSize: 13, opacity: 0.85 }}>Powered by Gemini AI • Analyzes sales & stock to guide decisions</p>
          </div>
        </div>
        <button
          onClick={runAnalysis}
          disabled={loading}
          style={{
            background: '#fff', color: '#764ba2', border: 'none', borderRadius: 12,
            padding: '12px 28px', fontWeight: 800, fontSize: 14, cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.7 : 1, transition: 'all 0.2s', display: 'inline-flex', alignItems: 'center', gap: 8
          }}
        >
          {loading ? (
            <><span style={{ display: 'inline-block', width: 14, height: 14, border: '2px solid #764ba2', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />Analysing...</>
          ) : '✨ Run Analysis'}
        </button>
      </div>

      {error && (
        <div style={{ background: '#fef2f2', border: '1px solid #fee2e2', borderRadius: 12, padding: '16px 20px', color: '#dc2626', marginBottom: 20, fontSize: 14 }}>
          ⚠️ {error}
        </div>
      )}

      {!result && !loading && (
        <div style={{ textAlign: 'center', padding: '48px 20px', color: 'var(--text-muted)' }}>
          <div style={{ fontSize: 52, marginBottom: 16 }}>📊</div>
          <p style={{ fontSize: 16, fontWeight: 600, marginBottom: 8 }}>No analysis yet</p>
          <p style={{ fontSize: 13 }}>Click "Run Analysis" to get AI-powered restocking & pricing recommendations based on your sales history.</p>
        </div>
      )}

      {result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
          {/* Summary */}
          <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 16, padding: '20px 24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
              <span style={{ fontSize: 20 }}>📋</span>
              <h3 style={{ margin: 0, fontSize: 16, fontWeight: 700 }}>Executive Summary</h3>
            </div>
            <p style={{ margin: 0, color: 'var(--text)', fontSize: 14, lineHeight: 1.7 }}>{result.summary}</p>
          </div>

          {/* Restock */}
          {result.restock?.length > 0 && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
                <span style={{ fontSize: 20 }}>🔺</span>
                <h3 style={{ margin: 0, fontSize: 16, fontWeight: 700, color: '#e5202f' }}>Restock These Products</h3>
                <span style={{ background: '#fef2f2', color: '#e5202f', fontSize: 11, fontWeight: 700, padding: '2px 8px', borderRadius: 20 }}>{result.restock.length} items</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                {result.restock.map((item, i) => (
                  <div key={i} style={{ background: 'var(--surface)', border: `1px solid ${urgencyColor(item.urgency)}33`, borderLeft: `4px solid ${urgencyColor(item.urgency)}`, borderRadius: 14, padding: '16px 20px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 8, marginBottom: 10 }}>
                      <div>
                        <div style={{ fontWeight: 700, fontSize: 15, color: 'var(--primary)', marginBottom: 2 }}>{item.productName}</div>
                        <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{item.reason}</div>
                      </div>
                      <span style={{ background: urgencyBg(item.urgency), color: urgencyColor(item.urgency), fontSize: 11, fontWeight: 700, padding: '3px 10px', borderRadius: 20, textTransform: 'uppercase', whiteSpace: 'nowrap' }}>
                        {item.urgency} urgency
                      </span>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 8 }}>
                      <div style={{ background: 'var(--bg2)', borderRadius: 10, padding: '10px 12px', textAlign: 'center' }}>
                        <div style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', marginBottom: 4 }}>Current Stock</div>
                        <div style={{ fontWeight: 800, fontSize: 18, color: 'var(--primary)' }}>{item.currentStock}</div>
                      </div>
                      <div style={{ background: '#f0fdf4', borderRadius: 10, padding: '10px 12px', textAlign: 'center' }}>
                        <div style={{ fontSize: 10, color: '#10b981', fontWeight: 600, textTransform: 'uppercase', marginBottom: 4 }}>Target Stock</div>
                        <div style={{ fontWeight: 800, fontSize: 18, color: '#10b981' }}>{item.recommendedStock}</div>
                      </div>
                      <div style={{ background: 'var(--bg2)', borderRadius: 10, padding: '10px 12px', textAlign: 'center' }}>
                        <div style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', marginBottom: 4 }}>Current Price</div>
                        <div style={{ fontWeight: 800, fontSize: 16, color: 'var(--primary)' }}>₹{item.currentPrice}</div>
                      </div>
                      <div style={{ background: '#f0fdf4', borderRadius: 10, padding: '10px 12px', textAlign: 'center' }}>
                        <div style={{ fontSize: 10, color: '#10b981', fontWeight: 600, textTransform: 'uppercase', marginBottom: 4 }}>Suggested Price</div>
                        <div style={{ fontWeight: 800, fontSize: 16, color: '#10b981' }}>₹{item.recommendedPrice}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Reduce / Slow movers */}
          {result.reduce?.length > 0 && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
                <span style={{ fontSize: 20 }}>🔻</span>
                <h3 style={{ margin: 0, fontSize: 16, fontWeight: 700, color: '#f59e0b' }}>Reduce Stock / Drop Price</h3>
                <span style={{ background: '#fffbeb', color: '#f59e0b', fontSize: 11, fontWeight: 700, padding: '2px 8px', borderRadius: 20 }}>{result.reduce.length} items</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                {result.reduce.map((item, i) => (
                  <div key={i} style={{ background: 'var(--surface)', border: '1px solid #f59e0b33', borderLeft: '4px solid #f59e0b', borderRadius: 14, padding: '16px 20px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 8, marginBottom: 10 }}>
                      <div>
                        <div style={{ fontWeight: 700, fontSize: 15, color: 'var(--primary)', marginBottom: 2 }}>{item.productName}</div>
                        <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{item.reason}</div>
                      </div>
                      <span style={{ background: '#fffbeb', color: '#f59e0b', fontSize: 11, fontWeight: 700, padding: '3px 10px', borderRadius: 20, textTransform: 'uppercase', whiteSpace: 'nowrap' }}>slow mover</span>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 8 }}>
                      <div style={{ background: 'var(--bg2)', borderRadius: 10, padding: '10px 12px', textAlign: 'center' }}>
                        <div style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', marginBottom: 4 }}>Current Stock</div>
                        <div style={{ fontWeight: 800, fontSize: 18, color: 'var(--primary)' }}>{item.currentStock}</div>
                      </div>
                      <div style={{ background: '#fffbeb', borderRadius: 10, padding: '10px 12px', textAlign: 'center' }}>
                        <div style={{ fontSize: 10, color: '#f59e0b', fontWeight: 600, textTransform: 'uppercase', marginBottom: 4 }}>Target Stock</div>
                        <div style={{ fontWeight: 800, fontSize: 18, color: '#f59e0b' }}>{item.recommendedStock}</div>
                      </div>
                      <div style={{ background: 'var(--bg2)', borderRadius: 10, padding: '10px 12px', textAlign: 'center' }}>
                        <div style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', marginBottom: 4 }}>Current Price</div>
                        <div style={{ fontWeight: 800, fontSize: 16, color: 'var(--primary)' }}>₹{item.currentPrice}</div>
                      </div>
                      <div style={{ background: '#fffbeb', borderRadius: 10, padding: '10px 12px', textAlign: 'center' }}>
                        <div style={{ fontSize: 10, color: '#f59e0b', fontWeight: 600, textTransform: 'uppercase', marginBottom: 4 }}>Suggested Price</div>
                        <div style={{ fontWeight: 800, fontSize: 16, color: '#f59e0b' }}>₹{item.recommendedPrice}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Out of stock alerts */}
          {result.outOfStockAlert?.length > 0 && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
                <span style={{ fontSize: 20 }}>🚨</span>
                <h3 style={{ margin: 0, fontSize: 16, fontWeight: 700, color: '#dc2626' }}>Out of Stock — Missed Revenue</h3>
                <span style={{ background: '#fef2f2', color: '#dc2626', fontSize: 11, fontWeight: 700, padding: '2px 8px', borderRadius: 20 }}>{result.outOfStockAlert.length} alerts</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {result.outOfStockAlert.map((item, i) => (
                  <div key={i} style={{ background: '#fef2f2', border: '1px solid #fee2e2', borderRadius: 12, padding: '14px 18px', display: 'flex', alignItems: 'center', gap: 16 }}>
                    <span style={{ fontSize: 24 }}>📦</span>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 700, color: '#dc2626', marginBottom: 2 }}>{item.productName}</div>
                      <div style={{ fontSize: 13, color: '#7f1d1d' }}>{item.reason} — ordered {item.orderedCount} times</div>
                    </div>
                    <div style={{ background: '#dc2626', color: '#fff', borderRadius: 10, padding: '6px 14px', fontWeight: 700, fontSize: 13, whiteSpace: 'nowrap' }}>Restock Now</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.restock?.length === 0 && result.reduce?.length === 0 && result.outOfStockAlert?.length === 0 && (
            <div style={{ textAlign: 'center', padding: '32px', background: '#f0fdf4', borderRadius: 16, border: '1px solid #bbf7d0' }}>
              <div style={{ fontSize: 36, marginBottom: 10 }}>✅</div>
              <div style={{ fontWeight: 700, color: '#10b981', fontSize: 16 }}>Inventory looks healthy!</div>
              <div style={{ color: '#065f46', fontSize: 13, marginTop: 4 }}>No immediate action required based on current data.</div>
            </div>
          )}
        </div>
      )}
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}

// ===== PRODUCT FORM =====
function ProductForm({ editProduct, onSave, onCancel, showToast }) {
  const [name, setName] = useState(editProduct?.name || "");
  const [description, setDescription] = useState(editProduct?.description || "");
  const [price, setPrice] = useState(editProduct?.price || "");
  const [originalPrice, setOriginalPrice] = useState(editProduct?.original_price || "");
  const [stock, setStock] = useState(editProduct?.stock ?? "");
  const [category, setCategory] = useState(editProduct?.category || "");
  const [imageUrl, setImageUrl] = useState(editProduct?.image_url || "");
  const [enhancedImageUrl, setEnhancedImageUrl] = useState(editProduct?.enhanced_image_url || "");
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(editProduct?.enhanced_image_url || editProduct?.image_url || "");
  const [saving, setSaving] = useState(false);
  const [geminiLoading, setGeminiLoading] = useState(false);
  const [geminiAction, setGeminiAction] = useState("");
  const [bgColor, setBgColor] = useState("#0d1117");
  const [cssFilter, setCssFilter] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  function handleFileChange(file) {
    if (!file) return;
    setImageFile(file);
    const reader = new FileReader();
    reader.onload = e => setImagePreview(e.target.result);
    reader.readAsDataURL(file);
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

  function getBase64FromPreview(preview) {
    if (!preview || preview.startsWith("http")) return null;
    return preview.split(",")[1];
  }

  async function runGeminiEnhance() {
    const base64 = getBase64FromPreview(imagePreview);
    if (!base64 && !imageUrl) {
      showToast("Please upload an image first", "error");
      return;
    }
    setGeminiLoading(true);
    setGeminiAction("enhance");
    try {
      let b64 = base64;
      let mime = imageFile?.type || "image/jpeg";
      if (!b64 && imageUrl) {
        // Fetch from URL
        const resp = await fetch(`/api/gemini`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ action: "enhance", imageBase64: "placeholder", mimeType: mime, productName: name })
        });
        const d = await resp.json();
        if (d.error && d.error.includes("not configured")) {
          showToast("Add GEMINI_API_KEY to .env.local to use AI features", "info");
          return;
        }
      }
      const res = await fetch("/api/gemini", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "enhance", imageBase64: b64 || "", mimeType: mime, productName: name })
      });
      const data = await res.json();
      if (data.error) {
        showToast(data.error, "error");
        return;
      }
      if (data.data) {
        const d = data.data;
        if (d.suggestedName && !name) setName(d.suggestedName);
        if (d.description) setDescription(d.description);
        if (d.category) setCategory(d.category);
        showToast("✨ Gemini AI enhanced product details!", "success");
      }
    } catch (err) {
      showToast("Gemini enhance failed: " + err.message, "error");
    } finally {
      setGeminiLoading(false);
      setGeminiAction("");
    }
  }
  async function runGeminiRemoveBg() {
    if (!imagePreview) {
      showToast("Please upload an image first", "error");
      return;
    }
    setGeminiLoading(true);
    setGeminiAction("removeBg");
    try {
      showToast("Processing AI... This may take a few seconds", "info");
      
      const base64 = getBase64FromPreview(imagePreview);
      const mime = imageFile?.type || "image/jpeg";
      
      const geminiPromise = fetch("/api/gemini", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "removeBackground", imageBase64: base64 || "", mimeType: mime })
      }).then(r => r.json());

      const removeBgPromise = imglyRemoveBackground(imagePreview, {
        output: { format: 'image/png' }
      });

      const [geminiData, blob] = await Promise.all([geminiPromise, removeBgPromise]);
      
      const newUrl = URL.createObjectURL(blob);
      setImagePreview(newUrl);
      
      const newFile = new File([blob], 'transparent-image.png', { type: 'image/png' });
      setImageFile(newFile);

      if (geminiData.data?.recommendedBg) {
        setBgColor(geminiData.data.recommendedBg);
        showToast("True Background Removed & AI color applied!", "success");
      } else {
        showToast("Background successfully removed!", "success");
      }
    } catch (err) {
      console.error(err);
      showToast("Failed to remove background: " + err.message, "error");
    } finally {
      setGeminiLoading(false);
      setGeminiAction("");
    }
  }



  async function handleSave() {
    if (!name || !price) {
      showToast("Product name and price are required", "error");
      return;
    }
    setSaving(true);
    try {
      let finalImageUrl = imageUrl;
      let finalEnhancedUrl = enhancedImageUrl;

      // Upload image if file selected
      if (imageFile) {
        showToast("Uploading image...", "info");
        try {
          finalImageUrl = await uploadImage(imageFile);
          finalEnhancedUrl = finalImageUrl; // same for now
        } catch (err) {
          showToast("Image upload failed (Supabase not configured) — product saved without image", "info");
        }
      }

      const payload = { name, description, price, original_price: originalPrice || null, stock: stock || 0, category, image_url: finalImageUrl, enhanced_image_url: finalEnhancedUrl };
      const method = editProduct ? "PUT" : "POST";
      const body = editProduct ? { ...payload, id: editProduct.id } : payload;

      const res = await fetch("/api/products", {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (!res.ok) {
        if (data.error?.includes("not configured")) {
          showToast("Supabase not configured. Add credentials to .env.local", "error");
        } else {
          throw new Error(data.error);
        }
        return;
      }
      showToast(editProduct ? "Product updated!" : "Product added!", "success");
      onSave(data.product);
    } catch (err) {
      showToast("Save failed: " + err.message, "error");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="upload-section">
      <div className="upload-section-title">
        <span style={{ fontSize: 20 }}>{editProduct ? "✏️" : "➕"}</span>
        {editProduct ? "Edit Product" : "Add New Product"}
      </div>

      <div className="add-product-grid">
        {/* Image Upload Column */}
        <div className="add-product-img-col">
          {imagePreview ? (
            <div style={{ position: "relative" }}>
              <div className="upload-preview" style={{ background: bgColor }}>
                <img src={imagePreview} alt="Preview" style={{ width: "100%", height: "100%", objectFit: "cover", filter: cssFilter, transition: "filter 0.5s ease" }} />
                <div className="upload-preview-tag enhanced">{cssFilter ? "AI Enhanced" : "Preview"}</div>
              </div>
              <button
                onClick={() => { setImagePreview(""); setImageFile(null); setImageUrl(""); setCssFilter(""); }}
                style={{ width: "100%", marginTop: 8, padding: "6px", borderRadius: 8, background: "rgba(229,32,47,.1)", border: "1px solid rgba(229,32,47,.2)", color: "#e5202f", fontSize: 12, cursor: "pointer" }}>
                Remove Image
              </button>
            </div>
          ) : (
            <div
              className={`upload-area ${dragOver ? "drag-over" : ""}`}
              style={{ minHeight: 180 }}
              onDragOver={e => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onDrop={e => { e.preventDefault(); setDragOver(false); handleFileChange(e.dataTransfer.files[0]); }}
              onClick={() => fileInputRef.current?.click()}
            >
              <input type="file" ref={fileInputRef} accept="image/*" onChange={e => handleFileChange(e.target.files[0])} style={{ display: "none" }} id="image-file-input" />
              <div className="upload-icon">📸</div>
              <div className="upload-text"><strong>Click or drag</strong><br />to upload image</div>
            </div>
          )}

          {/* OR use URL */}
          <div style={{ marginTop: 8 }}>
            <input
              type="url"
              className="form-input"
              placeholder="Or paste image URL..."
              value={imageUrl}
              onChange={e => { setImageUrl(e.target.value); setImagePreview(e.target.value); }}
              style={{ fontSize: 11 }}
              id="image-url-input"
            />
          </div>

          {/* Gemini Actions */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, marginTop: 12 }}>
            <button
              className="gemini-btn"
              onClick={runGeminiRemoveBg}
              disabled={geminiLoading || !imagePreview}
              id="gemini-bg-btn"
              style={{ fontSize: 11, padding: "8px 12px" }}
            >
              {geminiLoading && geminiAction === "removeBg" ? <span className="gemini-spinner" /> : "🎨"}
              AI Remove BG & Color
            </button>
            <button
              className="gemini-btn"
              onClick={runGeminiEnhance}
              disabled={geminiLoading || !imagePreview}
              id="gemini-enhance-btn"
              style={{ fontSize: 11, padding: "8px 12px" }}
            >
              {geminiLoading && geminiAction === "enhance" ? <span className="gemini-spinner" /> : "✨"}
              AI Enhance Details
            </button>
          </div>

          {bgColor && bgColor !== "#0d1117" && (
            <div style={{ marginTop: 8, display: "flex", alignItems: "center", gap: 8, fontSize: 11, color: "var(--text-muted)" }}>
              <div style={{ width: 16, height: 16, borderRadius: 4, background: bgColor, border: "1px solid rgba(255,255,255,.2)" }} />
              <span>BG: {bgColor}</span>
            </div>
          )}
        </div>

        {/* Form Fields */}
        <div className="form-grid">
          <div className="form-field full">
            <label className="form-label" htmlFor="product-name">Product Name *</label>
            <input id="product-name" type="text" className="form-input" placeholder="e.g. Vitamin C Serum" value={name} onChange={e => setName(e.target.value)} required />
          </div>
          <div className="form-field full">
            <label className="form-label" htmlFor="product-desc">Description</label>
            <textarea id="product-desc" className="form-textarea" placeholder="Describe the product..." value={description} onChange={e => setDescription(e.target.value)} />
          </div>
          <div className="form-field">
            <label className="form-label" htmlFor="product-price">Price (₹) *</label>
            <input id="product-price" type="number" className="form-input" placeholder="999" value={price} onChange={e => setPrice(e.target.value)} min="0" step="0.01" required />
          </div>
          <div className="form-field">
            <label className="form-label" htmlFor="product-orig-price">Original Price (₹)</label>
            <input id="product-orig-price" type="number" className="form-input" placeholder="1299 (optional)" value={originalPrice} onChange={e => setOriginalPrice(e.target.value)} min="0" step="0.01" />
          </div>
          <div className="form-field">
            <label className="form-label" htmlFor="product-stock">Stock Quantity *</label>
            <input id="product-stock" type="number" className="form-input" placeholder="0" value={stock} onChange={e => setStock(e.target.value)} min="0" required />
          </div>
          <div className="form-field">
            <label className="form-label" htmlFor="product-category">Category</label>
            <select id="product-category" className="form-select" value={category} onChange={e => setCategory(e.target.value)}>
              <option value="">Select category...</option>
              {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div className="form-actions" style={{ gridColumn: "1/-1" }}>
            <button className="glow-btn save-btn" onClick={handleSave} disabled={saving} id="save-product-btn">
              <span>{saving ? "Saving..." : editProduct ? "Update Product" : "Add Product"}</span>
            </button>
            <button className="cancel-btn" onClick={onCancel} id="cancel-product-btn">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  );
}



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
            <h1>Arhat Creation</h1>
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
                  <td style="text-align:right">₹${item.product.price}</td>
                  <td style="text-align:right">₹${item.product.price * item.qty}</td>
                </tr>
              `).join('')}
              <tr class="total-row">
                <td colspan="3" style="text-align:right; padding-right:20px;">Grand Total:</td>
                <td style="text-align:right; color:#10b981;">₹${bill.total.toLocaleString('en-IN')}</td>
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
      <div style={{ background: 'var(--surface)', borderRadius: '16px', padding: '32px', border: '1px solid var(--border)', boxShadow: '0 4px 12px rgba(0,0,0,0.02)', boxSizing: 'border-box', width: '100%' }}>
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
                    <div style={{ fontSize: '18px', fontWeight: '800', color: 'var(--primary)' }}>₹{bill.total.toLocaleString('en-IN')}</div>
                    <button onClick={() => handlePrint(bill)} style={{ padding: '6px 12px', background: '#10b981', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', fontSize: '13px' }}>Print PDF</button>
                  </div>
                </div>
                <div>
                  {bill.items.map((item, i) => (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '8px' }}>
                      <span style={{ color: 'var(--text-muted)' }}>{item.qty}x {item.product.name}</span>
                      <span style={{ fontWeight: '600' }}>₹{(item.product.price * item.qty).toLocaleString('en-IN')}</span>
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
    <div style={{ background: 'var(--surface)', borderRadius: '16px', padding: '32px', border: '1px solid var(--border)', boxShadow: '0 4px 12px rgba(0,0,0,0.02)', boxSizing: 'border-box', width: '100%' }}>
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
                    <option key={p.id} value={p.id}>{p.name} (₹{p.price}) - {p.stock} in stock</option>
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
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>₹{item.product.price} x {item.qty}</div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                        <div style={{ fontWeight: '700' }}>₹{(item.product.price * item.qty).toLocaleString('en-IN')}</div>
                        <button onClick={() => removeFromCart(item.product.id)} style={{ background: 'none', border: 'none', color: 'var(--red)', cursor: 'pointer', fontSize: '18px' }}>✕</button>
                      </div>
                    </div>
                  ))}
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '12px', marginTop: '12px' }}>
                    <div style={{ fontSize: '18px', fontWeight: '600' }}>Total</div>
                    <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--primary)' }}>₹{total.toLocaleString('en-IN')}</div>
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


// ===== ADMIN PAGE =====

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
        <label className="glow-btn" style={{ cursor: 'pointer', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', height: '48px', padding: '0 32px', borderRadius: '14px', fontSize: '15px' }}>
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
      
      <div className="add-product-grid" style={{ padding: 24 }}>
        {/* Left Side: Image Viewer */}
        <div className="add-product-img-col" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
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
                 <span style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', fontWeight: 600, color: 'var(--text-muted)' }}>{"\u20B9"}</span>
                 <input type="number" className="form-input" style={{ fontSize: 16, padding: '14px 18px 14px 32px', background: '#fff', border: '2px solid transparent', boxShadow: '0 2px 10px rgba(0,0,0,0.02)', width: '100%', boxSizing: 'border-box' }} value={current.price} onChange={e => updateCurrent("price", e.target.value)} onFocus={e => e.target.style.borderColor = 'var(--primary)'} onBlur={e => e.target.style.borderColor = 'transparent'} />
               </div>
             </div>
             <div className="form-field">
               <label className="form-label" style={{ fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Original Price</label>
               <div style={{ position: 'relative' }}>
                 <span style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', fontWeight: 600, color: 'var(--text-muted)' }}>{"\u20B9"}</span>
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
                {saving ? "Saving..." : currentIndex === queue.length - 1 ? "\u2728 Save & Finish" : "Next Image \u2794"}
             </button>
           </div>
        </div>
      </div>
    </div>
  );
}

export default function AdminPanel() {
  const router = useRouter();
  const [authed, setAuthed] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editProduct, setEditProduct] = useState(null);
  const [toast, setToast] = useState({ show: false, message: "", type: "info" });
  const [activeTab, setActiveTab] = useState("products");
  const [isMock, setIsMock] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => { checkAuth(); }, []);
  useEffect(() => { if (authed) loadProducts(); }, [authed]);

  async function checkAuth() {
    try {
      const res = await fetch("/api/auth");
      if (res.ok) {
        setAuthed(true);
      } else {
        router.push("/admin/login");
      }
    } catch {
      router.push("/admin/login");
    }
  }

  async function loadProducts() {
    setLoading(true);
    try {
      const res = await fetch("/api/products");
      const data = await res.json();
      setProducts(data.products || []);
      setIsMock(data.isMock || false);
    } catch (err) {
      showToast("Failed to load products", "error");
    } finally {
      setLoading(false);
    }
  }

  function showToast(message, type = "info", duration = 4000) {
    setToast({ show: true, message, type });
    setTimeout(() => setToast(t => ({ ...t, show: false })), duration);
  }

  async function handleDelete(id) {
    if (!confirm("Delete this product? This cannot be undone.")) return;
    try {
      const res = await fetch(`/api/products?id=${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Delete failed");
      setProducts(ps => ps.filter(p => p.id !== id));
      showToast("Product deleted", "success");
    } catch (err) {
      showToast("Delete failed: " + err.message, "error");
    }
  }

  async function handleStockUpdate(id, newStock) {
    try {
      const res = await fetch("/api/products", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, stock: parseInt(newStock) })
      });
      if (!res.ok) throw new Error("Update failed");
      setProducts(ps => ps.map(p => p.id === id ? { ...p, stock: parseInt(newStock) } : p));
      showToast("Stock updated", "success");
    } catch (err) {
      showToast("Stock update failed: " + err.message, "error");
    }
  }

  async function handleLogout() {
    await fetch("/api/auth", { method: "DELETE" });
    router.push("/admin/login");
  }

  function handleFormSave(savedProduct) {
    if (editProduct) {
      setProducts(ps => ps.map(p => p.id === savedProduct?.id ? savedProduct : p));
    } else {
      if (savedProduct) setProducts(ps => [savedProduct, ...ps]);
    }
    loadProducts(); // Refresh from server
    setShowForm(false);
    setEditProduct(null);
  }

  if (authed === null) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#020204" }}>
        <div className="loader-ring" />
      </div>
    );
  }

  return (
    <div className="admin-layout">
      {/* Sidebar Overlay for Mobile */}
      <div className={`admin-sidebar-overlay ${menuOpen ? 'open' : ''}`} onClick={() => setMenuOpen(false)} />

      {/* Sidebar */}
      <aside className={`admin-sidebar ${menuOpen ? 'open' : ''}`}>
        <div className="sidebar-logo">
          Arhat Creation
          <span>Admin Panel</span>
        </div>
        <ul className="sidebar-nav">
          <li>
            <button onClick={() => { setActiveTab("products"); setShowForm(false); setMenuOpen(false); }} className={activeTab === "products" && !showForm ? "active" : ""} id="tab-products">
              📦 Products
            </button>
          </li>
          <li>
            <button onClick={() => { setActiveTab("bulk"); setShowForm(false); setMenuOpen(false); }} className={activeTab === "bulk" && !showForm ? "active" : ""} id="tab-bulk">
              {"\uD83D\uDCE5"} Bulk Upload
            </button>
          </li>
          <li>
            <button onClick={() => { setActiveTab("ai"); setShowForm(false); setMenuOpen(false); }} className={activeTab === "ai" && !showForm ? "active" : ""} id="tab-ai-analyser">
              🤖 AI Analyser
            </button>
          </li>
          <li>
        <button onClick={() => { setActiveTab("bill"); setShowForm(false); setMenuOpen(false); }} className={activeTab === "bill" ? "active" : ""} id="tab-billing">
              🧾 Billing (POS)
            </button>
          </li>
          <li>
            <a href="/" target="_blank" rel="noopener noreferrer" id="view-store-link">
              🏪 View Store
            </a>
          </li>
          <li style={{ marginTop: "auto" }}>
            <button onClick={() => { handleLogout(); setMenuOpen(false); }} id="logout-btn" style={{ color: "#e5202f" }}>
              🚪 Logout
            </button>
          </li>
        </ul>
      </aside>


      {/* Main Content Area */}
      <main className="admin-main">
        <div className="admin-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <button 
              onClick={() => setMenuOpen(true)} 
              style={{ background: 'none', border: 'none', padding: '0', cursor: 'pointer' }}
              className="admin-mobile-menu-btn"
            >
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="3" y1="12" x2="21" y2="12"></line>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <line x1="3" y1="18" x2="21" y2="18"></line>
              </svg>
            </button>
            <div>
              <h1 className="admin-title">
                {activeTab === "products" ? "Product Management" : activeTab === "bill" ? "Billing (POS)" : activeTab === "ai" ? "AI Analyser" : activeTab === "bulk" ? "Bulk Upload" : "Dashboard"}
              </h1>
              <p className="admin-subtitle">
                {isMock
                  ? "⚠️ Demo mode — Configure Supabase to save real data"
                  : `${products.length} products in database`}
              </p>
            </div>
          </div>
        </div>

        {isMock && (
          <div style={{ padding: "14px 18px", borderRadius: 12, background: "rgba(0,212,255,.06)", border: "1px solid rgba(0,212,255,.15)", marginBottom: 24, fontSize: 13, color: "rgba(255,255,255,.8)", lineHeight: 1.6 }}>
            <strong style={{ color: "var(--accent2)" }}>🔧 Setup Required:</strong> To save products, set these in <code style={{ background: "rgba(255,255,255,.08)", padding: "1px 6px", borderRadius: 4 }}>.env.local</code>:<br />
            <code>NEXT_PUBLIC_SUPABASE_URL</code> · <code>NEXT_PUBLIC_SUPABASE_ANON_KEY</code> · <code>SUPABASE_SERVICE_ROLE_KEY</code> · <code>GEMINI_API_KEY</code>
          </div>
        )}

        {activeTab === "products" && !showForm && (
          <StatsBar products={products} />
        )}

        {showForm && (
          <ProductForm
            editProduct={editProduct}
            onSave={handleFormSave}
            onCancel={() => { setShowForm(false); setEditProduct(null); }}
            showToast={showToast}
          />
        )}

        {/* Main Content */}
        {loading ? (
          <div className="page-loader">
            <div className="loader-ring" />
            <p className="loader-text">Loading products...</p>
          </div>
        ) : activeTab === "ai" && !showForm ? (
          <AIAnalyser products={products} />
        ) : activeTab === "bulk" && !showForm ? (
          <BulkUploadForm onSave={handleFormSave} showToast={showToast} />
        ) : activeTab === "bill" && !showForm ? (
          <BillingSystem 
            products={products} 
            onUpdateStock={(updatedProduct) => {
              setProducts(prev => prev.map(p => p.id === updatedProduct.id ? updatedProduct : p));
            }}
            showToast={showToast}
          />
        ) : activeTab === "products" && !showForm ? (
          <div className="admin-table-wrap">
            <table className="admin-table" id="products-table">
              <thead>
                <tr>
                  <th>Image</th>
                  <th>Product</th>
                  <th>Category</th>
                  <th>Price</th>
                  <th>Stock</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {products.length === 0 ? (
                  <tr>
                    <td colSpan={6} style={{ textAlign: "center", padding: "48px", color: "var(--text-muted)", fontSize: 14 }}>
                      No products yet. Use Bulk Upload to add products.
                    </td>
                  </tr>
                ) : (
                  products.map(product => (
                    <tr key={product.id} id={`admin-row-${product.id}`}>
                      <td>
                        {(product.enhanced_image_url || product.image_url) ? (
                          <img
                            className="table-img"
                            src={product.enhanced_image_url || product.image_url}
                            alt={product.name}
                          />
                        ) : (
                          <div className="table-img-placeholder">🛍</div>
                        )}
                      </td>
                      <td>
                        <div style={{ fontWeight: 600, color: 'var(--primary)', marginBottom: 3 }}>{product.name}</div>
                        {product.description && (
                          <div style={{ fontSize: 11, color: "var(--text-muted)", maxWidth: 220, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                            {product.description}
                          </div>
                        )}
                      </td>
                      <td>
                        <span style={{ padding: "3px 10px", borderRadius: 20, background: "rgba(0,212,255,.08)", color: "var(--accent2)", fontSize: 11, fontWeight: 600 }}>
                          {product.category || "—"}
                        </span>
                      </td>
                      <td>
                        <div style={{ fontWeight: 700, color: 'var(--primary)' }}>₹{product.price?.toLocaleString("en-IN")}</div>
                        {product.original_price && (
                          <div style={{ fontSize: 11, color: "rgba(255,255,255,.4)", textDecoration: "line-through" }}>
                            ₹{product.original_price.toLocaleString("en-IN")}
                          </div>
                        )}
                      </td>
                      <td>
                        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                          <input
                            type="number"
                            className="stock-input"
                            value={product.stock}
                            min="0"
                            onChange={e => setProducts(ps => ps.map(p => p.id === product.id ? { ...p, stock: parseInt(e.target.value) || 0 } : p))}
                            onBlur={e => handleStockUpdate(product.id, e.target.value)}
                            id={`stock-input-${product.id}`}
                          />
                          <span style={{
                            fontSize: 10, fontWeight: 600,
                            color: product.stock > 10 ? "#12c02f" : product.stock > 0 ? "#f6b719" : "#e5202f"
                          }}>
                            {product.stock > 10 ? "●" : product.stock > 0 ? "◐" : "○"}
                          </span>
                        </div>
                      </td>
                      <td>
                        <div className="table-actions">
                          <button
                            className="action-btn edit"
                            onClick={() => { setEditProduct(product); setShowForm(true); setActiveTab("products"); }}
                            id={`edit-${product.id}`}
                          >
                            Edit
                          </button>
                          <button
                            className="action-btn delete"
                            onClick={() => handleDelete(product.id)}
                            id={`delete-${product.id}`}
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        ) : null}
      </main>

      <Toast {...toast} />
    </div>
  );
}
