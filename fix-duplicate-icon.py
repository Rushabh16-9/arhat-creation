import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Remove the duplicate mobile-style button from the desktop sidebar
duplicate_block = """<li>
<button onClick={() => { setActiveTab("bulk"); setShowForm(false); }} className={activeTab === "bulk" && !showForm ? "active" : ""}>
<div style={{ fontSize: '20px', marginBottom: '4px' }}>{"\\uD83D\\uDCF8"}</div>
<span>Bulk</span>
</button>"""

js = js.replace(duplicate_block, "<li>")

# 2. Replace the Camera icon with the Inbox Tray icon for Bulk Upload
js = js.replace('{"\\uD83D\\uDCF8"} Bulk Upload', '{"\\uD83D\\uDCE5"} Bulk Upload')
js = js.replace('{"\\uD83D\\uDCF8"}', '{"\\uD83D\\uDCE5"}')

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Duplicate button removed and icon updated!")
