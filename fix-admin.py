import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

admin_css = '''
/* MISSING ADMIN FIXES */
.sidebar-logo {
  padding: 32px 24px;
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 800;
  color: var(--primary);
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
}
.sidebar-logo span {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--gold);
  margin-top: 4px;
}
.upload-preview {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--border);
  position: relative;
  background: var(--bg3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}
.upload-icon {
  font-size: 40px;
  color: var(--text-dim);
  margin-bottom: 8px;
}
.upload-text {
  font-size: 13px;
  color: var(--text-muted);
  text-align: center;
  line-height: 1.5;
}
.upload-preview-tag {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255,255,255,0.9);
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  color: var(--primary);
}
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-top: 24px;
}
.form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.form-field.full {
  grid-column: 1 / -1;
}
.upload-section {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 40px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 40px;
  margin-bottom: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}
@media (max-width: 900px) {
  .upload-section {
    grid-template-columns: 1fr;
  }
}
.admin-main {
  padding-bottom: 80px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}
.stat-card {
  padding: 24px;
  border-radius: 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}
'''

if 'MISSING ADMIN FIXES' not in css:
    css = css + admin_css

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Admin CSS updated!")
