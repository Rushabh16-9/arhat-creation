with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Extract just the admin parts to analyze
import re
admin_styles = re.findall(r'/\* ADMIN LAYOUT \*/.*?/\* =', css, re.DOTALL)
if admin_styles:
    print(admin_styles[0][:2000])
else:
    print("Could not find admin styles")
