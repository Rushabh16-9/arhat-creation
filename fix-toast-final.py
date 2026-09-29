import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Completely replace the broken .toast block
proper_toast_css = '''
.toast {
  position: fixed !important;
  z-index: 9999 !important;
  bottom: 32px !important;
  right: 32px !important;
  top: auto !important;
  padding: 16px 24px !important;
  height: max-content !important;
  max-height: 60px !important;
  display: flex !important;
  align-items: center !important;
  border-radius: 16px !important;
  box-shadow: 0 12px 40px rgba(15,23,42,0.12) !important;
  border: 1px solid #e2e8f0 !important;
  background: #ffffff !important;
  color: #0f172a !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  transform: translateX(150%) !important;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.toast.show {
  transform: translateX(0) !important;
}
.toast.success {
  border-left: 4px solid #10b981 !important;
}
.toast.error {
  border-left: 4px solid #ef4444 !important;
}
.toast.info {
  border-left: 4px solid #3b82f6 !important;
}
'''

# Find and remove all existing .toast blocks
css = re.sub(r'\.toast(\.show|\.success|\.error|\.info)?\s*\{[^}]*\}', '', css)

# Append the fixed block
css = css + '\n' + proper_toast_css

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Toast CSS fully restored and fixed!")
