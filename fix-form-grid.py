with open('app/globals.css', 'a', encoding='utf-8') as f:
    f.write("""
/* FIX FORM GRID ON MOBILE */
@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr !important;
  }
  .form-input, .form-textarea {
    width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
  }
}
""")

print("Form grid fixes applied!")
