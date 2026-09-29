import re

with open('app/api/gemini/route.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_json = '''"suggestedName": "...",
          "description": "...",
          "category": "...",
          "sellingPoints": ["...", "...", "..."]
        }'''
        
new_json = '''"suggestedName": "...",
          "description": "...",
          "category": "...",
          "sellingPoints": ["...", "...", "..."],
          "suggestedCssFilter": "e.g., contrast(1.1) saturate(1.2)"
        }'''

js = js.replace(old_json, new_json)

old_text = '4. Key selling points (3 bullet points)'
new_text = '4. Key selling points (3 bullet points)\\n        5. A suggested CSS filter string to visually enhance the image (brightness, contrast, saturate)'
js = js.replace(old_text, new_text)

with open('app/api/gemini/route.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated route.js correctly")
