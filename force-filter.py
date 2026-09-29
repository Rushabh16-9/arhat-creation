import re

with open('app/admin/page.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Force the CSS filter to apply even if Gemini omits it or gives a generic response
fix_code = '''
          let filterToApply = "contrast(1.15) saturate(1.2) brightness(1.05)";
          if (d.suggestedCssFilter && !d.suggestedCssFilter.includes("e.g.")) {
            filterToApply = d.suggestedCssFilter;
          }
          setCssFilter(filterToApply);
          showToast'''

js = js.replace(
    'if (d.suggestedCssFilter) setCssFilter(d.suggestedCssFilter);\n          showToast',
    fix_code
)

# Rename the button so they don't think it removes the background
js = js.replace(
    'AI Background Color',
    'AI Suggest BG Color'
)

with open('app/admin/page.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Forced CSS filter and renamed button!")
