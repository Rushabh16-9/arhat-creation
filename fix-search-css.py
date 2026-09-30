with open('app/globals.css', 'a', encoding='utf-8') as f:
    f.write("""
/* FIX MOBILE SEARCH BAR SQUISHING */
@media (max-width: 640px) {
  .search-input {
    flex-basis: 100% !important;
    width: 100% !important;
    min-width: 100% !important;
  }
}
""")

print("Search bar mobile fix appended to CSS!")
