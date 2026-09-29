import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add cssFilter state
js = js.replace(
    'const [bgColor, setBgColor] = useState("#0d1117");',
    'const [bgColor, setBgColor] = useState("#0d1117");\n  const [cssFilter, setCssFilter] = useState("");'
)

# Apply filter in runGeminiEnhance
js = js.replace(
    'if (d.category) setCategory(d.category);\n          showToast',
    'if (d.category) setCategory(d.category);\n          if (d.suggestedCssFilter) setCssFilter(d.suggestedCssFilter);\n          showToast'
)

# Apply to image render
js = js.replace(
    '<img src={imagePreview} alt="Preview" style={{ width: "100%", height: "100%", objectFit: "cover" }} />',
    '<img src={imagePreview} alt="Preview" style={{ width: "100%", height: "100%", objectFit: "cover", filter: cssFilter, transition: "filter 0.5s ease" }} />'
)

# Change the tag text to "AI Enhanced" if filter is applied
js = js.replace(
    '<div className="upload-preview-tag enhanced">Preview</div>',
    '<div className="upload-preview-tag enhanced">{cssFilter ? "o"" AI Enhanced" : "Preview"}</div>'
)

# Reset filter when image is removed
js = js.replace(
    'setImagePreview(""); setImageFile(null); setImageUrl("");',
    'setImagePreview(""); setImageFile(null); setImageUrl(""); setCssFilter("");'
)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Added cssFilter logic!")
