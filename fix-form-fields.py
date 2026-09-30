import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the div wrappers for the form fields
js = js.replace('<div>\n             <label className="form-label">Product Name *</label>', 
                '<div className="form-field">\n             <label className="form-label">Product Name *</label>')

js = js.replace('<div style={{ flex: 1 }}>\n               <label className="form-label">Price *</label>', 
                '<div className="form-field" style={{ flex: 1 }}>\n               <label className="form-label">Price *</label>')

js = js.replace('<div style={{ flex: 1 }}>\n               <label className="form-label">Original Price</label>', 
                '<div className="form-field" style={{ flex: 1 }}>\n               <label className="form-label">Original Price</label>')

js = js.replace('<div style={{ flex: 1 }}>\n               <label className="form-label">Category</label>', 
                '<div className="form-field" style={{ flex: 1 }}>\n               <label className="form-label">Category</label>')

js = js.replace('<div style={{ flex: 1 }}>\n               <label className="form-label">Stock</label>', 
                '<div className="form-field" style={{ flex: 1 }}>\n               <label className="form-label">Stock</label>')

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Form fields styling fixed!")
