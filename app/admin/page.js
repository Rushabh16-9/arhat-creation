"use client";
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
  const totalValue = products.reduce((sum, p) => sum + (p.price * p.stock), 0);
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
      <div className="stat-card">
        <div className="stat-label">Inventory Value</div>
        <div className="stat-value yellow">₹{totalValue.toLocaleString("en-IN")}</div>
      </div>
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
    const base64 = getBase64FromPreview(imagePreview);
    if (!base64) {
      showToast("Please upload an image file to analyze background", "error");
      return;
    }
    setGeminiLoading(true);
    setGeminiAction("removeBg");
    try {
      const mime = imageFile?.type || "image/jpeg";
      const res = await fetch("/api/gemini", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "removeBackground", imageBase64: base64, mimeType: mime })
      });
      const data = await res.json();
      if (data.error) {
        showToast(data.error, "error");
        return;
      }
      if (data.data?.recommendedBg) {
        setBgColor(data.data.recommendedBg);
        showToast(`✨ Optimal background color set: ${data.data.recommendedBg}. ${data.data.bgDescription || ""}`, "success");
      }
    } catch (err) {
      showToast("Background analysis failed: " + err.message, "error");
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

      <div style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 28, alignItems: "start" }}>
        {/* Image Upload Column */}
        <div style={{ width: 200 }}>
          {imagePreview ? (
            <div style={{ position: "relative" }}>
              <div className="upload-preview" style={{ background: bgColor }}>
                <img src={imagePreview} alt="Preview" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
                <div className="upload-preview-tag enhanced">Preview</div>
              </div>
              <button
                onClick={() => { setImagePreview(""); setImageFile(null); setImageUrl(""); }}
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
              AI Background Color
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

// ===== ADMIN PAGE =====
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
      {/* Sidebar */}
      <aside className="admin-sidebar">
        <div className="sidebar-logo">
          Arhat Shop
          <span>Admin Panel</span>
        </div>
        <ul className="sidebar-nav">
          <li>
            <button onClick={() => setActiveTab("products")} className={activeTab === "products" ? "active" : ""} id="tab-products">
              📦 Products
            </button>
          </li>
          <li>
            <button onClick={() => { setShowForm(true); setEditProduct(null); setActiveTab("products"); }} id="tab-add-product">
              ➕ Add Product
            </button>
          </li>
          <li>
            <a href="/" target="_blank" rel="noopener noreferrer" id="view-store-link">
              🏪 View Store
            </a>
          </li>
          <li style={{ marginTop: "auto" }}>
            <button onClick={handleLogout} id="logout-btn" style={{ color: "#e5202f" }}>
              🚪 Logout
            </button>
          </li>
        </ul>
      </aside>

      {/* Main */}
      <main className="admin-main">
        <div className="admin-header">
          <div>
            <h1 className="admin-title">
              {activeTab === "products" ? "Product Management" : "Dashboard"}
            </h1>
            <p className="admin-subtitle">
              {isMock
                ? "⚠️ Demo mode — Configure Supabase to save real data"
                : `${products.length} products in database`}
            </p>
          </div>
          {!showForm && (
            <button
              className="glow-btn add-product-btn"
              onClick={() => { setShowForm(true); setEditProduct(null); }}
              id="add-product-header-btn"
            >
              <span>➕ Add Product</span>
            </button>
          )}
        </div>

        {isMock && (
          <div style={{ padding: "14px 18px", borderRadius: 12, background: "rgba(0,212,255,.06)", border: "1px solid rgba(0,212,255,.15)", marginBottom: 24, fontSize: 13, color: "rgba(255,255,255,.8)", lineHeight: 1.6 }}>
            <strong style={{ color: "var(--accent2)" }}>🔧 Setup Required:</strong> To save products, set these in <code style={{ background: "rgba(255,255,255,.08)", padding: "1px 6px", borderRadius: 4 }}>.env.local</code>:<br />
            <code>NEXT_PUBLIC_SUPABASE_URL</code> · <code>NEXT_PUBLIC_SUPABASE_ANON_KEY</code> · <code>SUPABASE_SERVICE_ROLE_KEY</code> · <code>GEMINI_API_KEY</code>
          </div>
        )}

        <StatsBar products={products} />

        {showForm && (
          <ProductForm
            editProduct={editProduct}
            onSave={handleFormSave}
            onCancel={() => { setShowForm(false); setEditProduct(null); }}
            showToast={showToast}
          />
        )}

        {/* Products Table */}
        {loading ? (
          <div className="page-loader">
            <div className="loader-ring" />
            <p className="loader-text">Loading products...</p>
          </div>
        ) : (
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
                      No products yet. Click "Add Product" to get started.
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
                        <div style={{ fontWeight: 600, color: "#fff", marginBottom: 3 }}>{product.name}</div>
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
                        <div style={{ fontWeight: 700, color: "#fff" }}>₹{product.price?.toLocaleString("en-IN")}</div>
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
        )}
      </main>

      <Toast {...toast} />
    </div>
  );
}
