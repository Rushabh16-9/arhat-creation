import os

css_path = 'app/globals.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

overhaul_css = '''
/* === PREMIUM ADMIN OVERHAUL === */
.admin-main {
  padding: 48px 56px !important;
  background: #f8fafc !important;
}
.admin-title {
  font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
  font-size: 28px !important;
  letter-spacing: -0.03em !important;
  color: #0f172a !important;
}
.sidebar-logo {
  font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
  font-size: 22px !important;
  letter-spacing: -0.03em !important;
  color: #0f172a !important;
  border-bottom: 1px solid #e2e8f0 !important;
}
.sidebar-logo span {
  color: #64748b !important;
  letter-spacing: 0.1em !important;
}
.admin-sidebar {
  border-right: 1px solid #e2e8f0 !important;
  background: #ffffff !important;
  box-shadow: 1px 0 20px rgba(15,23,42,0.02) !important;
}
.stat-card {
  box-shadow: 0 10px 30px rgba(15,23,42,0.03) !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 24px !important;
  background: #ffffff !important;
  padding: 28px !important;
}
.stat-label {
  font-size: 13px !important;
  color: #64748b !important;
  font-weight: 600 !important;
}
.admin-table-wrap {
  box-shadow: 0 10px 40px rgba(15,23,42,0.04) !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 24px !important;
  background: #ffffff !important;
  padding: 8px !important;
}
.admin-table th {
  background: transparent !important;
  color: #64748b !important;
  border-bottom: 1px solid #e2e8f0 !important;
  font-size: 12px !important;
}
.admin-table td {
  border-bottom: 1px solid #f1f5f9 !important;
  color: #334155 !important;
}
.admin-table tbody tr:hover td {
  background: #f8fafc !important;
}
.toast {
  top: auto !important;
  bottom: 32px !important;
  right: 32px !important;
  border-radius: 16px !important;
  box-shadow: 0 12px 40px rgba(15,23,42,0.1) !important;
  border: 1px solid #e2e8f0 !important;
  background: #ffffff !important;
  color: #0f172a !important;
}
.action-btn {
  border-radius: 10px !important;
  font-weight: 600 !important;
  padding: 8px 14px !important;
}
.action-btn.edit {
  background: #f1f5f9 !important;
  color: #475569 !important;
  border-color: #e2e8f0 !important;
}
.action-btn.delete {
  background: #fef2f2 !important;
  color: #ef4444 !important;
  border-color: #fecaca !important;
}
.sidebar-nav li a.active, .sidebar-nav li button.active {
  background: #f1f5f9 !important;
  color: #0f172a !important;
  font-weight: 600 !important;
}
.admin-subtitle {
  color: #64748b !important;
  margin-top: 6px !important;
}
'''

if 'PREMIUM ADMIN OVERHAUL' not in css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write('\n' + overhaul_css)
    print("Appended premium admin styles")
else:
    print("Already appended")
