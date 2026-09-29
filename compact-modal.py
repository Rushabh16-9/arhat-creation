import re

with open('app/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Limit description to 3 lines
js = js.replace(
    '<p className="modal-desc">{product.description}</p>',
    '<p className="modal-desc" style={{ display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical", overflow: "hidden", textOverflow: "ellipsis" }}>{product.description}</p>'
)

# Also reduce the massive bottom margin in the price row
js = js.replace(
    'marginBottom: \'20px\'',
    'marginBottom: \'12px\''
)

# And make the order section more compact
js = js.replace(
    '<div className="order-section" style={{ background: \'#fff\', borderRadius: \'24px\', padding: \'24px\', boxShadow: \'0 4px 20px rgba(0,0,0,0.04)\', border: \'1px solid #f1f5f9\', marginTop: \'32px\' }}>',
    '<div className="order-section" style={{ background: \'#fff\', borderRadius: \'20px\', padding: \'20px\', boxShadow: \'0 4px 20px rgba(0,0,0,0.04)\', border: \'1px solid #f1f5f9\', marginTop: \'16px\' }}>'
)

# And reduce the bottom margin of the Place Your Order header
js = js.replace(
    '<div style={{ display: \'flex\', alignItems: \'center\', gap: \'8px\', marginBottom: \'20px\' }}>',
    '<div style={{ display: \'flex\', alignItems: \'center\', gap: \'8px\', marginBottom: \'12px\' }}>'
)

# And reduce the bottom margin of the input wrapper
js = js.replace(
    '<div style={{ position: \'relative\', marginBottom: \'24px\' }}>',
    '<div style={{ position: \'relative\', marginBottom: \'16px\' }}>'
)

with open('app/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Modal layout compacted vertically!")
