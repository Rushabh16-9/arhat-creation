import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add missing admin header and button styles
admin_header_css = '''
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}
.admin-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 4px;
}
.admin-subtitle {
  color: var(--text-muted);
  font-size: 14px;
}
.add-product-btn {
  height: 48px;
  padding: 0 24px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  background: var(--primary);
  color: #fff;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
  transition: all .2s ease;
}
.add-product-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.2);
}
'''

if '.admin-header {' not in css:
    css = css + admin_header_css
else:
    # Replace existing admin-header with flexbox version
    css = re.sub(r'\.admin-header\s*\{[^}]*\}', '.admin-header {\n  display: flex;\n  justify-content: space-between;\n  align-items: flex-start;\n  margin-bottom: 32px;\n  flex-wrap: wrap;\n  gap: 16px;\n}', css)
    
if '.add-product-btn {' not in css:
    css = css + '''
.add-product-btn {
  height: 48px;
  padding: 0 24px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  background: var(--primary);
  color: #fff;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
  transition: all .2s ease;
}
.add-product-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.2);
}
'''

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Admin Header & Button Fixed!")
