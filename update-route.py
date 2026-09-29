import re

with open('app/api/gemini/route.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update the Gemini prompt to ask for css filter
new_prompt = '''"suggestedName": "...",
          "description": "...",
          "category": "...",
          "sellingPoints": ["...", "...", "..."],
          "suggestedCssFilter": "e.g., contrast(1.1) saturate(1.2) brightness(1.05)"
        }'''

js = re.sub(
    r'"suggestedName": "...",\s*"description": "...",\s*"category": "...",\s*"sellingPoints": \["\.\.\.", "\.\.\.", "\.\.\."\]\s*\}\',
    new_prompt,
    js
)

js = js.replace(
    '4. Key selling points (3 bullet points)',
    '4. Key selling points (3 bullet points)\n        5. A suggested CSS filter string to visually enhance the image (brightness, contrast, saturate)'
)

with open('app/api/gemini/route.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated route.js")
