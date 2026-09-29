import re

with open('app/globals.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove the broken grid from .upload-section
css = css.replace(
    '''.upload-section {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 40px;''',
    '''.upload-section {
  display: block;'''
)

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Fixed CSS layout for upload-section!")
