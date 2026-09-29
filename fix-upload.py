import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

upload_area_css = '''
.upload-area {
  border: 2px dashed var(--border2);
  border-radius: 16px;
  background: var(--bg3);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 32px 16px;
  cursor: pointer;
  transition: all .2s;
}
.upload-area:hover, .upload-area.drag-over {
  border-color: var(--primary);
  background: rgba(15, 23, 42, 0.03);
}
.upload-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 12px;
}
'''

if '.upload-area {' not in css:
    css = css + upload_area_css

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Added upload-area CSS!")
