import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix Products tab button
js = js.replace(
    'onClick={() => setActiveTab("products")} className={activeTab === "products" ? "active" : ""}',
    'onClick={() => { setActiveTab("products"); setShowForm(false); }} className={!showForm ? "active" : ""}'
)

# Fix Add Product tab button
js = js.replace(
    'onClick={() => { setShowForm(true); setEditProduct(null); setActiveTab("products"); }}\nid="tab-add-product">',
    'onClick={() => { setShowForm(true); setEditProduct(null); }}\nclassName={showForm && !editProduct ? "active" : ""}\nid="tab-add-product">'
)
# Note: the newlines in replace string might be tricky in python, let's use regex
js = re.sub(
    r'onClick=\{\(\) => \{ setShowForm\(true\); setEditProduct\(null\); setActiveTab\("products"\); \}\}\s*id="tab-add-product">',
    r'onClick={() => { setShowForm(true); setEditProduct(null); }}\nclassName={showForm && !editProduct ? "active" : ""}\nid="tab-add-product">',
    js
)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Active tab state fixed!")
