import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_input = '''                <input 
                  type="number" 
                  min="1" 
                  max={selectedProduct?.stock || 1}
                  value={qty} 
                  onChange={e => setQty(parseInt(e.target.value) || 1)}
                  style={{ width: '100%', padding: '12px', borderRadius: '10px', border: '1px solid var(--border)', outline: 'none' }}
                />'''

new_input = '''                <input 
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
                />'''

# We must be careful because string exact match might fail due to spaces/newlines.
js = re.sub(
    r'<input\s*type="number"\s*min="1"\s*max=\{selectedProduct\?\.stock \|\| 1\}\s*value=\{qty\}\s*onChange=\{e => setQty\(parseInt\(e\.target\.value\) \|\| 1\)\}\s*style=\{\{ width: \'100%\', padding: \'12px\', borderRadius: \'10px\', border: \'1px solid var\(--border\)\', outline: \'none\' \}\}\s*/>',
    lambda _: new_input,
    js,
    flags=re.DOTALL
)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Quantity input logic fixed!")
