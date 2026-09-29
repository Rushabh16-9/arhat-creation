with open('app/globals.css', 'a', encoding='utf-8') as f:
    f.write("""
/* FIX MOBILE OVERFLOW AND PADDING */
@media (max-width: 640px) {
  .admin-main {
    padding: 16px 16px !important;
  }
  .admin-content {
    padding: 0 !important;
  }
  .upload-section {
    padding: 20px !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }
  .admin-layout {
    width: 100vw;
    overflow-x: hidden;
  }
}
""")

print("Appended padding fixes to CSS!")
