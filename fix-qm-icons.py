import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace corrupted Rupee symbols
js = js.replace('<span style={{ position: \'absolute\', left: 16, top: \'50%\', transform: \'translateY(-50%)\', fontWeight: 600, color: \'var(--text-muted)\' }}>?</span>', 
                '<span style={{ position: \'absolute\', left: 16, top: \'50%\', transform: \'translateY(-50%)\', fontWeight: 600, color: \'var(--text-muted)\' }}>{"\\u20B9"}</span>')

# Replace corrupted Sparkles and Arrow emojis
js = js.replace('"? Save & Finish"', '"\\u2728 Save & Finish"')
js = js.replace('"Next Image ?"', '"Next Image \\u2794"')

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Icons successfully fixed!")
