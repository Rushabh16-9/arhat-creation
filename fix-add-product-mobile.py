with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the hardcoded layout grid
old_grid = '<div style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 28, alignItems: "start" }}>'
new_grid = '<div className="add-product-grid">'
js = js.replace(old_grid, new_grid)

# Replace the hardcoded image column width
old_img_col = '{/* Image Upload Column */}\n        <div style={{ width: 200 }}>'
new_img_col = '{/* Image Upload Column */}\n        <div className="add-product-img-col">'
js = js.replace(old_img_col, new_img_col)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Page.js updated to use CSS classes instead of inline styles!")

with open('app/globals.css', 'a', encoding='utf-8') as f:
    f.write("""
/* ADD PRODUCT FORM LAYOUT */
.add-product-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 28px;
  align-items: start;
}
.add-product-img-col {
  width: 200px;
}

@media (max-width: 640px) {
  .add-product-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  .add-product-img-col {
    width: 100%;
    max-width: 240px;
    margin: 0 auto;
  }
}
""")
print("CSS appended!")
